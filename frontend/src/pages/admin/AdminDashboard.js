import React, { useState, useEffect } from 'react';
import { adminAPI } from '../../services/api';
import { Card, StatCard, LoadingSpinner, PageHeader, DemoBanner } from '../../components/common/Card';
import { PieChart, Pie, Cell, Tooltip, ResponsiveContainer, BarChart, Bar, XAxis, YAxis, CartesianGrid, Legend } from 'recharts';

const COLORS = ['#10b981', '#f59e0b', '#ef4444'];

export default function AdminDashboard() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => { adminAPI.getDashboard().then(r => setData(r.data)).finally(() => setLoading(false)); }, []);

  if (loading) return <LoadingSpinner />;
  if (!data) return <div>Failed to load</div>;

  const pieData = [
    { name: 'Ready', value: data.students_ready },
    { name: 'Mod. Ready', value: data.students_moderately_ready },
    { name: 'Needs Work', value: data.students_needs_improvement },
  ];

  const skillData = Object.entries(data.skill_averages || {}).map(([k, v]) => ({ skill: k.toUpperCase(), avg: v }));
  const deptData = (data.department_comparison || []).slice(0, 6);

  return (
    <div>
      <DemoBanner message="Admin dashboard shows data for demo students. All scores are synthetic prototype data." />
      <PageHeader title="Placement Officer Dashboard" subtitle="Batch-level placement readiness overview" />

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(180px, 1fr))', gap: 16, marginBottom: 24 }}>
        <StatCard icon="👥" label="Total Students" value={data.total_students} color="#4f46e5" />
        <StatCard icon="📊" label="Avg. Readiness" value={`${data.average_readiness}%`} color="#06b6d4" />
        <StatCard icon="✅" label="Ready" value={data.students_ready} color="#10b981" />
        <StatCard icon="⚠️" label="Needs Improvement" value={data.students_needs_improvement} color="#ef4444" />
        <StatCard icon="📝" label="Assessments" value={data.assessment_count} color="#8b5cf6" />
        <StatCard icon="🎯" label="Weakest Skill" value={data.most_common_weak_skill?.toUpperCase()} color="#f59e0b" />
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 20, marginBottom: 20 }}>
        <Card>
          <h3 style={{ fontWeight: 700, marginBottom: 16, fontSize: 15 }}>Readiness Distribution</h3>
          <ResponsiveContainer width="100%" height={240}>
            <PieChart>
              <Pie data={pieData} cx="50%" cy="50%" outerRadius={90} dataKey="value" label={({ name, value }) => `${name}: ${value}`} labelLine={false}>
                {pieData.map((_, i) => <Cell key={i} fill={COLORS[i]} />)}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        </Card>
        <Card>
          <h3 style={{ fontWeight: 700, marginBottom: 16, fontSize: 15 }}>Average Skill Scores</h3>
          <ResponsiveContainer width="100%" height={240}>
            <BarChart data={skillData} margin={{ left: 0 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" />
              <XAxis dataKey="skill" tick={{ fontSize: 9 }} />
              <YAxis domain={[0, 100]} tick={{ fontSize: 10 }} />
              <Tooltip />
              <Bar dataKey="avg" fill="#4f46e5" radius={[4, 4, 0, 0]} name="Average Score" />
            </BarChart>
          </ResponsiveContainer>
        </Card>
      </div>

      {deptData.length > 0 && (
        <Card>
          <h3 style={{ fontWeight: 700, marginBottom: 16, fontSize: 15 }}>Department Readiness Comparison</h3>
          <ResponsiveContainer width="100%" height={200}>
            <BarChart data={deptData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" />
              <XAxis dataKey="department" tick={{ fontSize: 11 }} />
              <YAxis domain={[0, 100]} tick={{ fontSize: 10 }} />
              <Tooltip />
              <Bar dataKey="avg_readiness" fill="#06b6d4" radius={[4, 4, 0, 0]} name="Avg Readiness %" />
            </BarChart>
          </ResponsiveContainer>
        </Card>
      )}
    </div>
  );
}
