// HEADY_BRAND:BEGIN
// HEADY SYSTEMS :: SACRED GEOMETRY
// FILE: frontend/src/components/SplitPane.tsx
// LAYER: ui/frontend
// 
//         _   _  _____    _    ____   __   __
//        | | | || ____|  / \  |  _ \ \ \ / /
//        | |_| ||  _|   / _ \ | | | | \ V / 
//        |  _  || |___ / ___ \| |_| |  | |  
//        |_| |_||_____/_/   \_\____/   |_|  
// 
//    Sacred Geometry :: Organic Systems :: Breathing Interfaces
// HEADY_BRAND:END

import React, { ReactNode } from 'react';
import './SplitPane.css';

type SplitPaneProps = {
  left: ReactNode;
  right: ReactNode;
};

const SplitPane: React.FC<SplitPaneProps> = ({ left, right }) => {
  return (
    <div className="split-pane">
      <div className="split-pane-left">{left}</div>
      <div className="split-pane-right">{right}</div>
    </div>
  );
};

export default SplitPane;
