import React from 'react';
import { Routes, Route } from 'react-router-dom';
import { AppLayout, ContentLayout, Header } from '@cloudscape-design/components';
import MessageFlowVisualizer from './components/MessageFlowVisualizer';
import Navigation from './components/Navigation';

const App: React.FC = () => {
  return (
    <div className="app-container">
      <AppLayout
        content={
          <ContentLayout
            header={
              <Header
                variant="h1"
                description="Visualize and interact with Lightning Network protocol messages"
              >
                LNPrototest Message Flow Visualizer
              </Header>
            }
          >
            <Routes>
              <Route path="/" element={<MessageFlowVisualizer />} />
            </Routes>
          </ContentLayout>
        }
        navigation={<Navigation />}
        toolsHide
      />
    </div>
  );
};

export default App;
