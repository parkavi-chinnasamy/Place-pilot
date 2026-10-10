import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { adminAPI } from '../../services/api';
import { Card, PageHeader, LoadingSpinner, DemoBanner, Badge, ProgressBar } from '../../components/common/Card';
import { RadarChart, Radar, PolarGrid, PolarAngleAxis, ResponsiveContainer } from 'recharts';

export default function AdminStudentDetail() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => { adminAPI.getStudent(id).then(r => setData(r.data)).finally(() => setLoading(false)); }, [id]);

  if (loading) return <LoadingSpinner />;
  if (!data) return <div>Student not found</div>;

  const { student, skill_profile, readiness, recent_assessments } = data;
  const radarData = Object.entries(skill_profile || {}).map(([k, v]) => ({ subject: k.toUpperCase(), value: Math.round(v) }));

  return (
    <div>
      <DemoBanner />
      <PageHeader title={student.full_name} subtitle={`${student.department} · ${student.email}`}
        action={<button onClick={() => navigate('/admin/students')} style={{ padding:'9px 20px', border:'1px solid #e2e8f0', borderRadius:8, background:'white', cursor:'pointer', fontWeight:600, fontSize:13 }}>← Back to Students</button>}
      />

      <div style={{ display:'grid', gridTemplateColumns:'1fr 1fr', gap:20, marginBottom:20 }}>
        <Card>
          <h3 style={{ fontWeight:700, marginBottom:16, fontSize:15 }}>Academic Profile</h3>
          {[['Batch',student.batch],['Year',`Year ${student.year}`],['CGPA',student.cgpa],['10th %',student.tenth_percent],['12th %',student.twelfth_percent],['Languages',(student.programming_languages||[]).join(', ')||'—']].map(([l,v]) => (
            <div key={l} style={{ display:'flex', justifyContent:'space-between', padding:'8px 0', borderBottom:'1px solid #f1f5f9', fontSize:13 }}>
              <span style={{ color:'#64748b' }}>{l}</span>
              <span style={{ fontWeight:600 }}>{v || '—'}</span>
            </div>
          ))}
        </Card>

        <Card>
          <h3 style={{ fontWeight:700, marginBottom:16, fontSize:15 }}>Readiness by Role</h3>
          {readiness?.length > 0 ? readiness.map((r,i) => (
            <div key={i} style={{ marginBottom:12, padding:'10px 14px', background:'#f8fafc', borderRadius:8 }}>
              <div style={{ display:'flex', justifyContent:'space-between', marginBottom:4 }}>
                <span style={{ fontWeight:600, fontSize:13 }}>{r.job_role_id}</span>
                <span style={{ fontWeight:700, color: r.category==='Ready'?'#10b981':r.category==='Moderately Ready'?'#f59e0b':'#ef4444' }}>{r.score?.toFixed(0)}%</span>
              </div>
              <Badge label={r.category} type={r.category==='Ready'?'success':r.category==='Moderately Ready'?'warning':'danger'} />
            </div>
          )) : <p style={{ color:'#94a3b8', fontSize:13 }}>No readiness calculated yet</p>}
        </Card>
      </div>

      <div style={{ display:'grid', gridTemplateColumns:'1fr 1fr', gap:20, marginBottom:20 }}>
        <Card>
          <h3 style={{ fontWeight:700, marginBottom:16, fontSize:15 }}>Skill Profile</h3>
          <ResponsiveContainer width="100%" height={240}>
            <RadarChart data={radarData}>
              <PolarGrid stroke="#e2e8f0" />
              <PolarAngleAxis dataKey="subject" tick={{ fontSize:10 }} />
              <Radar dataKey="value" stroke="#4f46e5" fill="#4f46e5" fillOpacity={0.25} />
            </RadarChart>
          </ResponsiveContainer>
        </Card>
        <Card>
          <h3 style={{ fontWeight:700, marginBottom:16, fontSize:15 }}>Skill Scores</h3>
          {Object.entries(skill_profile||{}).map(([k,v]) => (
            <div key={k} style={{ marginBottom:10 }}>
              <div style={{ display:'flex', justifyContent:'space-between', fontSize:12, marginBottom:4 }}>
                <span style={{ fontWeight:600, textTransform:'capitalize' }}>{k}</span>
                <span style={{ fontWeight:700, color:v>=70?'#10b981':v>=50?'#f59e0b':'#ef4444' }}>{Math.round(v)}</span>
              </div>
              <ProgressBar value={v} color={v>=70?'#10b981':v>=50?'#f59e0b':'#ef4444'} showLabel={false} />
            </div>
          ))}
        </Card>
      </div>

      <Card>
        <h3 style={{ fontWeight:700, marginBottom:16, fontSize:15 }}>Recent Assessments</h3>
        {recent_assessments?.length > 0 ? (
          <table style={{ width:'100%', borderCollapse:'collapse', fontSize:13 }}>
            <thead><tr style={{ background:'#f8fafc' }}>
              {['Type','Score','Correct','Date'].map(h => <th key={h} style={{ padding:'8px 12px', textAlign:'left', fontSize:11, fontWeight:700, color:'#64748b', textTransform:'uppercase' }}>{h}</th>)}
            </tr></thead>
            <tbody>
              {recent_assessments.map((a,i) => (
                <tr key={i} style={{ borderBottom:'1px solid #f1f5f9' }}>
                  <td style={{ padding:'10px 12px', fontWeight:600, textTransform:'capitalize' }}>{a.type}</td>
                  <td style={{ padding:'10px 12px', fontWeight:700, color:a.score>=70?'#10b981':a.score>=50?'#f59e0b':'#ef4444' }}>{a.score?.toFixed(0)}%</td>
                  <td style={{ padding:'10px 12px', color:'#64748b' }}>{a.correct}/{a.total}</td>
                  <td style={{ padding:'10px 12px', color:'#94a3b8', fontSize:12 }}>{new Date(a.date).toLocaleDateString()}</td>
                </tr>
              ))}
            </tbody>
          </table>
        ) : <p style={{ color:'#94a3b8', fontSize:13 }}>No assessments taken yet</p>}
      </Card>
    </div>
  );
}
