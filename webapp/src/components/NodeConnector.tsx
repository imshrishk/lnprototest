import React, { useState } from 'react';
import {
  SpaceBetween,
  FormField,
  Input,
  Box
} from '@cloudscape-design/components';

interface NodeConnectorProps {
  onConnect: (nodeId: string, host: string, port: number) => void;
  selectedNodeId?: string;
}

const NodeConnector: React.FC<NodeConnectorProps> = ({ onConnect, selectedNodeId }) => {
  const [host, setHost] = useState('localhost');
  const [port, setPort] = useState('9735');

  // Handle form submission
  const handleSubmit = () => {
    if (!selectedNodeId) return;
    onConnect(selectedNodeId, host, parseInt(port, 10));
  };

  return (
    <Box>
      <SpaceBetween size="l">
        <FormField
          label="Host"
          description="The hostname or IP address of the Lightning node"
        >
          <Input
            value={host}
            onChange={event => setHost(event.detail.value)}
            placeholder="localhost"
          />
        </FormField>

        <FormField
          label="Port"
          description="The port number of the Lightning node"
        >
          <Input
            value={port}
            onChange={event => setPort(event.detail.value)}
            placeholder="9735"
            type="number"
          />
        </FormField>
      </SpaceBetween>
    </Box>
  );
};

export default NodeConnector;
