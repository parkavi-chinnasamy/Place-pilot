import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import { toast } from 'react-toastify';

export default function Register() {
  const { login } = useAuth();
  const navigate = useNavigate();
  const [form, setForm] = useState({ full_name: '', email: '', password: '', role: 'student' });
  const [loading, setLoading] = useState(false);
  const { authAPI } = require('../../services/api');

  const handle = async (e) => {
    e.preventDefault();
    if (form.password.length < 6) return toast.error('Password must be at least 6 characters');
    setLoading(true);
    try {
      const { default: API } = await import('../../services/api');
      await API.post('/api/auth/register', form);
      const data = await login(form.email, form.password);
      toast.success('Account created successfully!');
      navigate(data.role === 'student' ? '/dashboard' : '/admin/dashboard');
    } catch (err) {
      toast.error(err.response?.data?.detail || 'Registration failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ minHeight: '100vh', display: 'flex', alignItems: 'center', justifyContent: 'center', background: 'linear-gradient(135deg,#1e1b4b 0%,#0f0c29 100%)', padding: 20 }}>
      <div style={{ width: '100%', maxWidth: 440, background: 'white', borderRadius: 20, padding: '40px 36px', boxShadow: '0 25px 50px rgba(0,0,0,0.3)' }}>
        <div style={{ textAlign: 'center', marginBottom: 32 }}>
          <div style={{ width: 52, height: 52, background: 'linear-gradient(135deg,#818cf8,#4f46e5)', borderRadius: 14, display: 'flex', alignItems: 'center', justifyContent: 'center', fontWeight: 800, color: 'white', fontSize: 18, margin: '0 auto 16px' }}>PP</div>
          <h1 style={{ fontSize: 22, fontWeight: 800 }}>Create your account</h1>
          <p style={{ color: '#64748b', marginTop: 6, fontSize: 13 }}>Start your placement preparation journey</p>
        </div>
        <form onSubmit={handle}>
          {[
            { label: 'Full Name', key: 'full_name', type: 'text' },
            { label: 'Email', key: 'email', type: 'email' },
            { label: 'Password', key: 'password', type: 'password' },
          ].map(f => (
            <div key={f.key} style={{ marginBottom: 16 }}>
              <label style={{ display: 'block', fontSize: 13, fontWeight: 600, marginBottom: 6, color: '#374151' }}>{f.label}</label>
              <input type={f.type} value={form[f.key]} onChange={e => setForm({ ...form, [f.key]: e.target.value })} required
                style={{ width: '100%', padding: '10px 14px', border: '1.5px solid #e5e7eb', borderRadius: 8, fontSize: 14, outline: 'none' }}
                onFocus={e => e.target.style.borderColor = '#4f46e5'}
                onBlur={e => e.target.style.borderColor = '#e5e7eb'}
              />
            </div>
          ))}
          <div style={{ marginBottom: 20 }}>
            <label style={{ display: 'block', fontSize: 13, fontWeight: 600, marginBottom: 6, color: '#374151' }}>I am a</label>
            <div style={{ display: 'flex', gap: 10 }}>
              {['student', 'admin'].map(r => (
                <label key={r} style={{ flex: 1, display: 'flex', alignItems: 'center', gap: 8, padding: '10px 14px', border: `1.5px solid ${form.role === r ? '#4f46e5' : '#e5e7eb'}`, borderRadius: 8, cursor: 'pointer', background: form.role === r ? '#eef2ff' : 'white', fontSize: 13, fontWeight: 600 }}>
                  <input type="radio" name="role" value={r} checked={form.role === r} onChange={e => setForm({ ...form, role: e.target.value })} style={{ accentColor: '#4f46e5' }} />
                  {r === 'student' ? '👤 Student' : '🛡️ Placement Officer'}
                </label>
              ))}
            </div>
          </div>
          <button type="submit" disabled={loading} style={{ width: '100%', padding: '12px', background: '#4f46e5', color: 'white', border: 'none', borderRadius: 8, fontWeight: 700, fontSize: 14, cursor: loading ? 'not-allowed' : 'pointer', opacity: loading ? 0.7 : 1 }}>
            {loading ? 'Creating account…' : 'Create Account'}
          </button>
        </form>
        <p style={{ textAlign: 'center', marginTop: 24, fontSize: 13, color: '#64748b' }}>
          Already have an account? <Link to="/login" style={{ color: '#4f46e5', fontWeight: 600 }}>Sign in</Link>
        </p>
      </div>
    </div>
  );
}
