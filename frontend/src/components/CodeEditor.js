// HEADY_BRAND:BEGIN
// HEADY SYSTEMS :: SACRED GEOMETRY
// FILE: frontend/src/components/CodeEditor.js
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

import React, { useRef } from 'react';
import Editor from '@monaco-editor/react';

const CodeEditor = ({ code, language, onChange, onSave, filename }) => {
  const editorRef = useRef(null);

  const handleEditorDidMount = (editor, monaco) => {
    editorRef.current = editor;

    // Ctrl+S to save
    editor.addCommand(monaco.KeyMod.CtrlCmd | monaco.KeyCode.KeyS, () => {
      if (onSave) onSave();
    });
  };

  return (
    <div style={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
        {filename && (
            <div style={{
                padding: '5px 10px',
                backgroundColor: '#1e1e1e',
                color: '#fff',
                fontSize: '12px',
                borderBottom: '1px solid #333'
            }}>
                {filename}
            </div>
        )}
        <div style={{ flex: 1 }}>
            <Editor
            height="100%"
            theme="vs-dark"
            path={filename}
            defaultLanguage={language || 'plaintext'}
            value={code}
            onChange={onChange}
            onMount={handleEditorDidMount}
            options={{
                minimap: { enabled: true },
                automaticLayout: true,
                fontSize: 14,
            }}
            />
        </div>
    </div>
  );
};

export default CodeEditor;
