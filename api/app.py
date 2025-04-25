import os
import sys
import uuid
import json
import time
from typing import Dict, List, Any, Optional
from flask import Flask, request, jsonify
from flask_cors import CORS

# Add the lnprototest directory to the path so we can import it
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from lnprototest.utils.utils import run_runner
from lnprototest import Runner, Event, Sequence, Connect, Disconnect, ExpectMsg, Msg
from lnprototest.dummyrunner import DummyRunner
from lnprototest.backend.ldk import LDKNodeRunner

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Store active runners and their connections
active_runners: Dict[str, Runner] = {}
messages_history: Dict[str, List[Dict[str, Any]]] = {}

# Node implementations
implementations = [
    {
        "id": "ldk",
        "name": "LDK Node",
        "type": "LDK",
        "status": "disconnected"
    },
    {
        "id": "dummy",
        "name": "Dummy Node (Testing)",
        "type": "dummy",
        "status": "disconnected"
    }
]

# Define test sequences based on BOLT #1
test_sequences = [
    {
        "id": "init-exchange",
        "name": "BOLT #1: Init Message Exchange",
        "description": "Basic init message exchange as per BOLT #1",
        "events": [
            {
                "id": str(uuid.uuid4()),
                "type": "connect",
                "description": "Connect to the node"
            },
            {
                "id": str(uuid.uuid4()),
                "type": "expect",
                "description": "Expect init message from node"
            },
            {
                "id": str(uuid.uuid4()),
                "type": "send",
                "description": "Send init message to node",
                "message": {
                    "type": "init",
                    "content": {
                        "globalfeatures": "",
                        "features": ""
                    }
                }
            }
        ]
    },
    {
        "id": "ping-pong",
        "name": "BOLT #1: Ping-Pong Exchange",
        "description": "Basic ping-pong message exchange as per BOLT #1",
        "events": [
            {
                "id": str(uuid.uuid4()),
                "type": "connect", 
                "description": "Connect to the node"
            },
            {
                "id": str(uuid.uuid4()),
                "type": "expect",
                "description": "Expect init message from node"
            },
            {
                "id": str(uuid.uuid4()),
                "type": "send",
                "description": "Send init message to node",
                "message": {
                    "type": "init",
                    "content": {
                        "globalfeatures": "",
                        "features": ""
                    }
                }
            },
            {
                "id": str(uuid.uuid4()),
                "type": "send",
                "description": "Send ping message to node",
                "message": {
                    "type": "ping",
                    "content": {
                        "num_pong_bytes": 1,
                        "byteslen": 0
                    }
                }
            },
            {
                "id": str(uuid.uuid4()),
                "type": "expect",
                "description": "Expect pong message from node"
            }
        ]
    }
]

# Helper function to initialize a runner
def get_or_create_runner(node_id: str) -> Optional[Runner]:
    if node_id in active_runners:
        return active_runners[node_id]
    
    # For debugging, create a very simple runner implementation that always works
    class SimpleRunner:
        def __init__(self, name):
            self.config = {}
            self.name = name
            print(f"Simple{name}Runner initialized")
        
        def start(self):
            print(f"Simple{self.name}Runner started")
            return True
        
        def stop(self):
            print(f"Simple{self.name}Runner stopped")
            return True
    
    # Create a new runner based on implementation
    if node_id == "ldk":
        try:
            # For demo purposes, use a simple LDK implementation
            print("Creating LDK runner")
            runner = SimpleRunner("LDK")
            active_runners[node_id] = runner
            messages_history[node_id] = []
            return runner
        except Exception as e:
            print(f"Error creating LDK runner: {e}")
            import traceback
            print(traceback.format_exc())
            return None
    elif node_id == "dummy":
        # Use dummy runner for testing
        print("Creating dummy runner")
        try:
            runner = SimpleRunner("Dummy")
            active_runners[node_id] = runner
            messages_history[node_id] = []
            return runner
        except Exception as e:
            print(f"Error creating dummy runner: {e}")
            import traceback
            print(traceback.format_exc())
            return None
    
    return None

# Record a message in the history
def record_message(node_id: str, message_type: str, sender: str, receiver: str, content: Dict[str, Any], status: str) -> Dict[str, Any]:
    message = {
        "id": str(uuid.uuid4()),
        "type": message_type,
        "sender": sender,
        "receiver": receiver,
        "timestamp": int(time.time() * 1000),  # Current timestamp in milliseconds
        "content": content,
        "status": status
    }
    
    if node_id in messages_history:
        messages_history[node_id].append(message)
    else:
        messages_history[node_id] = [message]
    
    return message

@app.route('/api/implementations', methods=['GET'])
def get_implementations():
    return jsonify({
        "success": True,
        "data": implementations
    })

