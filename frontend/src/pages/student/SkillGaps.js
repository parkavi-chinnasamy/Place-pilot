import React, { useState, useEffect } from 'react';
import { readinessAPI, jobRolesAPI } from '../../services/api';
import { Card, PageHeader, LoadingSpinner, DemoBanner, ProgressBar, Badge } from '../../components/common/Card';
import { RadarChart, Radar, PolarGrid, PolarAngleAxis, ResponsiveContainer } from 'recharts';

export default function SkillGaps() {
  const [gaps, setGaps] = useState([]);
  const [roles, setRoles] = useState([]);
  const [selectedRole, setSelectedRole] = useState('');
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    jobRolesAPI.list().then(r => { setRoles(r.data); if (r.data[0]) { setSelectedRole(r.data[0].id); loadGaps(r.data[0].id); } });
  }, []);

  const loadGaps = async (roleId) => {
    setLoading(true);
    try { const res = await readinessAPI.getSkillGaps(roleId); setGaps(res.data); } catch {}
    finally { setLoading(false); }
  };

  const handleRole = (id) => { setSelectedRole(id); loadGaps(id); };

  const radarData = gaps.map(g => ({ subject: g.skill_name.toUpperCase(), student: Math.round(g.student_score||0), required: Math.round(g.required_score||0) }));

  return (
    <div>
      <DemoBanner />
      <PageHeader title="Skill Gap Analysis" subtitle="See exactly where you stand vs what the role requires" />

      <Card style={{ marginBottom:24 }}>
        <label style={{ fontSize:12, fontWeight:700, color:'#64748b', display:'block', marginBottom:6 }}>FILTER BY JOB ROLE</label>
        <select value={selectedRole} onChange={e => handleRole(e.target.value)}
          style={{ padding:'10px 14px', border:'1.5px solid #e2e8f0', borderRadius:8, fontSize:14, background:'white', minWidth:260 }}>
          {roles.map(r => <option key={r.id} value={r.id}>{r.name}</option>)}
        </select>
      </Card>

      {loading ? <LoadingSpinner /> : (
        <>
          {gaps.length > 0 ? (
            <>
              <div style={{ display:'grid', gridTemplateColumns:'1fr 1fr', gap:20, marginBottom:20 }}>
                <Card>
                  <h3 style={{ fontWeight:700, marginBottom:16 }}>Skill Gap Radar</h3>
                  <ResponsiveContainer width="100%" height={280}>
                    <RadarChart data={radarData}>
                      <PolarGrid stroke="#e2e8f0" />
                      <PolarAngleAxis dataKey="subject" tick={{ fontSize:10 }} />
                      <Radar name="Your Score" dataKey="student" stroke="#4f46e5" fill="#4f46e5" fillOpacity={0.3} />
                      <Radar name="Required" dataKey="required" stroke="#ef4444" fill="#ef4444" fillOpacity={0.1} strokeDasharray="4 2" />
                    </RadarChart>
                  </ResponsiveContainer>
                  <div style={{ display:'flex', gap:16, justifyContent:'center', marginTop:8 }}>
                    <span style={{ fontSize:12, color:'#4f46e5', fontWeight:600 }}>● Your Score</span>
                    <span style={{ fontSize:12, color:'#ef4444', fontWeight:600 }}>● Required</span>
                  </div>
                </Card>
                <Card>
                  <h3 style={{ fontWeight:700, marginBottom:16 }}>Priority Ranking</h3>
                  <div style={{ fontSize:12, color:'#94a3b8', marginBottom:12 }}>Skills sorted by gap severity (highest priority first)</div>
                  {[...gaps].sort((a,b)=>b.gap-a.gap).map((g,i) => (
                    <div key={i} style={{ display:'flex', alignItems:'center', gap:12, marginBottom:10 }}>
                      <span style={{ fontWeight:800, color: i<2?'#ef4444':i<4?'#f59e0b':'#10b981', width:20, fontSize:14 }}>#{i+1}</span>
                      <div style={{ flex:1 }}>
                        <div style={{ display:'flex', justifyContent:'space-between', marginBottom:4, fontSize:13 }}>
                          <span style={{ fontWeight:600 }}>{g.skill_name.toUpperCase()}</span>
                          <span style={{ color: g.gap>20?'#ef4444':g.gap>10?'#f59e0b':'#10b981', fontWeight:700 }}>Gap: {g.gap?.toFixed(0)}</span>
                        </div>
                        <ProgressBar value={g.student_score||0} color={g.gap>20?'#ef4444':g.gap>10?'#f59e0b':'#10b981'} showLabel={false} />
                      </div>
                    </div>
                  ))}
                </Card>
              </div>

              <Card>
                <h3 style={{ fontWeight:700, marginBottom:16 }}>Detailed Skill Analysis</h3>
                <div style={{ overflowX:'auto' }}>
                  <table style={{ width:'100%', borderCollapse:'collapse', fontSize:13 }}>
                    <thead>
                      <tr style={{ background:'#f8fafc' }}>
                        {['Priority','Skill','Your Score','Required','Gap','Evidence','Trend'].map(h => (
                          <th key={h} style={{ padding:'10px 12px', textAlign:'left', fontWeight:700, color:'#64748b', fontSize:11, textTransform:'uppercase', letterSpacing:'0.04em', borderBottom:'2px solid #e2e8f0' }}>{h}</th>
                        ))}
                      </tr>
                    </thead>
                    <tbody>
                      {gaps.map((g,i) => (
                        <tr key={i} style={{ borderBottom:'1px solid #f1f5f9' }}>
                          <td style={{ padding:'10px 12px', fontWeight:700, color:'#4f46e5' }}>#{g.priority}</td>
                          <td style={{ padding:'10px 12px', fontWeight:600 }}>{g.skill_name.toUpperCase()}</td>
                          <td style={{ padding:'10px 12px' }}>
                            <span style={{ fontWeight:700, color:g.gap>20?'#ef4444':g.gap>10?'#f59e0b':'#10b981' }}>{g.student_score?.toFixed(0)}</span>/100
                          </td>
                          <td style={{ padding:'10px 12px', color:'#475569' }}>{g.required_score?.toFixed(0)}/100</td>
                          <td style={{ padding:'10px 12px' }}>
                            <span style={{ fontWeight:700, color:g.gap>20?'#ef4444':g.gap>10?'#f59e0b':'#64748b' }}>{g.gap?.toFixed(0)}</span>
                          </td>
                          <td style={{ padding:'10px 12px' }}>
                            <Badge label={g.confidence} type={g.confidence==='High'?'success':g.confidence==='Medium'?'warning':'info'} />
                            {g.observations<2 && <span style={{ fontSize:10, color:'#94a3b8', display:'block', marginTop:2 }}>Limited data ({g.observations} obs)</span>}
                          </td>
                          <td style={{ padding:'10px 12px' }}>
                            <span style={{ fontSize:12, color:g.trend==='improving'?'#10b981':g.trend==='declining'?'#ef4444':'#64748b' }}>
                              {g.trend==='improving'?'↑ Improving':g.trend==='declining'?'↓ Declining':'→ Stable'}
                            </span>
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </Card>
            </>
          ) : (
            <Card style={{ textAlign:'center', padding:60 }}>
              <div style={{ fontSize:48, marginBottom:16 }}>📊</div>
              <h3 style={{ fontSize:16, fontWeight:600, marginBottom:8 }}>No skill gap data yet</h3>
              <p style={{ color:'#94a3b8', fontSize:13 }}>Calculate your readiness first to see skill gaps</p>
            </Card>
          )}
        </>
      )}
    </div>
  );
}
