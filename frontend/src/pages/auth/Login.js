import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import { toast } from 'react-toastify';

export default function Login() {
  const { login } = useAuth();
  const navigate = useNavigate();
  const [form, setForm] = useState({ email: '', password: '' });
  const [loading, setLoading] = useState(false);

  const handle = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      const data = await login(form.email, form.password);
      toast.success(`Welcome back, ${data.full_name}!`);
      navigate(data.role === 'student' ? '/dashboard' : '/admin/dashboard');
    } catch (err) {
      toast.error(err.response?.data?.detail || 'Login failed');
    } finally {
      setLoading(false);
    }
  };

  const demoLogin = async (role) => {
    const creds = role === 'admin'
      ? { email: 'admin@placepilot.edu', password: 'Admin@123!' }
      : { email: 'ananya.sharma@demo.edu', password: 'Student@123!' };
    setForm(creds);
    setLoading(true);
    try {
      const data = await login(creds.email, creds.password);
      navigate(data.role === 'student' ? '/dashboard' : '/admin/dashboard');
    } catch {
      toast.error('Demo login failed — ensure backend is running');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ minHeight: '100vh', display: 'flex', alignItems: 'center', justifyContent: 'center', background: 'linear-gradient(135deg,#1e1b4b 0%,#0f0c29 100%)', padding: 20 }}>
      <div style={{ width: '100%', maxWidth: 420, background: 'white', borderRadius: 20, padding: '40px 36px', boxShadow: '0 25px 50px rgba(0,0,0,0.3)' }}>
        <div style={{ textAlign: 'center', marginBottom: 32 }}>
          <div style={{ width: 52, height: 52, background: 'linear-gradient(135deg,#818cf8,#4f46e5)', borderRadius: 14, display: 'flex', alignItems: 'center', justifyContent: 'center', fontWeight: 800, color: 'white', fontSize: 18, margin: '0 auto 16px' }}>PP</div>
          <h1 style={{ fontSize: 22, fontWeight: 800 }}>Sign in to PlacePilot</h1>
          <p style={{ color: '#64748b', marginTop: 6, fontSize: 13 }}>Enter your credentials to continue</p>
        </div>

        <form onSubmit={handle}>
          {[{ label: 'Email', key: 'email', type: 'email' }, { label: 'Password', key: 'password', type: 'password' }].map(f => (
            <div key={f.key} style={{ marginBottom: 16 }}>
              <label style={{ display: 'block', fontSize: 13, fontWeight: 600, marginBottom: 6, color: '#374151' }}>{f.label}</label>
              <input type={f.type} value={form[f.key]} onChange={e => setForm({ ...form, [f.key]: e.target.value })} required
                style={{ width: '100%', padding: '10px 14px', border: '1.5px solid #e5e7eb', borderRadius: 8, fontSize: 14, outline: 'none', transition: 'border 0.15s' }}
                onFocus={e => e.target.style.borderColor = '#4f46e5'}
                onBlur={e => e.target.style.borderColor = '#e5e7eb'}
              />
            </div>
          ))}
          <button type="submit" disabled={loading} style={{ width: '100%', padding: '12px', background: '#4f46e5', color: 'white', border: 'none', borderRadius: 8, fontWeight: 700, fontSize: 14, cursor: loading ? 'not-allowed' : 'pointer', opacity: loading ? 0.7 : 1, marginTop: 8 }}>
            {loading ? 'Signing in…' : 'Sign In'}
          </button>
        </form>

        <div style={{ textAlign: 'center', margin: '20px 0', color: '#9ca3af', fontSize: 13 }}>— or try a demo —</div>
        <div style={{ display: 'flex', gap: 8 }}>
          <button onClick={() => demoLogin('student')} style={{ flex: 1, padding: '9px', background: '#f1f5f9', border: '1px solid #e2e8f0', borderRadius: 8, fontWeight: 600, fontSize: 12, cursor: 'pointer' }}>
            👤 Demo Student
          </button>
          <button onClick={() => demoLogin('admin')} style={{ flex: 1, padding: '9px', background: '#f1f5f9', border: '1px solid #e2e8f0', borderRadius: 8, fontWeight: 600, fontSize: 12, cursor: 'pointer' }}>
            🛡️ Demo Admin
          </button>
        </div>

        <p style={{ textAlign: 'center', marginTop: 24, fontSize: 13, color: '#64748b' }}>
          New here? <Link to="/register" style={{ color: '#4f46e5', fontWeight: 600 }}>Create an account</Link>
        </p>
      </div>
    </div>
  );
}
