// HEADY_BRAND:BEGIN
// HEADY SYSTEMS :: SACRED GEOMETRY
// FILE: frontend/src/components/Layout.js
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

import React from 'react';
import './Layout.css';

const Layout = ({ sidebar, editor, cascade, bottom }) => {
  return (
    <div className="ide-layout">
      <div className="ide-header">
        <span>Heady Admin IDE</span>
        <div style={{marginLeft: 'auto'}}>
          {/* Settings button placeholder */}
        </div>
      </div>
      <div className="ide-body">
        <div className="ide-sidebar">{sidebar}</div>
        <div className="ide-main">
          <div className="ide-editor-area">{editor}</div>
          <div className="ide-bottom-panel">{bottom}</div>
        </div>
        <div className="ide-cascade">{cascade}</div>
      </div>
    </div>
  );
};

export default Layout;
