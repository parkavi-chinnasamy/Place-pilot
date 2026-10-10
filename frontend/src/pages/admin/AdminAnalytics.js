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

      <Card>
        <h3 style={{ fontWeight: 700, marginBottom: 12, fontSize: 15 }}>About the ML Model</h3>
        <div style={{ background: '#f8fafc', borderRadius: 10, padding: 20, fontSize: 13, lineHeight: 1.9, color: '#475569' }}>
          <p><strong>Algorithm:</strong> Random Forest Classifier (scikit-learn)</p>
          <p><strong>Features:</strong> Academic score, DSA, Programming, DBMS, OOP, Aptitude, Coding Test, Technical Test, Interview, Resume, LeetCode, Communication (12 features)</p>
          <p><strong>Target:</strong> Ready / Moderately Ready / Needs Improvement</p>
          <p><strong>Training data:</strong> 800 synthetic samples (demo data — clearly labelled)</p>
          <p><strong>Explainability:</strong> SHAP TreeExplainer</p>
          <p style={{ color: '#92400e', background: '#fff7ed', padding: '8px 12px', borderRadius: 6, marginTop: 8 }}>
            ⚠️ Scores are prototype outputs from synthetic training data. See Model Evaluation page for accuracy metrics.
          </p>
        </div>
      </Card>
    </div>
  );
}
