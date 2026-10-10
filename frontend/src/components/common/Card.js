import React from 'react';

export function Card({ children, className = '', style = {} }) {
  return (
    <div style={{ background: 'var(--bg-card)', borderRadius: 'var(--radius)', border: '1px solid var(--border)', boxShadow: 'var(--shadow)', padding: '20px', ...style }} className={className}>
      {children}
    </div>
  );
}

export function StatCard({ icon, label, value, color = '#4f46e5', sub }) {
  return (
    <div style={{ background: 'white', borderRadius: 'var(--radius)', border: '1px solid var(--border)', padding: '20px', display: 'flex', alignItems: 'flex-start', gap: '16px', boxShadow: 'var(--shadow)' }}>
      <div style={{ width: 48, height: 48, borderRadius: 12, background: `${color}18`, display: 'flex', alignItems: 'center', justifyContent: 'center', color, fontSize: 22, flexShrink: 0 }}>{icon}</div>
      <div>
        <div style={{ fontSize: 13, color: 'var(--text-muted)', marginBottom: 4 }}>{label}</div>
        <div style={{ fontSize: 24, fontWeight: 700, color: 'var(--text)' }}>{value}</div>
        {sub && <div style={{ fontSize: 12, color: 'var(--text-light)', marginTop: 2 }}>{sub}</div>}
      </div>
    </div>
  );
}

export function Badge({ label, type = 'default' }) {
  const colors = {
    success: { bg: '#d1fae5', color: '#065f46' },
    warning: { bg: '#fef3c7', color: '#92400e' },
    danger: { bg: '#fee2e2', color: '#991b1b' },
    info: { bg: '#dbeafe', color: '#1e40af' },
    default: { bg: '#f1f5f9', color: '#475569' },
  };
  const c = colors[type] || colors.default;
  return (
    <span style={{ background: c.bg, color: c.color, padding: '2px 10px', borderRadius: 20, fontSize: 12, fontWeight: 600 }}>{label}</span>
  );
}

export function LoadingSpinner({ size = 32 }) {
  return (
    <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', padding: 40 }}>
      <div style={{ width: size, height: size, border: '3px solid var(--border)', borderTopColor: 'var(--primary)', borderRadius: '50%', animation: 'spin 0.8s linear infinite' }} />
      <style>{`@keyframes spin { to { transform: rotate(360deg); } }`}</style>
    </div>
  );
}

export function ProgressBar({ value, max = 100, color = '#4f46e5', height = 8, showLabel = true }) {
  const pct = Math.min(100, Math.max(0, (value / max) * 100));
  return (
    <div>
      <div style={{ background: '#f1f5f9', borderRadius: 9999, height, overflow: 'hidden' }}>
        <div style={{ width: `${pct}%`, height: '100%', background: color, borderRadius: 9999, transition: 'width 0.4s ease' }} />
      </div>
      {showLabel && <div style={{ textAlign: 'right', fontSize: 11, color: 'var(--text-muted)', marginTop: 3 }}>{Math.round(pct)}%</div>}
    </div>
  );
}

export function PageHeader({ title, subtitle, action }) {
  return (
    <div style={{ marginBottom: 24, display: 'flex', alignItems: 'flex-start', justifyContent: 'space-between', flexWrap: 'wrap', gap: 12 }}>
      <div>
        <h1 style={{ fontSize: 22, fontWeight: 700, color: 'var(--text)', marginBottom: 4 }}>{title}</h1>
        {subtitle && <p style={{ color: 'var(--text-muted)', fontSize: 14 }}>{subtitle}</p>}
      </div>
      {action && <div>{action}</div>}
    </div>
  );
}

export function EmptyState({ icon, title, description, action }) {
  return (
    <div style={{ textAlign: 'center', padding: '60px 20px', color: 'var(--text-muted)' }}>
      {icon && <div style={{ fontSize: 48, marginBottom: 16, opacity: 0.4 }}>{icon}</div>}
      <h3 style={{ fontSize: 16, fontWeight: 600, marginBottom: 8, color: 'var(--text)' }}>{title}</h3>
      {description && <p style={{ fontSize: 13, marginBottom: action ? 20 : 0 }}>{description}</p>}
      {action}
    </div>
  );
}

export function Btn({ children, onClick, variant = 'primary', size = 'md', disabled = false, type = 'button', style = {} }) {
  const variants = {
    primary: { background: 'var(--primary)', color: 'white', border: 'none' },
    secondary: { background: 'white', color: 'var(--text)', border: '1px solid var(--border)' },
    success: { background: 'var(--success)', color: 'white', border: 'none' },
    danger: { background: 'var(--danger)', color: 'white', border: 'none' },
    outline: { background: 'transparent', color: 'var(--primary)', border: '1.5px solid var(--primary)' },
  };
  const sizes = { sm: { padding: '6px 14px', fontSize: 12 }, md: { padding: '9px 20px', fontSize: 13 }, lg: { padding: '12px 28px', fontSize: 15 } };
  const v = variants[variant] || variants.primary;
  const s = sizes[size] || sizes.md;
  return (
    <button type={type} onClick={onClick} disabled={disabled} style={{ ...v, ...s, borderRadius: 8, fontWeight: 600, cursor: disabled ? 'not-allowed' : 'pointer', opacity: disabled ? 0.6 : 1, display: 'inline-flex', alignItems: 'center', gap: 6, transition: 'all 0.15s', ...style }}>
      {children}
    </button>
  );
}

export function DemoBanner({ message }) {
  return (
    <div style={{ background: '#fef3c7', border: '1px solid #fcd34d', borderRadius: 8, padding: '10px 16px', fontSize: 12, color: '#92400e', display: 'flex', alignItems: 'center', gap: 8, marginBottom: 16 }}>
      <span>⚠️</span>
      <span>{message || 'Demo Data – This is prototype/synthetic data for demonstration purposes only.'}</span>
    </div>
  );
}
