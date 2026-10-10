import React, { useState, useEffect } from 'react';
import { resumeAPI, jobRolesAPI } from '../../services/api';
import { Card, PageHeader, Btn, LoadingSpinner, DemoBanner, ProgressBar } from '../../components/common/Card';
import { toast } from 'react-toastify';
import { FiUpload, FiFileText } from 'react-icons/fi';

export default function ResumeAnalyzer() {
  const [roles, setRoles] = useState([]);
  const [selectedRole, setSelectedRole] = useState('');
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    jobRolesAPI.list().then(r => setRoles(r.data));
    resumeAPI.getHistory().then(r => setHistory(r.data)).catch(() => {});
  }, []);

  const analyze = async () => {
    if (!file) return toast.warning('Please select a resume file');
    const fd = new FormData();
    fd.append('file', file);
    if (selectedRole) fd.append('job_role_id', selectedRole);
    setLoading(true);
    try {
      const res = await resumeAPI.analyze(fd);
      setResult(res.data);
      resumeAPI.getHistory().then(r => setHistory(r.data)).catch(() => {});
      toast.success('Resume analyzed!');
    } catch (e) { toast.error(e.response?.data?.detail || 'Analysis failed'); }
    finally { setLoading(false); }
  };

  const scores = result ? [
    { label:'Overall', val:result.overall_score, color:'#4f46e5' },
    { label:'Skills', val:result.skills_score, color:'#10b981' },
    { label:'Education', val:result.education_score, color:'#06b6d4' },
    { label:'Projects', val:result.projects_score, color:'#8b5cf6' },
    { label:'Experience', val:result.experience_score, color:'#f59e0b' },
    { label:'Completeness', val:result.completeness_score, color:'#ef4444' },
  ] : [];

  return (
    <div>
      <DemoBanner message="Resume analysis uses keyword matching for prototype. Full NLP parsing can be added in production. Score feeds into your readiness engine." />
      <PageHeader title="Resume Analyzer" subtitle="Get a role-specific resume score and improvement suggestions" />

      <Card style={{ marginBottom:24 }}>
        <h3 style={{ fontWeight:700, marginBottom:16, fontSize:15 }}>Upload Your Resume</h3>
        <div style={{ display:'grid', gridTemplateColumns:'1fr 1fr', gap:16, marginBottom:16 }}>
          <div>
            <label style={{ fontSize:12, fontWeight:700, color:'#64748b', display:'block', marginBottom:6 }}>TARGET JOB ROLE (optional)</label>
            <select value={selectedRole} onChange={e => setSelectedRole(e.target.value)}
              style={{ width:'100%', padding:'10px 14px', border:'1.5px solid #e2e8f0', borderRadius:8, fontSize:14, background:'white' }}>
              <option value="">Select for role-specific analysis…</option>
              {roles.map(r => <option key={r.id} value={r.id}>{r.name}</option>)}
            </select>
          </div>
          <div>
            <label style={{ fontSize:12, fontWeight:700, color:'#64748b', display:'block', marginBottom:6 }}>RESUME FILE (PDF/DOC)</label>
            <input type="file" accept=".pdf,.doc,.docx" onChange={e => setFile(e.target.files[0])}
              style={{ width:'100%', padding:'8px', border:'1.5px solid #e2e8f0', borderRadius:8, fontSize:13 }} />
          </div>
        </div>
        <Btn onClick={analyze} disabled={loading || !file} size="lg">
          <FiUpload /> {loading ? 'Analyzing…' : 'Analyze Resume'}
        </Btn>
      </Card>

      {loading && <LoadingSpinner />}

      {result && !loading && (
        <>
          <div style={{ display:'grid', gridTemplateColumns:'repeat(auto-fit,minmax(140px,1fr))', gap:14, marginBottom:20 }}>
            {scores.map(s => (
              <Card key={s.label} style={{ textAlign:'center', padding:18 }}>
                <div style={{ fontSize:32, fontWeight:800, color:s.color }}>{s.val}</div>
                <div style={{ fontSize:12, color:'#94a3b8', marginTop:4 }}>{s.label}</div>
                <div style={{ marginTop:8 }}>
                  <ProgressBar value={s.val} color={s.color} showLabel={false} />
                </div>
              </Card>
            ))}
          </div>

          <div style={{ display:'grid', gridTemplateColumns:'1fr 1fr', gap:20, marginBottom:20 }}>
            <Card>
              <h3 style={{ fontWeight:700, marginBottom:12, fontSize:15 }}>✅ Detected Skills</h3>
              {result.extracted_skills?.length > 0 ? (
                <div style={{ display:'flex', flexWrap:'wrap', gap:8 }}>
                  {result.extracted_skills.map((s,i) => <span key={i} style={{ background:'#d1fae5', color:'#065f46', padding:'4px 12px', borderRadius:20, fontSize:12, fontWeight:600 }}>{s}</span>)}
                </div>
              ) : <p style={{ color:'#94a3b8', fontSize:13 }}>No specific skills detected. Add a skills section to your resume.</p>}
            </Card>
            <Card>
              <h3 style={{ fontWeight:700, marginBottom:12, fontSize:15, color:'#ef4444' }}>❌ Missing Skills</h3>
              {result.missing_skills?.length > 0 ? (
                <div style={{ display:'flex', flexWrap:'wrap', gap:8 }}>
                  {result.missing_skills.map((s,i) => <span key={i} style={{ background:'#fee2e2', color:'#991b1b', padding:'4px 12px', borderRadius:20, fontSize:12, fontWeight:600 }}>{s}</span>)}
                </div>
              ) : <p style={{ color:'#10b981', fontSize:13 }}>✓ No critical missing skills for selected role</p>}
            </Card>
          </div>

          <Card>
            <h3 style={{ fontWeight:700, marginBottom:16, fontSize:15 }}>💡 Improvement Suggestions</h3>
            {result.improvement_suggestions?.length > 0 ? result.improvement_suggestions.map((s,i) => (
              <div key={i} style={{ display:'flex', gap:12, marginBottom:12, padding:'12px 16px', background:'#fff7ed', borderRadius:8, borderLeft:'3px solid #f59e0b' }}>
                <span style={{ fontWeight:700, color:'#92400e', flexShrink:0 }}>{s.area}</span>
                <span style={{ fontSize:13, color:'#78350f' }}>{s.tip}</span>
              </div>
            )) : <p style={{ color:'#10b981', fontSize:13 }}>✓ Your resume looks comprehensive!</p>}
          </Card>
        </>
      )}

      {history.length > 0 && (
        <Card style={{ marginTop:20 }}>
          <h3 style={{ fontWeight:700, marginBottom:12, fontSize:15 }}>Analysis History</h3>
          {history.map((h,i) => (
            <div key={i} style={{ display:'flex', justifyContent:'space-between', padding:'10px 0', borderBottom:'1px solid #f1f5f9', fontSize:13 }}>
              <div style={{ display:'flex', alignItems:'center', gap:8 }}>
                <FiFileText color="#94a3b8" />
                <span>{h.file_name}</span>
              </div>
              <div style={{ display:'flex', gap:16 }}>
                <span style={{ fontWeight:700, color:'#4f46e5' }}>{h.overall_score}/100</span>
                <span style={{ color:'#94a3b8' }}>{new Date(h.analyzed_at).toLocaleDateString()}</span>
              </div>
            </div>
          ))}
        </Card>
      )}
    </div>
  );
}
