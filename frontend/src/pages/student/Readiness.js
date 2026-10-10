import React, { useState, useEffect } from 'react';
import { readinessAPI, jobRolesAPI } from '../../services/api';
import { Card, PageHeader, Btn, LoadingSpinner, DemoBanner, Badge, ProgressBar } from '../../components/common/Card';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid, Cell } from 'recharts';
import { toast } from 'react-toastify';
import { FiRefreshCw } from 'react-icons/fi';

const RC_COLOR = { 'Ready':'#10b981','Moderately Ready':'#f59e0b','Needs Improvement':'#ef4444' };

export default function Readiness() {
  const [roles, setRoles] = useState([]);
  const [selectedRole, setSelectedRole] = useState('');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [currentList, setCurrentList] = useState([]);

  useEffect(() => {
    jobRolesAPI.list().then(r => setRoles(r.data)).catch(() => {});
    readinessAPI.getCurrent().then(r => setCurrentList(r.data)).catch(() => {});
  }, []);

  const calculate = async () => {
    if (!selectedRole) return toast.warning('Select a job role first');
    setLoading(true);
    try {
      const res = await readinessAPI.calculate(selectedRole);
      setResult(res.data);
      const cur = await readinessAPI.getCurrent();
      setCurrentList(cur.data);
      toast.success('Readiness calculated!');
    } catch (e) {
      toast.error(e.response?.data?.detail || 'Calculation failed');
    } finally { setLoading(false); }
  };

  const shapData = result ? [
    ...(result.readiness?.positive_factors || []).map(f => ({ name: f.label, value: parseFloat(f.shap), color: '#10b981' })),
    ...(result.readiness?.negative_factors || []).map(f => ({ name: f.label, value: Math.abs(parseFloat(f.shap)), color: '#ef4444' })),
  ] : [];

  const gapData = (result?.skill_gaps || []).map(g => ({
    skill: g.skill_name.toUpperCase(), student: Math.round(g.student_score), required: Math.round(g.required_score), gap: Math.round(g.gap)
  }));

  return (
    <div>
      <DemoBanner message="Prototype — Readiness scores use a Random Forest trained on SYNTHETIC demo data. Not a guarantee of placement success." />
      <PageHeader title="Placement Readiness" subtitle="Role-specific AI readiness prediction with SHAP explanations" />

      {/* Role picker */}
      <Card style={{ marginBottom: 24, display:'flex', gap:12, alignItems:'flex-end', flexWrap:'wrap' }}>
        <div style={{ flex:1 }}>
          <label style={{ display:'block', fontSize:12, fontWeight:700, color:'#64748b', marginBottom:6 }}>TARGET JOB ROLE</label>
          <select value={selectedRole} onChange={e => setSelectedRole(e.target.value)}
            style={{ width:'100%', padding:'10px 14px', border:'1.5px solid #e2e8f0', borderRadius:8, fontSize:14, background:'white' }}>
            <option value="">Choose a role…</option>
            {roles.map(r => <option key={r.id} value={r.id}>{r.name}</option>)}
          </select>
        </div>
        <Btn onClick={calculate} disabled={loading} size="lg">
          <FiRefreshCw /> {loading ? 'Calculating…' : 'Calculate Readiness'}
        </Btn>
      </Card>

      {/* Existing readiness cards */}
      {currentList.length > 0 && !result && (
        <div style={{ marginBottom: 24 }}>
          <h3 style={{ fontWeight:700, marginBottom:12, fontSize:15 }}>Your Current Readiness</h3>
          <div style={{ display:'grid', gridTemplateColumns:'repeat(auto-fit,minmax(200px,1fr))', gap:14 }}>
            {currentList.map((r,i) => (
              <Card key={i} style={{ borderTop:`4px solid ${RC_COLOR[r.readiness_category]||'#94a3b8'}` }}>
                <div style={{ fontSize:12, fontWeight:700, color:'#64748b', marginBottom:6 }}>{r.job_role_name}</div>
                <div style={{ fontSize:36, fontWeight:800, color:RC_COLOR[r.readiness_category] }}>{r.readiness_score?.toFixed(0)}%</div>
                <div style={{ marginTop:6 }}><Badge label={r.readiness_category} type={r.readiness_category==='Ready'?'success':r.readiness_category==='Moderately Ready'?'warning':'danger'} /></div>
              </Card>
            ))}
          </div>
        </div>
      )}

      {loading && <LoadingSpinner />}

      {result && !loading && (
        <>
          {/* Big score banner */}
          <Card style={{ marginBottom:20, background:'linear-gradient(135deg,#1e1b4b,#312e81)', color:'white', border:'none' }}>
            <div style={{ display:'flex', justifyContent:'space-between', alignItems:'center', flexWrap:'wrap', gap:20 }}>
              <div>
                <div style={{ fontSize:12, color:'rgba(255,255,255,0.5)', marginBottom:6, letterSpacing:'0.06em' }}>
                  {result.readiness?.job_role_name?.toUpperCase()} · READINESS SCORE
                </div>
                <div style={{ fontSize:72, fontWeight:800, color:RC_COLOR[result.readiness?.readiness_category]||'#818cf8', lineHeight:1 }}>
                  {result.readiness?.readiness_score?.toFixed(0)}%
                </div>
                <div style={{ marginTop:12 }}>
                  <Badge label={result.readiness?.readiness_category} type={result.readiness?.readiness_category==='Ready'?'success':result.readiness?.readiness_category==='Moderately Ready'?'warning':'danger'} />
                </div>
                <p style={{ marginTop:12, fontSize:11, color:'rgba(255,255,255,0.35)', maxWidth:480 }}>
                  {result.readiness?.disclaimer}
                </p>
              </div>
              <div style={{ textAlign:'center' }}>
                <div style={{ fontSize:11, color:'rgba(255,255,255,0.4)', marginBottom:4 }}>Model Confidence</div>
                <div style={{ fontSize:32, fontWeight:700 }}>{((result.readiness?.confidence||0)*100).toFixed(0)}%</div>
                <div style={{ fontSize:10, color:'rgba(255,255,255,0.3)', marginTop:4 }}>{result.readiness?.model_version}</div>
              </div>
            </div>
          </Card>

          <div style={{ display:'grid', gridTemplateColumns:'1fr 1fr', gap:20, marginBottom:20 }}>
            {/* SHAP Chart */}
            <Card>
              <h3 style={{ fontWeight:700, marginBottom:4 }}>Why this score? (SHAP)</h3>
              <p style={{ fontSize:12, color:'#94a3b8', marginBottom:16 }}>
                Green = contributed toward readiness · Red = pulled score down
              </p>
              {shapData.length > 0 ? (
                <ResponsiveContainer width="100%" height={240}>
                  <BarChart data={shapData} layout="vertical" margin={{ left:120, right:10 }}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" />
                    <XAxis type="number" tick={{ fontSize:10 }} />
                    <YAxis type="category" dataKey="name" tick={{ fontSize:11 }} width={120} />
                    <Tooltip formatter={v => v.toFixed(3)} />
                    <Bar dataKey="value" radius={[0,4,4,0]}>
                      {shapData.map((e,i) => <Cell key={i} fill={e.color} />)}
                    </Bar>
                  </BarChart>
                </ResponsiveContainer>
              ) : <p style={{ color:'#94a3b8', fontSize:13, textAlign:'center', padding:40 }}>No SHAP data available</p>}
            </Card>

            {/* Skill Gaps */}
            <Card>
              <h3 style={{ fontWeight:700, marginBottom:4 }}>Skill Gap Analysis</h3>
              <p style={{ fontSize:12, color:'#94a3b8', marginBottom:16 }}>Your score vs required score for this role</p>
              {gapData.length > 0 ? (
                <ResponsiveContainer width="100%" height={240}>
                  <BarChart data={gapData} margin={{ left:0, right:10 }}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" />
                    <XAxis dataKey="skill" tick={{ fontSize:9 }} />
                    <YAxis domain={[0,100]} tick={{ fontSize:10 }} />
                    <Tooltip />
                    <Bar dataKey="student" fill="#4f46e5" name="Your Score" radius={[4,4,0,0]} />
                    <Bar dataKey="required" fill="#e2e8f0" name="Required" radius={[4,4,0,0]} />
                  </BarChart>
                </ResponsiveContainer>
              ) : <p style={{ color:'#94a3b8', fontSize:13, textAlign:'center', padding:40 }}>No gap data</p>}
            </Card>
          </div>

          {/* Positive / Negative factors */}
          <div style={{ display:'grid', gridTemplateColumns:'1fr 1fr', gap:20, marginBottom:20 }}>
            <Card style={{ borderLeft:'4px solid #10b981' }}>
              <h3 style={{ fontWeight:700, marginBottom:12, color:'#10b981', fontSize:15 }}>✅ Positive Contributors</h3>
              {(result.readiness?.positive_factors||[]).map((f,i) => (
                <div key={i} style={{ display:'flex', justifyContent:'space-between', padding:'8px 0', borderBottom:'1px solid #f1f5f9', fontSize:13 }}>
                  <span>{f.label}</span>
                  <div style={{ display:'flex', gap:12 }}>
                    <span style={{ color:'#94a3b8' }}>{f.value?.toFixed(0)}/100</span>
                    <span style={{ color:'#10b981', fontWeight:700 }}>+{Math.abs(f.shap).toFixed(3)}</span>
                  </div>
                </div>
              ))}
              {!(result.readiness?.positive_factors?.length) && <p style={{ color:'#94a3b8', fontSize:13 }}>No positive factors yet</p>}
            </Card>
            <Card style={{ borderLeft:'4px solid #ef4444' }}>
              <h3 style={{ fontWeight:700, marginBottom:12, color:'#ef4444', fontSize:15 }}>⚠️ Areas to Improve</h3>
              {(result.readiness?.negative_factors||[]).map((f,i) => (
                <div key={i} style={{ display:'flex', justifyContent:'space-between', padding:'8px 0', borderBottom:'1px solid #f1f5f9', fontSize:13 }}>
                  <span>{f.label}</span>
                  <div style={{ display:'flex', gap:12 }}>
                    <span style={{ color:'#94a3b8' }}>{f.value?.toFixed(0)}/100</span>
                    <span style={{ color:'#ef4444', fontWeight:700 }}>{f.shap?.toFixed(3)}</span>
                  </div>
                </div>
              ))}
              {!(result.readiness?.negative_factors?.length) && <p style={{ color:'#94a3b8', fontSize:13 }}>No negative factors found</p>}
            </Card>
          </div>

          {/* Priority gaps list */}
          <Card>
            <h3 style={{ fontWeight:700, marginBottom:16, fontSize:15 }}>Priority Skill Gaps</h3>
            <div style={{ display:'flex', flexDirection:'column', gap:12 }}>
              {(result.skill_gaps||[]).slice(0,6).map((g,i) => (
                <div key={i} style={{ display:'flex', alignItems:'center', gap:16, padding:'12px 16px', background:'#f8fafc', borderRadius:10 }}>
                  <div style={{ width:28, height:28, borderRadius:'50%', background:'#4f46e5', color:'white', display:'flex', alignItems:'center', justifyContent:'center', fontWeight:700, fontSize:13, flexShrink:0 }}>{i+1}</div>
                  <div style={{ flex:1 }}>
                    <div style={{ fontWeight:600, fontSize:13, marginBottom:4 }}>{g.skill_name.toUpperCase()}</div>
                    <ProgressBar value={g.student_score} color={g.gap>20?'#ef4444':'#f59e0b'} showLabel={false} />
                  </div>
                  <div style={{ textAlign:'right', flexShrink:0 }}>
                    <div style={{ fontSize:13, fontWeight:700, color:'#ef4444' }}>Gap: {g.gap?.toFixed(0)}</div>
                    <div style={{ fontSize:11, color:'#94a3b8' }}>{g.student_score?.toFixed(0)} / {g.required_score?.toFixed(0)}</div>
                    <div style={{ fontSize:10, color:'#94a3b8', marginTop:2 }}>Confidence: {g.confidence}</div>
                  </div>
                </div>
              ))}
            </div>
          </Card>
        </>
      )}
    </div>
  );
}
