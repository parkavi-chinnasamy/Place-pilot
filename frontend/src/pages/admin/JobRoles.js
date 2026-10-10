import React, { useState, useEffect } from 'react';
import { jobRolesAPI } from '../../services/api';
import { Card, PageHeader, LoadingSpinner, Btn, DemoBanner } from '../../components/common/Card';
import { toast } from 'react-toastify';
import { FiEdit, FiChevronDown, FiChevronUp } from 'react-icons/fi';

export default function JobRoles() {
  const [roles, setRoles] = useState([]);
  const [loading, setLoading] = useState(true);
  const [expanded, setExpanded] = useState(null);
  const [editing, setEditing] = useState(null);
  const [editForm, setEditForm] = useState({});
  const [saving, setSaving] = useState(false);
  const [showNew, setShowNew] = useState(false);
  const [newForm, setNewForm] = useState({ name: '', description: '', requirements: [] });

  const load = () => { jobRolesAPI.list().then(r => setRoles(r.data)).finally(() => setLoading(false)); };
  useEffect(() => { load(); }, []);

  const startEdit = (r) => { setEditing(r.id); setEditForm({ name: r.name, description: r.description || '', requirements: r.requirements || [] }); };

  const saveEdit = async () => {
    setSaving(true);
    try {
      await jobRolesAPI.update(editing, editForm);
      toast.success('Role updated!');
      setEditing(null);
      load();
    } catch { toast.error('Update failed'); }
    finally { setSaving(false); }
  };

  const updateReq = (reqs, i, field, val) => {
    const updated = [...reqs];
    updated[i] = { ...updated[i], [field]: field === 'required_score' ? parseInt(val) || 0 : val };
    return updated;
  };

  return (
    <div>
      <DemoBanner />
      <PageHeader title="Job Role Management" subtitle="Configure skill requirements for each role"
        action={<Btn onClick={() => setShowNew(!showNew)}>+ New Role</Btn>}
      />

      {showNew && (
        <Card style={{ marginBottom: 20, border: '2px solid #4f46e5' }}>
          <h3 style={{ fontWeight: 700, marginBottom: 16 }}>Create New Role</h3>
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 12, marginBottom: 16 }}>
            <div><label style={{ fontSize: 12, fontWeight: 600, color: '#64748b', display: 'block', marginBottom: 4 }}>ROLE NAME</label>
              <input value={newForm.name} onChange={e => setNewForm({ ...newForm, name: e.target.value })}
                style={{ width: '100%', padding: '9px 12px', border: '1.5px solid #e2e8f0', borderRadius: 8, fontSize: 13 }} /></div>
            <div><label style={{ fontSize: 12, fontWeight: 600, color: '#64748b', display: 'block', marginBottom: 4 }}>DESCRIPTION</label>
              <input value={newForm.description} onChange={e => setNewForm({ ...newForm, description: e.target.value })}
                style={{ width: '100%', padding: '9px 12px', border: '1.5px solid #e2e8f0', borderRadius: 8, fontSize: 13 }} /></div>
          </div>
          <div style={{ display: 'flex', gap: 8 }}>
            <Btn onClick={async () => { try { await jobRolesAPI.create(newForm); toast.success('Role created!'); setShowNew(false); setNewForm({ name:'',description:'',requirements:[] }); load(); } catch { toast.error('Failed'); } }}>Create</Btn>
            <Btn variant="secondary" onClick={() => setShowNew(false)}>Cancel</Btn>
          </div>
        </Card>
      )}

      {loading ? <LoadingSpinner /> : (
        <div style={{ display: 'flex', flexDirection: 'column', gap: 12 }}>
          {roles.map(role => (
            <Card key={role.id}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <div>
                  <h3 style={{ fontWeight: 700, fontSize: 15 }}>{role.name}</h3>
                  <p style={{ color: '#64748b', fontSize: 13, marginTop: 4 }}>{role.description}</p>
                  <div style={{ marginTop: 6, fontSize: 12, color: '#94a3b8' }}>{role.requirements?.length} skill requirements</div>
                </div>
                <div style={{ display: 'flex', gap: 8 }}>
                  <Btn variant="secondary" size="sm" onClick={() => startEdit(role)}><FiEdit /> Edit</Btn>
                  <button onClick={() => setExpanded(expanded === role.id ? null : role.id)}
                    style={{ padding: '6px 12px', border: '1px solid #e2e8f0', borderRadius: 8, background: 'white', cursor: 'pointer', fontSize: 12, display: 'flex', alignItems: 'center', gap: 4 }}>
                    Requirements {expanded === role.id ? <FiChevronUp /> : <FiChevronDown />}
                  </button>
                </div>
              </div>

              {editing === role.id && (
                <div style={{ marginTop: 16, padding: 16, background: '#f8fafc', borderRadius: 10 }}>
                  <h4 style={{ fontWeight: 700, marginBottom: 12 }}>Edit Requirements</h4>
                  {editForm.requirements?.map((req, i) => (
                    <div key={i} style={{ display: 'flex', gap: 10, marginBottom: 8, alignItems: 'center' }}>
                      <input value={req.skill_name} onChange={e => setEditForm({ ...editForm, requirements: updateReq(editForm.requirements, i, 'skill_name', e.target.value) })}
                        style={{ flex: 1, padding: '7px 10px', border: '1px solid #e2e8f0', borderRadius: 6, fontSize: 12 }} />
                      <input type="number" min="0" max="100" value={req.required_score} onChange={e => setEditForm({ ...editForm, requirements: updateReq(editForm.requirements, i, 'required_score', e.target.value) })}
                        style={{ width: 70, padding: '7px 10px', border: '1px solid #e2e8f0', borderRadius: 6, fontSize: 12, textAlign: 'center' }} />
                      <button onClick={() => setEditForm({ ...editForm, requirements: editForm.requirements.filter((_, j) => j !== i) })}
                        style={{ color: '#ef4444', background: 'none', border: 'none', cursor: 'pointer', fontWeight: 700, fontSize: 14 }}>✕</button>
                    </div>
                  ))}
                  <button onClick={() => setEditForm({ ...editForm, requirements: [...editForm.requirements, { skill_name: '', required_score: 70, weight: 1.0 }] })}
                    style={{ fontSize: 12, color: '#4f46e5', background: 'none', border: 'none', cursor: 'pointer', marginBottom: 12 }}>+ Add Skill</button>
                  <div style={{ display: 'flex', gap: 8 }}>
                    <Btn onClick={saveEdit} disabled={saving}>{saving ? 'Saving…' : 'Save'}</Btn>
                    <Btn variant="secondary" onClick={() => setEditing(null)}>Cancel</Btn>
                  </div>
                </div>
              )}

              {expanded === role.id && !editing && (
                <div style={{ marginTop: 16 }}>
                  <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill,minmax(180px,1fr))', gap: 10 }}>
                    {role.requirements?.map((req, i) => (
                      <div key={i} style={{ background: '#f8fafc', borderRadius: 8, padding: '10px 14px', border: '1px solid #e2e8f0' }}>
                        <div style={{ fontWeight: 700, fontSize: 12, textTransform: 'uppercase' }}>{req.skill_name}</div>
                        <div style={{ fontSize: 22, fontWeight: 800, color: '#4f46e5', marginTop: 4 }}>{req.required_score}</div>
                        <div style={{ fontSize: 11, color: '#94a3b8' }}>weight: {req.weight}</div>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </Card>
          ))}
        </div>
      )}
    </div>
  );
}