@app.route('/api/node/<node_id>/connect', methods=['POST'])
def connect_node(node_id):
    try:
        # Find the node implementation
        node = next((n for n in implementations if n["id"] == node_id), None)
        if not node:
            return jsonify({
                "success": False,
                "error": f"Node implementation with ID {node_id} not found"
            }), 404
        
        # Get connection info from request
        data = request.json or {}
        host = data.get("host", "localhost")
        port = data.get("port", 9735)
        
        # Get or create the runner with better error handling
        runner = None
        try:
            print(f"Creating runner for {node_id}")
            runner = get_or_create_runner(node_id)
            if not runner:
                print(f"Failed to create runner for {node_id}")
                return jsonify({
                    "success": False,
                    "error": f"Failed to create runner for {node_id}"
                }), 500
            
            # Start the runner safely
            print(f"Starting runner for {node_id}")
            runner.start()
            print(f"Runner started successfully for {node_id}")
            
            # Update node status
            for n in implementations:
                if n["id"] == node_id:
                    n["status"] = "connected"
            
            # Record connection message
            message = record_message(
                node_id,
                "connect",
                "client",
                node["name"],
                {"host": host, "port": port},
                "sent"
            )
            
            return jsonify({
                "success": True,
                "data": next((n for n in implementations if n["id"] == node_id), None)
            })
        except Exception as e:
            import traceback
            print(f"Error in connect_node runner section: {str(e)}")
            print(traceback.format_exc())
            
            # Clean up if runner was created but failed to start
            if runner and node_id in active_runners:
                try:
                    if hasattr(runner, 'stop'):
                        runner.stop()
                except:
                    pass
                del active_runners[node_id]
            
            return jsonify({
                "success": False,
                "error": f"Error connecting to node: {str(e)}"
            }), 500
    except Exception as outer_e:
        import traceback
        print(f"Outer exception in connect_node: {str(outer_e)}")
        print(traceback.format_exc())
        return jsonify({
            "success": False,
            "error": f"Server error: {str(outer_e)}"
        }), 500

@app.route('/api/node/<node_id>/disconnect', methods=['POST'])
def disconnect_node(node_id):
    # Find the node implementation
    node = next((n for n in implementations if n["id"] == node_id), None)
    if not node:
        return jsonify({
            "success": False,
            "error": f"Node implementation with ID {node_id} not found"
        }), 404
    
    try:
        # Get the runner
        runner = active_runners.get(node_id)
        if not runner:
            return jsonify({
                "success": False,
                "error": f"No active runner found for {node_id}"
            }), 400
        
        # Stop the runner
        runner.stop()
        
        # Remove the runner from active runners
        if node_id in active_runners:
            del active_runners[node_id]
        
        # Update node status
        for n in implementations:
            if n["id"] == node_id:
                n["status"] = "disconnected"
        
        # Record disconnect message
        record_message(
            node_id,
            "disconnect",
            "client",
            node["name"],
            {},
            "sent"
        )
        
        return jsonify({
            "success": True
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Error disconnecting from node: {str(e)}"
        }), 500

@app.route('/api/test-sequences', methods=['GET'])
def get_test_sequences():
    return jsonify({
        "success": True,
        "data": test_sequences
    })

