import axios from 'axios';
import { 
  ApiResponse, 
  Node, 
  Message, 
  EventSequence, 
  ConnectionInfo 
} from '../types';

// API base URL - would be configurable in a production app
const API_BASE_URL = 'http://localhost:5000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// API functions for interacting with lnprototest
export const lnprototestApi = {
  // Get available implementations
  getImplementations: async (): Promise<ApiResponse<Node[]>> => {
    try {
      const response = await api.get<ApiResponse<Node[]>>('/implementations');
      return response.data;
    } catch (error) {
      return { 
        success: false, 
        error: error instanceof Error ? error.message : 'Unknown error' 
      };
    }
  },

  // Connect to a node
  connectNode: async (nodeId: string, connInfo: ConnectionInfo): Promise<ApiResponse<Node>> => {
    try {
      const response = await api.post<ApiResponse<Node>>(`/node/${nodeId}/connect`, connInfo);
      return response.data;
    } catch (error) {
      return { 
        success: false, 
        error: error instanceof Error ? error.message : 'Unknown error' 
      };
    }
  },

  // Disconnect from a node
  disconnectNode: async (nodeId: string): Promise<ApiResponse<void>> => {
    try {
      const response = await api.post<ApiResponse<void>>(`/node/${nodeId}/disconnect`);
      return response.data;
    } catch (error) {
      return { 
        success: false, 
        error: error instanceof Error ? error.message : 'Unknown error' 
      };
    }
  },

  // Get predefined test sequences based on BOLT specs
  getTestSequences: async (): Promise<ApiResponse<EventSequence[]>> => {
    try {
      const response = await api.get<ApiResponse<EventSequence[]>>('/test-sequences');
      return response.data;
    } catch (error) {
      return { 
        success: false, 
        error: error instanceof Error ? error.message : 'Unknown error' 
      };
    }
  },

  // Run a specific test sequence
  runTestSequence: async (sequenceId: string, nodeId: string): Promise<ApiResponse<Message[]>> => {
    try {
      const response = await api.post<ApiResponse<Message[]>>(`/test-sequences/${sequenceId}/run`, { nodeId });
      return response.data;
    } catch (error) {
      return { 
        success: false, 
        error: error instanceof Error ? error.message : 'Unknown error' 
      };
    }
  },

  // Send a custom message to the node
  sendMessage: async (nodeId: string, message: Partial<Message>): Promise<ApiResponse<Message>> => {
    try {
      const response = await api.post<ApiResponse<Message>>(`/node/${nodeId}/message`, message);
      return response.data;
    } catch (error) {
      return { 
        success: false, 
        error: error instanceof Error ? error.message : 'Unknown error' 
      };
    }
  },

  // Get message history for a node
  getMessageHistory: async (nodeId: string): Promise<ApiResponse<Message[]>> => {
    try {
      const response = await api.get<ApiResponse<Message[]>>(`/node/${nodeId}/messages`);
      return response.data;
    } catch (error) {
      return { 
        success: false, 
        error: error instanceof Error ? error.message : 'Unknown error' 
      };
    }
  }
};
