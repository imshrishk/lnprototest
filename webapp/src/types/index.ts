// Node types
export interface Node {
  id: string;
  name: string;
  type: 'LND' | 'CLN' | 'LDK';
  status: 'connected' | 'disconnected';
}

// Message types based on BOLT specs
export interface Message {
  id: string;
  type: string;
  sender: string;
  receiver: string;
  timestamp: number;
  content: Record<string, any>;
  status: 'sent' | 'received' | 'error';
}

// Sequence of events for message flow
export interface EventSequence {
  id: string;
  name: string;
  description: string;
  events: Event[];
}

// Event in a test sequence
export interface Event {
  id: string;
  type: 'connect' | 'disconnect' | 'send' | 'expect' | 'other';
  description: string;
  nodeId?: string;
  message?: Message;
}

// API types for interacting with lnprototest
export interface TestRunOptions {
  implementation: 'ldk' | 'cln' | 'lnd';
  testSequence: EventSequence;
}

// API response types
export interface ApiResponse<T> {
  success: boolean;
  data?: T;
  error?: string;
}

// Node connection info
export interface ConnectionInfo {
  nodeId: string;
  pubkey: string;
  port: number;
  host: string;
}