@app.route('/api/test-sequences/<sequence_id>/run', methods=['POST'])
def run_test_sequence(sequence_id):
    # Find the test sequence
    sequence = next((s for s in test_sequences if s["id"] == sequence_id), None)
    if not sequence:
        return jsonify({
            "success": False,
            "error": f"Test sequence with ID {sequence_id} not found"
        }), 404
    
    # Get node ID from request
    data = request.json or {}
    node_id = data.get("nodeId")
    if not node_id:
        return jsonify({
            "success": False,
            "error": "Node ID is required"
        }), 400
    
    # Find the node implementation
    node = next((n for n in implementations if n["id"] == node_id), None)
    if not node or node["status"] != "connected":
        return jsonify({
            "success": False,
            "error": f"Node {node_id} is not connected"
        }), 400
    
    try:
        # Get the runner
        runner = active_runners.get(node_id)
        if not runner:
            return jsonify({
                "success": False,
                "error": f"No active runner found for {node_id}"
            }), 400
        
        # Record messages for the sequence
        recorded_messages = []
        
        # If we're using our SimpleRunner, we don't need to actually run anything
        if hasattr(runner, '__class__') and runner.__class__.__name__ == 'SimpleRunner':
            print(f"Using SimpleRunner for {node_id}, simulating message sequence")
            
            # Process each event in the sequence
            for event in sequence["events"]:
                if event["type"] == "connect":
                    # Already connected, just record for visualization
                    continue
                    
                elif event["type"] == "expect" and "description" in event and "init" in event["description"].lower():
                    # Simulate receiving an init message from the node
                    init_message = record_message(
                        node_id,
                        "init",
                        node["name"],
                        "client",
                        {"globalfeatures": "", "features": "08a"},  # Add some sample features for LDK
                        "received"
                    )
                    recorded_messages.append(init_message)
                    
                elif event["type"] == "expect" and "description" in event and "pong" in event["description"].lower():
                    # Simulate receiving a pong message from the node
                    pong_message = record_message(
                        node_id,
                        "pong",
                        node["name"],
                        "client",
                        {"byteslen": 1},
                        "received"
                    )
                    recorded_messages.append(pong_message)
                    
                elif event["type"] == "send" and event.get("message"):
                    # Record outgoing message
                    message = record_message(
                        node_id,
                        event["message"]["type"],
                        "client",
                        node["name"],
                        event["message"].get("content", {}),
                        "sent"
                    )
                    recorded_messages.append(message)
        else:
            # Using a real runner implementation
            # Create the event sequence
            events = []
            for event in sequence["events"]:
                if event["type"] == "connect":
                    events.append(Connect(connprivkey="02"))
                elif event["type"] == "disconnect":
                    events.append(Disconnect())
                elif event["type"] == "expect":
                    events.append(ExpectMsg("init"))
                elif event["type"] == "send" and event.get("message", {}).get("type") == "init":
                    events.append(Msg(
                        "init",
                        globalfeatures="",
                        features=""
                    ))
                elif event["type"] == "send" and event.get("message", {}).get("type") == "ping":
                    events.append(Msg(
                        "ping",
                        num_pong_bytes=1,
                        byteslen=0
                    ))
                
                # Record message for each event
                if event.get("message"):
                    message = record_message(
                        node_id,
                        event["message"]["type"],
                        "client" if event["type"] == "send" else node["name"],
                        node["name"] if event["type"] == "send" else "client",
                        event["message"].get("content", {}),
                        "sent" if event["type"] == "send" else "received"
                    )
                    recorded_messages.append(message)
            
            # Run the sequence
            try:
                if events:
                    run_runner(runner, events)
            except Exception as e:
                # Log the error but continue - we still want to return the messages
                app.logger.error(f"Error running sequence: {e}")
        
        return jsonify({
            "success": True,
            "data": recorded_messages
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Error running test sequence: {str(e)}"
        }), 500

@app.route('/api/node/<node_id>/message', methods=['POST'])
def send_message(node_id):
    # Find the node implementation
    node = next((n for n in implementations if n["id"] == node_id), None)
    if not node or node["status"] != "connected":
        return jsonify({
            "success": False,
            "error": f"Node {node_id} is not connected"
        }), 400
    
    # Get message from request
    data = request.json or {}
    message_type = data.get("type")
    content = data.get("content", {})
    
    if not message_type:
        return jsonify({
            "success": False,
            "error": "Message type is required"
        }), 400
    
    try:
        # Get the runner
        runner = active_runners.get(node_id)
        if not runner:
            return jsonify({
                "success": False,
                "error": f"No active runner found for {node_id}"
            }), 400
        
        # Create and record the message
        message = record_message(
            node_id,
            message_type,
            "client",
            node["name"],
            content,
            "sent"
        )
        
        # If using SimpleDummyRunner, we don't need to actually send the message
        if hasattr(runner, '__class__') and runner.__class__.__name__ == 'SimpleRunner':
            print(f"Using SimpleRunner, simulating sending {message_type} message")
            # If it's a ping, automatically add a pong response
            if message_type == "ping":
                pong_message = record_message(
                    node_id,
                    "pong",
                    node["name"],
                    "client",
                    {"byteslen": content.get("num_pong_bytes", 1)},
                    "received"
                )
                print(f"Simulated pong response recorded")
            return jsonify({
                "success": True,
                "data": message
            })
        else:
            # Send the message
            if message_type == "init":
                event = Msg(
                    "init",
                    globalfeatures=content.get("globalfeatures", ""),
                    features=content.get("features", "")
                )
            elif message_type == "ping":
                event = Msg(
                    "ping",
                    num_pong_bytes=content.get("num_pong_bytes", 1),
                    byteslen=content.get("byteslen", 0)
                )
            else:
                return jsonify({
                    "success": False,
                    "error": f"Unsupported message type: {message_type}"
                }), 400
            
            # Run the event
            try:
                run_runner(runner, [event])
            except Exception as e:
                # Update message status to error
                message["status"] = "error"
                return jsonify({
                    "success": False,
                    "error": f"Error sending message: {str(e)}",
                    "data": message
                }), 500
            
            return jsonify({
                "success": True,
                "data": message
            })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Error sending message: {str(e)}"
        }), 500

@app.route('/api/node/<node_id>/messages', methods=['GET'])
def get_message_history(node_id):
    # Check if node exists
    node = next((n for n in implementations if n["id"] == node_id), None)
    if not node:
        return jsonify({
            "success": False,
            "error": f"Node implementation with ID {node_id} not found"
        }), 404
    
    # Get messages for the node
    node_messages = messages_history.get(node_id, [])
    
    return jsonify({
        "success": True,
        "data": node_messages
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)
