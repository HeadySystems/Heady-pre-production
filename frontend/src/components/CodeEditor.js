import React, { useRef, useState } from 'react';
import Editor from '@monaco-editor/react';

const CodeEditor = ({ code, language, onChange, onSave, filename }) => {
  const editorRef = useRef(null);
  const [showPreview, setShowPreview] = useState(false);

  const handleEditorDidMount = (editor, monaco) => {
    editorRef.current = editor;

    // Ctrl+S to save
    editor.addCommand(monaco.KeyMod.CtrlCmd | monaco.KeyCode.KeyS, () => {
      if (onSave) onSave();
    });
  };

  const isHtml = filename && (filename.endsWith('.html') || filename.endsWith('.htm'));

  return (
    <div style={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
        {filename && (
            <div style={{
                padding: '5px 10px',
                backgroundColor: '#1e1e1e',
                color: '#fff',
                fontSize: '12px',
                borderBottom: '1px solid #333',
                display: 'flex',
                justifyContent: 'space-between',
                alignItems: 'center'
            }}>
                <span>{filename}</span>
                {isHtml && (
                    <button
                        onClick={() => setShowPreview(!showPreview)}
                        style={{
                            background: showPreview ? '#007acc' : '#333',
                            color: 'white',
                            border: '1px solid #555',
                            cursor: 'pointer',
                            fontSize: '11px',
                            padding: '2px 5px'
                        }}
                    >
                        {showPreview ? "Edit" : "Preview"}
                    </button>
                )}
            </div>
        )}
        <div style={{ flex: 1, position: 'relative' }}>
            {showPreview && isHtml ? (
                <iframe
                    title="preview"
                    srcDoc={code}
                    style={{ width: '100%', height: '100%', border: 'none', background: 'white' }}
                    sandbox="allow-scripts"
                />
            ) : (
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
            )}
        </div>
    </div>
  );
};

export default CodeEditor;
