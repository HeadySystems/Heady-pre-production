import React, { useState } from 'react';
import axios from 'axios';
import Layout from './components/Layout';
import FileTree from './components/FileTree';
import CodeEditor from './components/CodeEditor';
import CascadePanel from './components/CascadePanel';
import TerminalComponent from './components/Terminal';
import SettingsModal from './components/SettingsModal';

function App() {
  const [currentFile, setCurrentFile] = useState(null); // { path, content }
  const [showSettings, setShowSettings] = useState(false);
  const [language, setLanguage] = useState('plaintext');
  const [notification, setNotification] = useState(null); // { type: 'success'|'error', message: string }

  const token = localStorage.getItem('admin_token') || 'default_insecure_token';

  const showNotification = (type, message) => {
    setNotification({ type, message });
    setTimeout(() => setNotification(null), 3000);
  };

  const handleFileSelect = async (path) => {
    try {
      const res = await axios.get(`/api/files/${path}`, {
         headers: { 'X-Admin-Token': token }
      });
      setCurrentFile({ path, content: res.data.content });

      // Guess language
      const ext = path.split('.').pop();
      const langMap = {
        'js': 'javascript', 'py': 'python', 'json': 'json', 'html': 'html', 'css': 'css', 'md': 'markdown'
      };
      setLanguage(langMap[ext] || 'plaintext');
    } catch (err) {
      console.error("Failed to load file", err);
      const errorMsg = err.response?.data?.detail || err.message || "Failed to load file";
      showNotification('error', `Error loading file: ${errorMsg}`);
    }
  };

  const handleCodeChange = (value) => {
    if (currentFile) {
        setCurrentFile({ ...currentFile, content: value });
    }
  };

  const handleSave = async () => {
    if (!currentFile) return;
    try {
        await axios.post('/api/files', {
            path: currentFile.path,
            content: currentFile.content
        }, { headers: { 'X-Admin-Token': token } });
        showNotification('success', `Saved ${currentFile.path}`);
    } catch (err) {
        console.error("Failed to save", err);
        const errorMsg = err.response?.data?.detail || err.message || "Failed to save file";
        showNotification('error', `Error saving file: ${errorMsg}`);
    }
  };

  return (
    <div className="App">
      <Layout
        sidebar={<FileTree onFileSelect={handleFileSelect} />}
        editor={
            currentFile ? (
                <CodeEditor
                    code={currentFile.content}
                    language={language}
                    onChange={handleCodeChange}
                    onSave={handleSave}
                    filename={currentFile.path}
                />
            ) : (
                <div style={{ padding: '20px', color: '#555' }}>Select a file to edit</div>
            )
        }
        cascade={<CascadePanel contextFile={currentFile} />}
        bottom={<TerminalComponent />}
      />

      {/* Settings Button in Header (using portal or absolute) */}
      <div style={{ position: 'absolute', top: '5px', right: '10px', zIndex: 100 }}>
         <button
            onClick={() => setShowSettings(true)}
            style={{ background: 'transparent', border: 'none', color: '#888', cursor: 'pointer', fontSize: '14px' }}
         >
            ⚙️ Settings
         </button>
      </div>

      {showSettings && <SettingsModal onClose={() => setShowSettings(false)} />}

      {/* Notification Toast */}
      {notification && (
        <div style={{
          position: 'fixed',
          top: '20px',
          right: '20px',
          padding: '12px 20px',
          borderRadius: '4px',
          backgroundColor: notification.type === 'success' ? '#4caf50' : '#f44336',
          color: 'white',
          zIndex: 1001,
          boxShadow: '0 2px 8px rgba(0,0,0,0.3)',
          maxWidth: '400px',
          animation: 'slideIn 0.3s ease-out'
        }}>
          {notification.message}
        </div>
      )}
    </div>
  );
}

export default App;
