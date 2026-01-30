import React, { useState, useEffect } from 'react';
import axios from 'axios';

const SettingsModal = ({ onClose }) => {
  const [settings, setSettings] = useState(null);
  const [loading, setLoading] = useState(true);

  const token = localStorage.getItem('admin_token') || 'default_insecure_token';

  useEffect(() => {
    axios.get('/api/settings', { headers: { 'X-Admin-Token': token } })
      .then(res => {
        setSettings(res.data);
        setLoading(false);
      })
      .catch(err => {
        console.error(err);
        setLoading(false);
      });
  }, [token]);

  const handleChange = (section, field, value) => {
    setSettings(prev => ({
      ...prev,
      [section]: {
        ...prev[section],
        [field]: value
      }
    }));
  };

  const handleSave = async () => {
    try {
      await axios.post('/api/settings', settings, { headers: { 'X-Admin-Token': token } });
      onClose();
    } catch (err) {
      alert("Failed to save settings");
    }
  };

  if (loading) return <div>Loading...</div>;

  return (
    <div style={{
      position: 'fixed', top: 0, left: 0, right: 0, bottom: 0,
      backgroundColor: 'rgba(0,0,0,0.5)', display: 'flex', alignItems: 'center', justifyContent: 'center', zIndex: 1000
    }}>
      <div style={{ backgroundColor: '#252526', padding: '20px', borderRadius: '5px', width: '400px', color: '#ccc' }}>
        <h3 style={{ marginTop: 0 }}>Settings</h3>

        <div style={{ marginBottom: '15px', borderBottom: '1px solid #444', paddingBottom: '10px' }}>
            <h4 style={{ marginBottom: '10px', color: '#4ec9b0' }}>Remote GPU</h4>
            <label style={{ display: 'block', marginBottom: '5px' }}>
                <input
                    type="checkbox"
                    checked={settings?.remote_gpu?.enabled || false}
                    onChange={e => handleChange('remote_gpu', 'enabled', e.target.checked)}
                /> Enable Remote GPU
            </label>
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '10px' }}>
                <label>
                    Host:
                    <input
                        type="text"
                        value={settings?.remote_gpu?.host || ''}
                        onChange={e => handleChange('remote_gpu', 'host', e.target.value)}
                        style={{ width: '100%', backgroundColor: '#333', color: '#fff', border: '1px solid #555' }}
                    />
                </label>
                <label>
                    Port:
                    <input
                        type="number"
                        value={settings?.remote_gpu?.port || 8000}
                        onChange={e => handleChange('remote_gpu', 'port', parseInt(e.target.value))}
                        style={{ width: '100%', backgroundColor: '#333', color: '#fff', border: '1px solid #555' }}
                    />
                </label>
            </div>
             <label style={{ display: 'block', marginTop: '5px' }}>
                <input
                    type="checkbox"
                    checked={settings?.remote_gpu?.use_rdma || false}
                    onChange={e => handleChange('remote_gpu', 'use_rdma', e.target.checked)}
                /> Use GPUDirect RDMA
            </label>
        </div>

        <div style={{ marginBottom: '15px' }}>
            <h4 style={{ marginBottom: '10px', color: '#ce9178' }}>AI Model Selection</h4>
            <label style={{ display: 'block' }}>
                Model:
                <select
                    value={settings?.ai_model?.selected_model || 'distilgpt2'}
                    onChange={e => handleChange('ai_model', 'selected_model', e.target.value)}
                    style={{ width: '100%', backgroundColor: '#333', color: '#fff', border: '1px solid #555', padding: '5px' }}
                >
                    <option value="distilgpt2">DistilGPT2 (Local / CPU Fast)</option>
                    <option value="gpt2-medium">GPT2 Medium (Local / GPU)</option>
                    <option value="gemini-pro">Google Gemini Pro (Cloud)</option>
                </select>
            </label>
        </div>

        <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '10px' }}>
            <button onClick={onClose} style={{ padding: '5px 10px', backgroundColor: '#555', color: '#fff', border: 'none', cursor: 'pointer' }}>Cancel</button>
            <button onClick={handleSave} style={{ padding: '5px 10px', backgroundColor: '#007acc', color: '#fff', border: 'none', cursor: 'pointer' }}>Save</button>
        </div>
      </div>
    </div>
  );
};

export default SettingsModal;
