import React, { useState, useEffect } from 'react';
import { studentAPI, jobRolesAPI } from '../../services/api';
import { Card, PageHeader, Btn, LoadingSpinner, ProgressBar } from '../../components/common/Card';
import { toast } from 'react-toastify';
import { FiEdit, FiSave, FiX } from 'react-icons/fi';

export default function Profile() {
  const [profile, setProfile] = useState(null);
  const [roles, setRoles] = useState([]);
  const [editing, setEditing] = useState(false);
  const [form, setForm] = useState({});
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);

  useEffect(() => {
    Promise.all([studentAPI.getProfile(), jobRolesAPI.list()])
      .then(([p, r]) => { setProfile(p.data); setForm(p.data); setRoles(r.data); })
      .catch(() => toast.error('Failed to load profile'))
      .finally(() => setLoading(false));
  }, []);

  const save = async () => {
    setSaving(true);
    try {
      await studentAPI.updateProfile(form);
      setProfile(form);
      setEditing(false);
      toast.success('Profile updated!');
    } catch { toast.error('Save failed'); }
    finally { setSaving(false); }
  };

  const field = (label, key, type = 'text', opts = {}) => (
    <div style={{ marginBottom: 16 }}>
      <label style={{ display: 'block', fontSize: 12, fontWeight: 600, color: '#64748b', marginBottom: 4, textTransform: 'uppercase', letterSpacing: '0.04em' }}>{label}</label>
      {editing ? (
        type === 'select' ? (
          <select value={form[key] || ''} onChange={e => setForm({ ...form, [key]: e.target.value })}
            style={{ width: '100%', padding: '9px 12px', border: '1.5px solid #e2e8f0', borderRadius: 8, fontSize: 13, background: 'white' }}>
            <option value="">Select…</option>
            {opts.options?.map(o => <option key={o.value} value={o.value}>{o.label}</option>)}
          </select>
        ) : (
          <input type={type} value={form[key] || ''} onChange={e => setForm({ ...form, [key]: e.target.value })}
            style={{ width: '100%', padding: '9px 12px', border: '1.5px solid #e2e8f0', borderRadius: 8, fontSize: 13 }} />
        )
      ) : (
        <div style={{ padding: '9px 12px', background: '#f8fafc', borderRadius: 8, fontSize: 13, color: form[key] ? '#1e293b' : '#94a3b8', border: '1px solid #f1f5f9' }}>
          {form[key] != null && form[key] !== '' ? String(form[key]) : '—'}
        </div>
      )}
    </div>
  );

  const skillField = (label, key) => (
    <div style={{ marginBottom: 14 }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 6 }}>
        <span style={{ fontSize: 13, fontWeight: 600 }}>{label}</span>
        <span style={{ fontSize: 13, fontWeight: 700, color: '#4f46e5' }}>{form[key] || 0}/100</span>
      </div>
      {editing ? (
        <input type="range" min="0" max="100" value={form[key] || 0} onChange={e => setForm({ ...form, [key]: parseInt(e.target.value) })}
          style={{ width: '100%', accentColor: '#4f46e5' }} />
      ) : (
        <ProgressBar value={form[key] || 0} color={form[key] >= 70 ? '#10b981' : form[key] >= 50 ? '#f59e0b' : '#ef4444'} showLabel={false} />
      )}
    </div>
  );

  if (loading) return <LoadingSpinner />;

  return (
    <div>
      <PageHeader title="My Profile" subtitle="Your academic and skill information"
        action={
          editing
            ? <div style={{ display: 'flex', gap: 8 }}><Btn onClick={() => setEditing(false)} variant="secondary"><FiX /> Cancel</Btn><Btn onClick={save} disabled={saving}><FiSave /> {saving ? 'Saving…' : 'Save'}</Btn></div>
            : <Btn onClick={() => setEditing(true)}><FiEdit /> Edit Profile</Btn>
        }
      />

      {/* Completeness */}
      <Card style={{ marginBottom: 20 }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: 16 }}>
          <div>
            <div style={{ fontSize: 13, fontWeight: 600, marginBottom: 6 }}>Profile Completeness</div>
            <ProgressBar value={profile?.profile_completeness || 0} />
          </div>
          <div style={{ fontSize: 32, fontWeight: 800, color: '#4f46e5', flexShrink: 0 }}>{profile?.profile_completeness || 0}%</div>
        </div>
      </Card>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 20 }}>
        <Card>
          <h3 style={{ fontWeight: 700, marginBottom: 20, fontSize: 15 }}>Personal Information</h3>
          {field('Full Name', 'full_name')}
          {field('Email', 'email', 'email')}
          {field('Phone', 'phone', 'tel')}
          {field('College', 'college')}
          {field('Department', 'department')}
          {field('Batch', 'batch')}
          {field('Year', 'year', 'number')}
          <div style={{ marginBottom: 16 }}>
            <label style={{ display: 'block', fontSize: 12, fontWeight: 600, color: '#64748b', marginBottom: 4, textTransform: 'uppercase', letterSpacing: '0.04em' }}>Target Role</label>
            {editing ? (
              <select value={form.target_role_id || ''} onChange={e => setForm({ ...form, target_role_id: e.target.value })}
                style={{ width: '100%', padding: '9px 12px', border: '1.5px solid #e2e8f0', borderRadius: 8, fontSize: 13, background: 'white' }}>
                <option value="">Select target role…</option>
                {roles.map(r => <option key={r.id} value={r.id}>{r.name}</option>)}
              </select>
            ) : (
              <div style={{ padding: '9px 12px', background: '#f8fafc', borderRadius: 8, fontSize: 13 }}>
                {roles.find(r => r.id === form.target_role_id)?.name || '—'}
              </div>
            )}
          </div>
        </Card>

        <div style={{ display: 'flex', flexDirection: 'column', gap: 20 }}>
          <Card>
            <h3 style={{ fontWeight: 700, marginBottom: 20, fontSize: 15 }}>Academic Performance</h3>
            {field('CGPA', 'cgpa', 'number')}
            {field('10th %', 'tenth_percent', 'number')}
            {field('12th %', 'twelfth_percent', 'number')}
          </Card>

          <Card>
            <h3 style={{ fontWeight: 700, marginBottom: 20, fontSize: 15 }}>Skill Self-Assessment</h3>
            <p style={{ fontSize: 12, color: '#94a3b8', marginBottom: 16 }}>These are your self-assessed scores. Actual scores are calculated from tests.</p>
            {skillField('Programming', 'skill_programming')}
            {skillField('DSA', 'skill_dsa')}
            {skillField('DBMS', 'skill_dbms')}
            {skillField('OOP', 'skill_oop')}
            {skillField('Web Development', 'skill_web_dev')}
            {skillField('AI/ML', 'skill_aiml')}
            {skillField('Communication', 'skill_communication')}
          </Card>
        </div>
      </div>
    </div>
  );
}
