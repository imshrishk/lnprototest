import React, { useState, useEffect } from 'react';
import {
  Container,
  Header,
  Tabs,
  Box,
  SpaceBetween,
  Button,
  Select,
  Alert,
  Spinner,
  FormField,
  Input,
  Table,
  Modal,
  ButtonDropdown
} from '@cloudscape-design/components';
import { lnprototestApi } from '../api/lnprototestApi';
import { Node, Message, EventSequence } from '../types';
import MessageList from './MessageList';
import NodeConnector from './NodeConnector';

const MessageFlowVisualizer: React.FC = () => {
  // State
  const [nodes, setNodes] = useState<Node[]>([]);
  const [selectedNode, setSelectedNode] = useState<Node | null>(null);
  const [availableSequences, setAvailableSequences] = useState<EventSequence[]>([]);
  const [selectedSequence, setSelectedSequence] = useState<EventSequence | null>(null);
  const [messages, setMessages] = useState<Message[]>([]);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const [activeTab, setActiveTab] = useState('messageFlow');
  const [isConnectModalVisible, setIsConnectModalVisible] = useState(false);

  // Load implementations on mount
  useEffect(() => {
    loadImplementations();
    loadTestSequences();
  }, []);

  // Load available implementations
  const loadImplementations = async () => {
    setLoading(true);
    const response = await lnprototestApi.getImplementations();
    setLoading(false);

    if (response.success && response.data) {
      setNodes(response.data);
    } else {
      setError(response.error || 'Failed to load implementations');
    }
  };

  // Load test sequences
  const loadTestSequences = async () => {
    setLoading(true);
    const response = await lnprototestApi.getTestSequences();
    setLoading(false);

    if (response.success && response.data) {
      setAvailableSequences(response.data);
    } else {
      setError(response.error || 'Failed to load test sequences');
    }
  };

  // Handle node selection
  const handleNodeSelect = (nodeId: string) => {
    const node = nodes.find(n => n.id === nodeId);
    if (node) {
      setSelectedNode(node);
      loadNodeMessages(nodeId);
    }
  };

  // Load node message history
  const loadNodeMessages = async (nodeId: string) => {
    setLoading(true);
    const response = await lnprototestApi.getMessageHistory(nodeId);
    setLoading(false);

    if (response.success && response.data) {
      setMessages(response.data);
    } else {
      setError(response.error || 'Failed to load message history');
    }
  };

  // Handle sequence selection
  const handleSequenceSelect = (sequenceId: string) => {
    const sequence = availableSequences.find(s => s.id === sequenceId);
    if (sequence) {
      setSelectedSequence(sequence);
    }
  };

  // Run a test sequence
  const runSequence = async () => {
    if (!selectedNode || !selectedSequence) {
      setError('Please select a node and a sequence');
      return;
    }

    setLoading(true);
    const response = await lnprototestApi.runTestSequence(
      selectedSequence.id,
      selectedNode.id
    );
    setLoading(false);

    if (response.success && response.data) {
      // Fix for TS2461: Ensure response.data is treated as an array
      const newMessages = Array.isArray(response.data) ? response.data : [response.data];
      setMessages(prev => [...prev, ...newMessages]);
    } else {
      setError(response.error || 'Failed to run test sequence');
    }
  };

  // Send a custom message
  const sendCustomMessage = async (message: Partial<Message>) => {
    if (!selectedNode) {
      setError('Please select a node');
      return;
    }

    setLoading(true);
    const response = await lnprototestApi.sendMessage(selectedNode.id, message);
    setLoading(false);

    if (response.success && response.data) {
      // Fix for TS2345: Ensure we're adding a Message, not undefined
      const newMessage = response.data;
      setMessages(prev => [...prev, newMessage as Message]);
    } else {
      setError(response.error || 'Failed to send message');
    }
  };

  // Connect to a node
  const handleNodeConnect = async (nodeId: string, host: string, port: number) => {
    setLoading(true);
    const response = await lnprototestApi.connectNode(nodeId, {
      nodeId,
      host,
      port,
      pubkey: 'dummy-pubkey' // In a real app, we would get this from user input
    });
    setLoading(false);
    setIsConnectModalVisible(false);

    if (response.success && response.data) {
      // Fix for TS2345: Properly handle potentially undefined response.data
      const updatedNode = response.data as Node;
      setNodes(prev => prev.map(n => (n.id === nodeId ? updatedNode : n)));
      setSelectedNode(updatedNode);
    } else {
      setError(response.error || 'Failed to connect to node');
    }
  };

  // Disconnect from a node
  const handleNodeDisconnect = async () => {
    if (!selectedNode) {
      setError('No node selected');
      return;
    }

    setLoading(true);
    const response = await lnprototestApi.disconnectNode(selectedNode.id);
    setLoading(false);

    if (response.success) {
      setNodes(prev => 
        prev.map(n => 
          n.id === selectedNode.id 
            ? { ...n, status: 'disconnected' } 
            : n
        )
      );
      setSelectedNode(prev => 
        prev ? { ...prev, status: 'disconnected' } : null
      );
    } else {
      setError(response.error || 'Failed to disconnect from node');
    }
  };

  // Render error alert if there's an error
  const renderError = () => {
    if (!error) return null;
    
    return (
      <Alert 
        type="error" 
        dismissible 
        onDismiss={() => setError(null)}
      >
        {error}
      </Alert>
    );
  };

  const renderNodeSelector = () => {
    return (
      <FormField label="Select Lightning Node Implementation">
        <Select
          selectedOption={selectedNode ? { label: selectedNode.name, value: selectedNode.id } : null}
          onChange={({ detail }) => handleNodeSelect(detail.selectedOption.value as string)}
          options={nodes.map(node => ({
            label: `${node.name} (${node.status})`,
            value: node.id
          }))}
          placeholder="Select a node implementation"
        />
      </FormField>
    );
  };

  const renderSequenceSelector = () => {
    return (
      <FormField label="Select Test Sequence">
        <Select
          selectedOption={selectedSequence ? { label: selectedSequence.name, value: selectedSequence.id } : null}
          onChange={({ detail }) => handleSequenceSelect(detail.selectedOption.value as string)}
          options={availableSequences.map(seq => ({
            label: seq.name,
            value: seq.id,
            description: seq.description
          }))}
          placeholder="Select a test sequence"
        />
      </FormField>
    );
  };

  const renderNodeActions = () => {
    if (!selectedNode) return null;

    return (
      <SpaceBetween direction="horizontal" size="s">
        {selectedNode.status === 'disconnected' ? (
          <Button 
            onClick={() => setIsConnectModalVisible(true)}
            variant="primary"
          >
            Connect
          </Button>
        ) : (
          <Button 
            onClick={handleNodeDisconnect}
            variant="primary"
          >
            Disconnect
          </Button>
        )}
        <ButtonDropdown
          items={[
            { id: 'init', text: 'Send Init Message' },
            { id: 'ping', text: 'Send Ping Message' },
            { id: 'custom', text: 'Send Custom Message' }
          ]}
          onItemClick={({ detail }) => {
            // In a real app, these would open different message dialogs
            if (detail.id === 'init') {
              sendCustomMessage({
                type: 'init',
                content: { globalfeatures: '', features: '' }
              });
            } else if (detail.id === 'ping') {
              sendCustomMessage({
                type: 'ping',
                content: { num_pong_bytes: 1, byteslen: 0 }
              });
            }
          }}
          disabled={selectedNode?.status !== 'connected'}
        >
          Send Message
        </ButtonDropdown>
        <Button
          onClick={runSequence}
          disabled={!selectedSequence || selectedNode?.status !== 'connected'}
        >
          Run Test Sequence
        </Button>
      </SpaceBetween>
    );
  };

  const renderConnectModal = () => {
    return (
      <Modal
        visible={isConnectModalVisible}
        onDismiss={() => setIsConnectModalVisible(false)}
        header="Connect to Node"
        footer={
          <Box float="right">
            <SpaceBetween direction="horizontal" size="xs">
              <Button variant="link" onClick={() => setIsConnectModalVisible(false)}>
                Cancel
              </Button>
              <Button variant="primary" onClick={() => {
                // In a real app, we would get these values from form inputs
                if (selectedNode) {
                  handleNodeConnect(selectedNode.id, 'localhost', 9735);
                }
              }}>
                Connect
              </Button>
            </SpaceBetween>
          </Box>
        }
      >
        <NodeConnector 
          onConnect={handleNodeConnect}
          selectedNodeId={selectedNode?.id}
        />
      </Modal>
    );
  };

  return (
    <Container>
      <SpaceBetween size="l">
        {renderError()}
        
        {loading && (
          <Box textAlign="center">
            <Spinner size="large" />
          </Box>
        )}
        
        <Tabs
          activeTabId={activeTab}
          onChange={({ detail }) => setActiveTab(detail.activeTabId)}
          tabs={[
            {
              id: 'messageFlow',
              label: 'Message Flow',
              content: (
                <SpaceBetween size="l">
                  {renderNodeSelector()}
                  {renderSequenceSelector()}
                  {renderNodeActions()}
                  
                  <Box>
                    <Header variant="h2">Message Flow</Header>
                    <MessageList messages={messages} />
                  </Box>
                </SpaceBetween>
              )
            },
            {
              id: 'documentation',
              label: 'Documentation',
              content: (
                <Box>
                  <Header variant="h2">Lightning Network Protocol Documentation</Header>
                  <p>This visualizer implements the Lightning Network protocol as specified in BOLT #1.</p>
                  <p>For more information, see <a href="https://github.com/lightning/bolts/blob/master/01-messaging.md" target="_blank" rel="noopener noreferrer">BOLT #1: Base Protocol</a>.</p>
                </Box>
              )
            }
          ]}
        />
      </SpaceBetween>
      
      {renderConnectModal()}
    </Container>
  );
};

export default MessageFlowVisualizer;
