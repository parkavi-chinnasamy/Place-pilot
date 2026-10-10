import React, { useState, useEffect } from 'react';
import { readinessAPI, assessmentAPI } from '../../services/api';
import { Card, PageHeader, LoadingSpinner, DemoBanner, Badge } from '../../components/common/Card';
import { LineChart, Line, XAxis, YAxis, Tooltip, CartesianGrid, ResponsiveContainer, Legend } from 'recharts';

export default function History() {
  const [readinessHistory, setReadinessHistory] = useState([]);
  const [assessmentHistory, setAssessmentHistory] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.all([
      readinessAPI.getHistory(),
      assessmentAPI.getHistory(),
    ]).then(([rh, ah]) => {
      setReadinessHistory(rh.data || []);
      setAssessmentHistory(ah.data || []);
    }).catch(() => {}).finally(() => setLoading(false));
  }, []);

  if (loading) return <LoadingSpinner />;

  const chartData = [...readinessHistory].reverse().map((h, i) => ({
    name: new Date(h.recorded_at).toLocaleDateString('en-US', { month: 'short', day: 'numeric' }),
    readiness: Math.round(h.readiness_score || 0),
  }));

  const RC_COLOR = { 'Ready': 'success', 'Moderately Ready': 'warning', 'Needs Improvement': 'danger' };

  return (
    <div>
      <DemoBanner />
      <PageHeader title="Progress History" subtitle="Track your improvement over time" />

      {/* Readiness Trend */}
      <Card style={{ marginBottom: 24 }}>
        <h3 style={{ fontWeight: 700, marginBottom: 4, fontSize: 15 }}>Readiness Score Over Time</h3>
        <p style={{ fontSize: 12, color: '#94a3b8', marginBottom: 16 }}>Each point = one readiness calculation</p>
        {chartData.length > 1 ? (
          <ResponsiveContainer width="100%" height={260}>
            <LineChart data={chartData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" />
              <XAxis dataKey="name" tick={{ fontSize: 11 }} />
              <YAxis domain={[0, 100]} tick={{ fontSize: 11 }} />
              <Tooltip />
              <Line type="monotone" dataKey="readiness" stroke="#4f46e5" strokeWidth={2.5} dot={{ r: 5, fill: '#4f46e5' }} name="Readiness %" />
            </LineChart>
          </ResponsiveContainer>
        ) : (
          <div style={{ textAlign: 'center', padding: 60, color: '#94a3b8' }}>
            <p>Calculate your readiness multiple times to see your trend here</p>
          </div>
        )}
      </Card>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 20 }}>
        {/* Readiness history table */}
        <Card>
          <h3 style={{ fontWeight: 700, marginBottom: 16, fontSize: 15 }}>Readiness History</h3>
          {readinessHistory.length > 0 ? (
            <div style={{ overflowX: 'auto' }}>
              <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: 13 }}>
                <thead>
                  <tr style={{ background: '#f8fafc' }}>
                    <th style={{ padding: '8px 12px', textAlign: 'left', fontSize: 11, fontWeight: 700, color: '#64748b', textTransform: 'uppercase' }}>Date</th>
                    <th style={{ padding: '8px 12px', textAlign: 'left', fontSize: 11, fontWeight: 700, color: '#64748b', textTransform: 'uppercase' }}>Score</th>
                    <th style={{ padding: '8px 12px', textAlign: 'left', fontSize: 11, fontWeight: 700, color: '#64748b', textTransform: 'uppercase' }}>Category</th>
                  </tr>
                </thead>
                <tbody>
                  {readinessHistory.map((h, i) => (
                    <tr key={i} style={{ borderBottom: '1px solid #f1f5f9' }}>
                      <td style={{ padding: '10px 12px', color: '#64748b' }}>{new Date(h.recorded_at).toLocaleDateString()}</td>
                      <td style={{ padding: '10px 12px', fontWeight: 700, color: '#4f46e5' }}>{h.readiness_score?.toFixed(0)}%</td>
                      <td style={{ padding: '10px 12px' }}><Badge label={h.readiness_category || 'Unknown'} type={RC_COLOR[h.readiness_category] || 'default'} /></td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          ) : <p style={{ color: '#94a3b8', fontSize: 13 }}>No readiness history yet. Calculate your readiness to start tracking.</p>}
        </Card>

        {/* Assessment history table */}
        <Card>
          <h3 style={{ fontWeight: 700, marginBottom: 16, fontSize: 15 }}>Assessment History</h3>
          {assessmentHistory.length > 0 ? (
            <div style={{ overflowX: 'auto' }}>
              <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: 13 }}>
                <thead>
                  <tr style={{ background: '#f8fafc' }}>
                    <th style={{ padding: '8px 12px', textAlign: 'left', fontSize: 11, fontWeight: 700, color: '#64748b', textTransform: 'uppercase' }}>Type</th>
                    <th style={{ padding: '8px 12px', textAlign: 'left', fontSize: 11, fontWeight: 700, color: '#64748b', textTransform: 'uppercase' }}>Score</th>
                    <th style={{ padding: '8px 12px', textAlign: 'left', fontSize: 11, fontWeight: 700, color: '#64748b', textTransform: 'uppercase' }}>Result</th>
                    <th style={{ padding: '8px 12px', textAlign: 'left', fontSize: 11, fontWeight: 700, color: '#64748b', textTransform: 'uppercase' }}>Date</th>
                  </tr>
                </thead>
                <tbody>
                  {assessmentHistory.map((a, i) => (
                    <tr key={i} style={{ borderBottom: '1px solid #f1f5f9' }}>
                      <td style={{ padding: '10px 12px', fontWeight: 600, textTransform: 'capitalize' }}>{a.type}</td>
                      <td style={{ padding: '10px 12px', fontWeight: 700, color: a.score >= 70 ? '#10b981' : a.score >= 50 ? '#f59e0b' : '#ef4444' }}>{a.score?.toFixed(0)}%</td>
                      <td style={{ padding: '10px 12px', color: '#64748b', fontSize: 12 }}>{a.correct_answers}/{a.total_questions}</td>
                      <td style={{ padding: '10px 12px', color: '#94a3b8', fontSize: 12 }}>{new Date(a.completed_at).toLocaleDateString()}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          ) : <p style={{ color: '#94a3b8', fontSize: 13 }}>No assessments taken yet. <a href="/assessment/aptitude" style={{ color: '#4f46e5' }}>Take a test now</a></p>}
        </Card>
      </div>
    </div>
  );
}
