import React, { useState, useEffect } from 'react';
import { adminAPI } from '../../services/api';
import { Card, PageHeader, LoadingSpinner, DemoBanner } from '../../components/common/Card';
import { LineChart, Line, XAxis, YAxis, Tooltip, CartesianGrid, ResponsiveContainer } from 'recharts';

export default function AdminAnalytics() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => { adminAPI.getAnalytics().then(r => setData(r.data)).finally(() => setLoading(false)); }, []);

  if (loading) return <LoadingSpinner />;

  return (
    <div>
      <DemoBanner />
      <PageHeader title="Analytics" subtitle="Batch-level performance trends and statistics" />
      <Card style={{ marginBottom: 24 }}>
        <h3 style={{ fontWeight: 700, marginBottom: 4, fontSize: 15 }}>Readiness Trend (Last 30 Days)</h3>
        <p style={{ fontSize: 12, color: '#94a3b8', marginBottom: 16 }}>Average readiness score across all students over time</p>
        {data?.readiness_trend?.length > 0 ? (
          <ResponsiveContainer width="100%" height={280}>
            <LineChart data={data.readiness_trend}>
              <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" />
              <XAxis dataKey="date" tick={{ fontSize: 11 }} />
              <YAxis domain={[0, 100]} tick={{ fontSize: 11 }} />
              <Tooltip />
              <Line type="monotone" dataKey="avg_readiness" stroke="#4f46e5" strokeWidth={2.5} dot={{ r: 4 }} name="Avg Readiness %" />
            </LineChart>
          </ResponsiveContainer>
        ) : (
          <div style={{ textAlign: 'center', padding: 80, color: '#94a3b8' }}>
            <p style={{ fontSize: 14 }}>No trend data yet. Readiness calculations by students will appear here.</p>
          </div>
        )}
      </Card>

      {/* Assessment Activity Overview */}
      {data?.assessment_stats && (
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: 16, marginBottom: 24 }}>
          <Card style={{ padding: 18 }}>
            <div style={{ fontSize: 12, color: '#64748b', fontWeight: 600 }}>Completed Assessments</div>
            <div style={{ fontSize: 28, fontWeight: 800, color: '#10b981', marginTop: 4 }}>
              {data.assessment_stats.total_completed}
            </div>
          </Card>
          <Card style={{ padding: 18 }}>
            <div style={{ fontSize: 12, color: '#64748b', fontWeight: 600 }}>In-Progress Assessments</div>
            <div style={{ fontSize: 28, fontWeight: 800, color: '#f59e0b', marginTop: 4 }}>
              {data.assessment_stats.total_in_progress}
            </div>
          </Card>
          {Object.entries(data.assessment_stats.by_type || {}).map(([typeKey, stats]) => (
            <Card key={typeKey} style={{ padding: 18 }}>
              <div style={{ fontSize: 12, color: '#64748b', fontWeight: 600, textTransform: 'capitalize' }}>{typeKey} Tests</div>
              <div style={{ fontSize: 22, fontWeight: 800, color: '#1e293b', marginTop: 4 }}>
                {stats.completed} <span style={{ fontSize: 13, fontWeight: 500, color: '#64748b' }}>completed</span>
              </div>
              <div style={{ fontSize: 12, color: '#4f46e5', fontWeight: 600, marginTop: 2 }}>
                Avg Score: {stats.avg_score}%
              </div>
            </Card>
          ))}
        </div>
      )}


    </div>
  );
}
