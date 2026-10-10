import React, { useState, useEffect } from 'react';
import { leetcodeAPI } from '../../services/api';
import { Card, PageHeader, Btn, LoadingSpinner, DemoBanner, ProgressBar } from '../../components/common/Card';
import { toast } from 'react-toastify';
import { FiSave, FiEdit } from 'react-icons/fi';

export default function LeetCode() {
  const [data, setData] = useState(null);
  const [editing, setEditing] = useState(false);
  const [form, setForm] = useState({ leetcode_username:'', total_solved:0, easy_solved:0, medium_solved:0, hard_solved:0, acceptance_rate:0, contest_rating:0, global_ranking:'' });
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);

  useEffect(() => {
    leetcodeAPI.getProgress().then(r => {
      setData(r.data);
      if (r.data?.total_solved > 0) setForm({ leetcode_username:r.data.leetcode_username||'', total_solved:r.data.total_solved, easy_solved:r.data.easy_solved, medium_solved:r.data.medium_solved, hard_solved:r.data.hard_solved, acceptance_rate:r.data.acceptance_rate, contest_rating:r.data.contest_rating, global_ranking:r.data.global_ranking||'' });
    }).finally(() => setLoading(false));
  }, []);

  const save = async () => {
    setSaving(true);
    try {
      await leetcodeAPI.update({ ...form, global_ranking: form.global_ranking || null });
      const r = await leetcodeAPI.getProgress();
      setData(r.data);
      setEditing(false);
      toast.success('LeetCode progress updated!');
    } catch { toast.error('Failed to save'); }
    finally { setSaving(false); }
  };

  if (loading) return <LoadingSpinner />;

  const total = data?.total_solved || 0;
  const easy = data?.easy_solved || 0;
  const medium = data?.medium_solved || 0;
  const hard = data?.hard_solved || 0;

  return (
    <div>
      <DemoBanner message="LeetCode data is manually entered. Live LeetCode API integration can be added in production. This data feeds into your readiness calculation." />
      <PageHeader title="LeetCode Progress" subtitle="Track your competitive programming performance"
        action={!editing ? <Btn onClick={() => setEditing(true)}><FiEdit /> Update Progress</Btn> :
          <div style={{ display:'flex', gap:8 }}>
            <Btn variant="secondary" onClick={() => setEditing(false)}>Cancel</Btn>
            <Btn onClick={save} disabled={saving}><FiSave /> {saving?'Saving…':'Save'}</Btn>
          </div>
        }
      />

      {editing ? (
        <Card style={{ maxWidth:600 }}>
          <h3 style={{ fontWeight:700, marginBottom:20, fontSize:15 }}>Update LeetCode Stats</h3>
          <div style={{ display:'grid', gridTemplateColumns:'1fr 1fr', gap:16 }}>
            {[
              { label:'LeetCode Username', key:'leetcode_username', type:'text' },
              { label:'Total Solved', key:'total_solved', type:'number' },
              { label:'Easy Solved', key:'easy_solved', type:'number' },
              { label:'Medium Solved', key:'medium_solved', type:'number' },
              { label:'Hard Solved', key:'hard_solved', type:'number' },
              { label:'Acceptance Rate (%)', key:'acceptance_rate', type:'number', step:'0.1' },
              { label:'Contest Rating', key:'contest_rating', type:'number' },
              { label:'Global Ranking', key:'global_ranking', type:'number' },
            ].map(f => (
              <div key={f.key}>
                <label style={{ fontSize:12, fontWeight:600, color:'#64748b', display:'block', marginBottom:4 }}>{f.label}</label>
                <input type={f.type} step={f.step} value={form[f.key]} onChange={e => setForm({ ...form, [f.key]: f.type==='number'&&e.target.value!==''?parseFloat(e.target.value):e.target.value })}
                  style={{ width:'100%', padding:'9px 12px', border:'1.5px solid #e2e8f0', borderRadius:8, fontSize:13 }} />
              </div>
            ))}
          </div>
        </Card>
      ) : (
        <>
          <div style={{ display:'grid', gridTemplateColumns:'repeat(auto-fit,minmax(160px,1fr))', gap:16, marginBottom:24 }}>
            {[
              { label:'Total Solved', val:total, color:'#4f46e5', emoji:'🎯' },
              { label:'Easy', val:easy, color:'#10b981', emoji:'🟢' },
              { label:'Medium', val:medium, color:'#f59e0b', emoji:'🟡' },
              { label:'Hard', val:hard, color:'#ef4444', emoji:'🔴' },
              { label:'Contest Rating', val:data?.contest_rating||0, color:'#8b5cf6', emoji:'🏆' },
              { label:'Acceptance Rate', val:`${data?.acceptance_rate?.toFixed(1)||0}%`, color:'#06b6d4', emoji:'✅' },
            ].map(s => (
              <Card key={s.label} style={{ textAlign:'center', padding:20 }}>
                <div style={{ fontSize:28, marginBottom:6 }}>{s.emoji}</div>
                <div style={{ fontSize:28, fontWeight:800, color:s.color }}>{s.val}</div>
                <div style={{ fontSize:12, color:'#94a3b8', marginTop:4 }}>{s.label}</div>
              </Card>
            ))}
          </div>

          <div style={{ display:'grid', gridTemplateColumns:'1fr 1fr', gap:20 }}>
            <Card>
              <h3 style={{ fontWeight:700, marginBottom:16, fontSize:15 }}>Difficulty Breakdown</h3>
              {[['Easy', easy, total, '#10b981'], ['Medium', medium, total, '#f59e0b'], ['Hard', hard, total, '#ef4444']].map(([l,v,t,c]) => (
                <div key={l} style={{ marginBottom:14 }}>
                  <div style={{ display:'flex', justifyContent:'space-between', marginBottom:6, fontSize:13 }}>
                    <span style={{ fontWeight:600 }}>{l}</span>
                    <span style={{ color:c, fontWeight:700 }}>{v} problems</span>
                  </div>
                  <ProgressBar value={t>0?v/t*100:0} color={c} showLabel={false} />
                </div>
              ))}
              {data?.leetcode_username && (
                <div style={{ marginTop:16, padding:'10px 14px', background:'#f8fafc', borderRadius:8, fontSize:13 }}>
                  <strong>Username:</strong> {data.leetcode_username}<br />
                  {data.global_ranking && <><strong>Rank:</strong> #{data.global_ranking?.toLocaleString()}</>}
                </div>
              )}
            </Card>
            <Card>
              <h3 style={{ fontWeight:700, marginBottom:16, fontSize:15 }}>How This Feeds Readiness</h3>
              <div style={{ background:'#eef2ff', borderRadius:10, padding:16, marginBottom:16 }}>
                <div style={{ fontSize:13, color:'#3730a3', lineHeight:1.8 }}>
                  <strong>LeetCode Score Formula:</strong><br />
                  score = min(100, (easy×1 + medium×2 + hard×3) × 0.15 + acceptance_rate × 0.3)
                </div>
              </div>
              <div style={{ padding:'10px 14px', background:'#f8fafc', borderRadius:8, fontSize:13, marginBottom:12 }}>
                <strong>Estimated LeetCode Score:</strong>{' '}
                <span style={{ color:'#4f46e5', fontWeight:700 }}>
                  {Math.min(100, ((easy + medium*2 + hard*3) * 0.15 + (data?.acceptance_rate||0) * 0.3)).toFixed(1)}/100
                </span>
              </div>
              <p style={{ fontSize:12, color:'#94a3b8', lineHeight:1.7 }}>
                This score is one of 12 features used by the Random Forest model to predict your placement readiness. Solving more medium and hard problems increases your score significantly.
              </p>
            </Card>
          </div>
        </>
      )}
    </div>
  );
}
