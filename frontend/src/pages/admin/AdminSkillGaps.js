import React, { useState, useEffect } from 'react';
import { adminAPI } from '../../services/api';
import { Card, PageHeader, LoadingSpinner, DemoBanner } from '../../components/common/Card';

const getColor = (val) => {
  if (val >= 75) return '#10b981';
  if (val >= 60) return '#f59e0b';
  return '#ef4444';
};

export default function AdminSkillGaps() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => { adminAPI.getSkillGaps().then(r => setData(r.data)).finally(() => setLoading(false)); }, []);

  if (loading) return <LoadingSpinner />;
  if (!data) return null;

  const skills = ['dsa', 'programming', 'dbms', 'oop', 'aptitude', 'coding', 'interview', 'resume', 'leetcode'];

  return (
    <div>
      <DemoBanner />
      <PageHeader title="Skill Gap Heatmap" subtitle="Students × Skills matrix showing batch-wide weak areas" />

      {/* Stats row */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit,minmax(160px,1fr))', gap: 14, marginBottom: 24 }}>
        {skills.map(s => (
          <Card key={s} style={{ padding: 14, textAlign: 'center' }}>
            <div style={{ fontSize: 22, fontWeight: 800, color: getColor(data.skill_stats[s]?.average || 0) }}>
              {data.skill_stats[s]?.average || 0}
            </div>
            <div style={{ fontSize: 11, fontWeight: 700, color: '#64748b', textTransform: 'uppercase', marginTop: 4 }}>{s}</div>
            <div style={{ fontSize: 11, color: '#ef4444', marginTop: 4 }}>
              {data.skill_stats[s]?.below_60_count || 0} below 60
            </div>
          </Card>
        ))}
      </div>

      {/* Heatmap table */}
      <Card>
        <h3 style={{ fontWeight: 700, marginBottom: 4, fontSize: 15 }}>Student-Skill Heatmap</h3>
        <p style={{ fontSize: 12, color: '#94a3b8', marginBottom: 16 }}>
          🟢 ≥75 · 🟡 60–74 · 🔴 &lt;60 · Hover for exact score
        </p>
        <div style={{ overflowX: 'auto' }}>
          <table style={{ borderCollapse: 'collapse', fontSize: 12, minWidth: 800 }}>
            <thead>
              <tr style={{ background: '#1e1b4b', color: 'white' }}>
                <th style={{ padding: '10px 16px', textAlign: 'left', fontWeight: 700, whiteSpace: 'nowrap' }}>Student</th>
                <th style={{ padding: '10px 8px', textAlign: 'left', fontWeight: 700, fontSize: 11, whiteSpace: 'nowrap' }}>Dept</th>
                {skills.map(s => <th key={s} style={{ padding: '10px 8px', textAlign: 'center', fontWeight: 700, fontSize: 11, textTransform: 'uppercase' }}>{s}</th>)}
              </tr>
            </thead>
            <tbody>
              {(data.heatmap || []).map((row, i) => (
                <tr key={i} style={{ borderBottom: '1px solid #f1f5f9' }}
                  onMouseEnter={e => e.currentTarget.style.background = '#f8fafc'}
                  onMouseLeave={e => e.currentTarget.style.background = 'transparent'}>
                  <td style={{ padding: '8px 16px', fontWeight: 600, whiteSpace: 'nowrap' }}>{row.student_name}</td>
                  <td style={{ padding: '8px 8px', color: '#94a3b8', fontSize: 11, whiteSpace: 'nowrap' }}>{row.department?.slice(0, 6)}</td>
                  {skills.map(s => {
                    const val = Math.round(row[s] || 0);
                    const bg = val >= 75 ? '#d1fae5' : val >= 60 ? '#fef3c7' : '#fee2e2';
                    const color = val >= 75 ? '#065f46' : val >= 60 ? '#78350f' : '#991b1b';
                    return (
                      <td key={s} title={`${row.student_name} · ${s.toUpperCase()}: ${val}`} style={{ padding: '6px 8px', textAlign: 'center' }}>
                        <div style={{ background: bg, color, borderRadius: 6, padding: '4px 6px', fontWeight: 700, fontSize: 11 }}>{val}</div>
                      </td>
                    );
                  })}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </Card>
    </div>
  );
}
