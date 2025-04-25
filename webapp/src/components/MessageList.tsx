import React from 'react';
import { 
  Table, 
  Box, 
  StatusIndicator
} from '@cloudscape-design/components';
import { Message } from '../types';

interface MessageListProps {
  messages: Message[];
}

const MessageList: React.FC<MessageListProps> = ({ messages }) => {
  // Format timestamp to readable date/time
  const formatTime = (timestamp: number): string => {
    return new Date(timestamp).toLocaleTimeString();
  };

  // Get status indicator based on message status
  const getStatusIndicator = (status: string): React.ReactNode => {
    switch (status) {
      case 'sent':
        return <StatusIndicator type="success">Sent</StatusIndicator>;
      case 'received':
        return <StatusIndicator type="info">Received</StatusIndicator>;
      case 'error':
        return <StatusIndicator type="error">Error</StatusIndicator>;
      default:
        return <StatusIndicator type="pending">Unknown</StatusIndicator>;
    }
  };

  // Format message content for display
  const formatContent = (content: Record<string, any>): string => {
    return JSON.stringify(content, null, 2);
  };

  // Get direction indicator
  const getDirection = (message: Message): string => {
    return `${message.sender} → ${message.receiver}`;
  };
  
  return (
    <Box>
      {messages.length === 0 ? (
        <Box textAlign="center" padding="l">
          No messages to display. Connect to a node and run a test sequence to see messages.
        </Box>
      ) : (
        <Table
          columnDefinitions={[
            {
              id: 'time',
              header: 'Time',
              cell: (item: Message) => formatTime(item.timestamp),
              sortingField: 'timestamp',
              width: 100,
            },
            {
              id: 'type',
              header: 'Type',
              cell: (item: Message) => item.type,
              sortingField: 'type',
              width: 120,
            },
            {
              id: 'direction',
              header: 'Direction',
              cell: (item: Message) => getDirection(item),
              width: 200,
            },
            {
              id: 'status',
              header: 'Status',
              cell: (item: Message) => getStatusIndicator(item.status),
              width: 100,
            },
            {
              id: 'content',
              header: 'Content',
              cell: (item: Message) => (
                <Box>
                  <span style={{ whiteSpace: 'pre-wrap', fontFamily: 'monospace' }}>
                    {formatContent(item.content)}
                  </span>
                </Box>
              ),
            },
          ]}
          items={messages}
          loadingText="Loading messages"
          empty={
            <Box textAlign="center" padding="l">
              <span style={{ fontWeight: 'bold' }}>No messages</span>
              <Box padding={{ top: 's' }}>
                No messages to display. Connect to a node and run a test sequence.
              </Box>
            </Box>
          }
          header={
            <Box>Message History</Box>
          }
          sortingDisabled
        />
      )}
    </Box>
  );
};

export default MessageList;
