import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { adminAPI } from '../../services/api';
import { Card, PageHeader, LoadingSpinner, DemoBanner, Badge } from '../../components/common/Card';

export default function AdminStudents() {
  const [students, setStudents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState('');
  const [filterReadiness, setFilterReadiness] = useState('');
  const navigate = useNavigate();

  useEffect(() => { adminAPI.getStudents().then(r => setStudents(r.data)).finally(() => setLoading(false)); }, []);

  const filtered = students.filter(s =>
    (s.full_name?.toLowerCase().includes(search.toLowerCase()) || s.email?.toLowerCase().includes(search.toLowerCase())) &&
    (!filterReadiness || s.readiness_category === filterReadiness)
  );

  const RC_TYPE = { 'Ready': 'success', 'Moderately Ready': 'warning', 'Needs Improvement': 'danger' };

  return (
    <div>
      <DemoBanner />
      <PageHeader title="All Students" subtitle={`${students.length} registered students`} />
      <Card style={{ marginBottom: 20, display: 'flex', gap: 12, flexWrap: 'wrap' }}>
        <input value={search} onChange={e => setSearch(e.target.value)} placeholder="Search by name or email…"
          style={{ flex: 1, padding: '9px 14px', border: '1.5px solid #e2e8f0', borderRadius: 8, fontSize: 13, minWidth: 200 }} />
        <select value={filterReadiness} onChange={e => setFilterReadiness(e.target.value)}
          style={{ padding: '9px 14px', border: '1.5px solid #e2e8f0', borderRadius: 8, fontSize: 13, background: 'white' }}>
          <option value="">All readiness levels</option>
          <option value="Ready">Ready</option>
          <option value="Moderately Ready">Moderately Ready</option>
          <option value="Needs Improvement">Needs Improvement</option>
        </select>
      </Card>

      {loading ? <LoadingSpinner /> : (
        <Card>
          <div style={{ overflowX: 'auto' }}>
            <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: 13 }}>
              <thead>
                <tr style={{ background: '#f8fafc' }}>
                  {['Student', 'Dept', 'CGPA', 'Target Role', 'Readiness', 'Strongest', 'Weakest', 'Last Test', 'Profile', ''].map(h => (
                    <th key={h} style={{ padding: '10px 14px', textAlign: 'left', fontSize: 11, fontWeight: 700, color: '#64748b', textTransform: 'uppercase', borderBottom: '2px solid #e2e8f0', whiteSpace: 'nowrap' }}>{h}</th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {filtered.map((s, i) => (
                  <tr key={i} style={{ borderBottom: '1px solid #f1f5f9', cursor: 'pointer' }} onClick={() => navigate(`/admin/students/${s.id}`)}
                    onMouseEnter={e => e.currentTarget.style.background = '#f8fafc'} onMouseLeave={e => e.currentTarget.style.background = 'transparent'}>
                    <td style={{ padding: '12px 14px' }}>
                      <div style={{ fontWeight: 600 }}>{s.full_name}</div>
                      <div style={{ fontSize: 11, color: '#94a3b8' }}>{s.email}</div>
                    </td>
                    <td style={{ padding: '12px 14px', color: '#64748b' }}>{s.department || '—'}</td>
                    <td style={{ padding: '12px 14px', fontWeight: 600 }}>{s.cgpa || '—'}</td>
                    <td style={{ padding: '12px 14px', color: '#64748b', fontSize: 12 }}>{s.target_role || '—'}</td>
                    <td style={{ padding: '12px 14px' }}>
                      {s.readiness_category ? <Badge label={s.readiness_category} type={RC_TYPE[s.readiness_category] || 'default'} /> : <span style={{ color: '#94a3b8' }}>—</span>}
                      {s.readiness_score && <div style={{ fontSize: 11, color: '#64748b', marginTop: 3 }}>{s.readiness_score?.toFixed(0)}%</div>}
                    </td>
                    <td style={{ padding: '12px 14px', color: '#10b981', fontWeight: 600, fontSize: 12 }}>{s.strongest_skill || '—'}</td>
                    <td style={{ padding: '12px 14px', color: '#ef4444', fontWeight: 600, fontSize: 12 }}>{s.weakest_skill || '—'}</td>
                    <td style={{ padding: '12px 14px', color: '#94a3b8', fontSize: 11 }}>{s.last_assessment ? new Date(s.last_assessment).toLocaleDateString() : '—'}</td>
                    <td style={{ padding: '12px 14px' }}>
                      <div style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
                        <div style={{ width: 50, height: 6, background: '#f1f5f9', borderRadius: 999 }}>
                          <div style={{ width: `${s.profile_completeness || 0}%`, height: '100%', background: '#4f46e5', borderRadius: 999 }} />
                        </div>
                        <span style={{ fontSize: 11, color: '#64748b' }}>{s.profile_completeness || 0}%</span>
                      </div>
                    </td>
                    <td style={{ padding: '12px 14px' }}><span style={{ color: '#4f46e5', fontSize: 12 }}>View →</span></td>
                  </tr>
                ))}
              </tbody>
            </table>
            {filtered.length === 0 && <div style={{ textAlign: 'center', padding: 40, color: '#94a3b8' }}>No students match your search</div>}
          </div>
        </Card>
      )}
    </div>
  );
}
