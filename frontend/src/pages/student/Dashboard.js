import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { RadarChart, Radar, PolarGrid, PolarAngleAxis, ResponsiveContainer, LineChart, Line, XAxis, YAxis, Tooltip, CartesianGrid } from 'recharts';
import { studentAPI, readinessAPI, jobRolesAPI } from '../../services/api';
import { Card, StatCard, LoadingSpinner, PageHeader, ProgressBar, Btn, DemoBanner, Badge } from '../../components/common/Card';
import { FiTarget, FiTrendingUp, FiZap, FiAward, FiRefreshCw, FiCheckCircle, FiAlertTriangle, FiBook } from 'react-icons/fi';
import { useAuth } from '../../context/AuthContext';
import { toast } from 'react-toastify';

const READINESS_COLOR = { 'Ready': '#10b981', 'Moderately Ready': '#f59e0b', 'Needs Improvement': '#ef4444' };
const READINESS_BADGE = { 'Ready': 'success', 'Moderately Ready': 'warning', 'Needs Improvement': 'danger' };

export default function Dashboard() {
  const { user } = useAuth();
  const [data, setData] = useState(null);
  const [roles, setRoles] = useState([]);
  const [loading, setLoading] = useState(true);
  const [recalcLoading, setRecalcLoading] = useState(false);

  const load = async () => {
    try {
      const [dashRes, rolesRes] = await Promise.all([studentAPI.getDashboard(), jobRolesAPI.list()]);
      setData(dashRes.data);
      setRoles(rolesRes.data);
    } catch (e) {
      toast.error('Failed to load dashboard');
    } finally { setLoading(false); }
  };

  useEffect(() => { load(); }, []);

  const recalculate = async () => {
    if (!data?.readiness?.job_role_id) return toast.info('Set a target role in your profile first');
    setRecalcLoading(true);
    try {
      await readinessAPI.calculate(data.readiness.job_role_id);
      toast.success('Readiness recalculated!');
      load();
    } catch { toast.error('Recalculation failed'); }
    finally { setRecalcLoading(false); }
  };

  if (loading) return <LoadingSpinner />;

  const sp = data?.skill_profile || {};
  const radarData = Object.entries(sp).map(([k, v]) => ({ subject: k.charAt(0).toUpperCase() + k.slice(1), value: Math.round(v) }));

  const historyData = (data?.performance_history || []).slice().reverse().map((h, i) => ({
    name: `T${i + 1}`, score: Math.round(h.score || 0)
  }));

  const skills = Object.entries(sp);
  const sorted = [...skills].sort((a, b) => b[1] - a[1]);
  const strengths = sorted.slice(0, 3);
  const weaknesses = sorted.slice(-3).reverse();

  return (
    <div>
      <DemoBanner message="Demo Mode – Skill scores and readiness are calculated from synthetic/demo data for prototype demonstration." />
      <PageHeader
        title={`Welcome back, ${user?.full_name?.split(' ')[0]} 👋`}
        subtitle="Here's your current placement readiness overview"
        action={<Btn onClick={recalculate} disabled={recalcLoading} variant="primary"><FiRefreshCw /> {recalcLoading ? 'Recalculating…' : 'Recalculate Readiness'}</Btn>}
      />

      {/* Stats Row */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: 16, marginBottom: 24 }}>
        <StatCard icon={<FiTarget />} label="Readiness Score" value={data?.readiness ? `${data.readiness.score?.toFixed(0)}%` : 'N/A'} color="#4f46e5" sub={data?.readiness?.category || 'Not calculated'} />
        <StatCard icon={<FiZap />} label="Target Role" value={data?.target_role || 'Not set'} color="#06b6d4" sub="Your current target" />
        <StatCard icon={<FiAward />} label="Profile Complete" value={`${data?.profile_completeness || 0}%`} color="#10b981" sub="Fill profile for better accuracy" />
        <StatCard icon={<FiTrendingUp />} label="Assessments" value={data?.recent_assessments?.length || 0} color="#f59e0b" sub="Recent test count" />
      </div>

      {/* Readiness Banner */}
      {data?.readiness && (
        <Card style={{ marginBottom: 24, background: 'linear-gradient(135deg,#1e1b4b,#2d2a6b)', color: 'white', border: 'none' }}>
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', flexWrap: 'wrap', gap: 16 }}>
            <div>
              <div style={{ fontSize: 12, color: 'rgba(255,255,255,0.5)', marginBottom: 8 }}>READINESS FOR {data.target_role?.toUpperCase()}</div>
              <div style={{ fontSize: 52, fontWeight: 800, color: READINESS_COLOR[data.readiness.category] || '#818cf8' }}>
                {data.readiness.score?.toFixed(0)}%
              </div>
              <div style={{ marginTop: 8 }}>
                <Badge label={data.readiness.category || 'Unknown'} type={READINESS_BADGE[data.readiness.category] || 'default'} />
              </div>
              <p style={{ fontSize: 12, color: 'rgba(255,255,255,0.4)', marginTop: 12 }}>
                ⚠️ Prototype score based on synthetic training data. Not a guarantee of placement.
              </p>
            </div>
            <div style={{ textAlign: 'right' }}>
              <div style={{ fontSize: 12, color: 'rgba(255,255,255,0.5)', marginBottom: 8 }}>Quick Actions</div>
              <div style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
                <Link to="/readiness" style={{ padding: '8px 16px', background: 'rgba(99,102,241,0.4)', color: 'white', borderRadius: 8, fontSize: 12, fontWeight: 600 }}>View Full Analysis</Link>
                <Link to="/recommendations" style={{ padding: '8px 16px', background: 'rgba(16,185,129,0.3)', color: 'white', borderRadius: 8, fontSize: 12, fontWeight: 600 }}>View Recommendations</Link>
              </div>
            </div>
          </div>
        </Card>
      )}

      {/* Charts + Skill cards */}
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 20, marginBottom: 24 }}>
        <Card>
          <h3 style={{ fontWeight: 700, marginBottom: 16 }}>Skill Radar Chart</h3>
          <ResponsiveContainer width="100%" height={260}>
            <RadarChart data={radarData}>
              <PolarGrid stroke="#e2e8f0" />
              <PolarAngleAxis dataKey="subject" tick={{ fontSize: 11 }} />
              <Radar name="Score" dataKey="value" stroke="#4f46e5" fill="#4f46e5" fillOpacity={0.25} />
            </RadarChart>
          </ResponsiveContainer>
        </Card>
        <Card>
          <h3 style={{ fontWeight: 700, marginBottom: 16 }}>Readiness Trend</h3>
          {historyData.length > 0 ? (
            <ResponsiveContainer width="100%" height={260}>
              <LineChart data={historyData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" />
                <XAxis dataKey="name" tick={{ fontSize: 11 }} />
                <YAxis domain={[0, 100]} tick={{ fontSize: 11 }} />
                <Tooltip />
                <Line type="monotone" dataKey="score" stroke="#4f46e5" strokeWidth={2} dot={{ r: 4 }} />
              </LineChart>
            </ResponsiveContainer>
          ) : (
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', height: 260, color: '#94a3b8', flexDirection: 'column', gap: 8 }}>
              <FiTrendingUp size={32} />
              <p>Calculate readiness to see your trend</p>
            </div>
          )}
        </Card>
      </div>

      {/* Skill scores */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: 16, marginBottom: 24 }}>
        {Object.entries(sp).map(([skill, score]) => (
          <Card key={skill} style={{ padding: 16 }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 8 }}>
              <span style={{ fontWeight: 600, fontSize: 13, textTransform: 'capitalize' }}>{skill}</span>
              <span style={{ fontWeight: 700, color: score >= 70 ? '#10b981' : score >= 50 ? '#f59e0b' : '#ef4444' }}>{Math.round(score)}</span>
            </div>
            <ProgressBar value={score} color={score >= 70 ? '#10b981' : score >= 50 ? '#f59e0b' : '#ef4444'} showLabel={false} />
          </Card>
        ))}
      </div>

      {/* Strengths & Weaknesses */}
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', gap: 16, marginBottom: 24 }}>
        <Card>
          <h3 style={{ fontWeight: 700, marginBottom: 12, display: 'flex', alignItems: 'center', gap: 8, color: '#10b981' }}><FiCheckCircle /> Strengths</h3>
          {strengths.map(([k, v]) => <div key={k} style={{ display: 'flex', justifyContent: 'space-between', padding: '8px 0', borderBottom: '1px solid #f1f5f9', fontSize: 13 }}>
            <span style={{ textTransform: 'capitalize' }}>{k}</span><span style={{ fontWeight: 700, color: '#10b981' }}>{Math.round(v)}/100</span>
          </div>)}
        </Card>
        <Card>
          <h3 style={{ fontWeight: 700, marginBottom: 12, display: 'flex', alignItems: 'center', gap: 8, color: '#ef4444' }}><FiAlertTriangle /> Weaknesses</h3>
          {weaknesses.map(([k, v]) => <div key={k} style={{ display: 'flex', justifyContent: 'space-between', padding: '8px 0', borderBottom: '1px solid #f1f5f9', fontSize: 13 }}>
            <span style={{ textTransform: 'capitalize' }}>{k}</span><span style={{ fontWeight: 700, color: '#ef4444' }}>{Math.round(v)}/100</span>
          </div>)}
        </Card>
        <Card>
          <h3 style={{ fontWeight: 700, marginBottom: 12, display: 'flex', alignItems: 'center', gap: 8, color: '#f59e0b' }}><FiBook /> Recent Tests</h3>
          {(data?.recent_assessments || []).slice(0, 4).map((a, i) => (
            <div key={i} style={{ display: 'flex', justifyContent: 'space-between', padding: '8px 0', borderBottom: '1px solid #f1f5f9', fontSize: 13 }}>
              <span style={{ textTransform: 'capitalize' }}>{a.type}</span>
              <span style={{ fontWeight: 700, color: a.score >= 70 ? '#10b981' : '#f59e0b' }}>{a.score?.toFixed(0)}%</span>
            </div>
          ))}
          {!data?.recent_assessments?.length && <p style={{ color: '#94a3b8', fontSize: 13 }}>No tests taken yet. <Link to="/assessment/aptitude" style={{ color: '#4f46e5' }}>Take a test</Link></p>}
        </Card>
      </div>
    </div>
  );
}
