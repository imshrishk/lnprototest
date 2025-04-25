import React from 'react';
import { SideNavigation } from '@cloudscape-design/components';
import { useNavigate } from 'react-router-dom';

const Navigation: React.FC = () => {
  const navigate = useNavigate();

  return (
    <SideNavigation
      header={{ text: 'LNPrototest', href: '/' }}
      onFollow={e => {
        e.preventDefault();
        navigate(e.detail.href);
      }}
      items={[
        {
          type: 'link',
          text: 'Message Flow Visualizer',
          href: '/'
        },
        {
          type: 'section',
          text: 'BOLT #1 Messages',
          items: [
            {
              type: 'link',
              text: 'Init Messages',
              href: '/bolt1/init'
            }
          ]
        }
      ]}
    />
  );
};

export default Navigation;
