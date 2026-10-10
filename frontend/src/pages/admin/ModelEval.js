import React, { useState, useEffect } from 'react';
import { adminAPI } from '../../services/api';
import { Card, PageHeader, LoadingSpinner, DemoBanner, StatCard } from '../../components/common/Card';

export default function ModelEval() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => { adminAPI.getModelEval().then(r => setData(r.data)).finally(() => setLoading(false)); }, []);

  if (loading) return <LoadingSpinner />;
  if (!data) return null;

  const cm = data.confusion_matrix || [];
  const labels = data.class_labels || [];

  return (
    <div>
      <DemoBanner message="Demo model trained on SYNTHETIC data. Metrics shown are from the demo training run. Replace with real placement data for production." />
      <PageHeader title="Model Evaluation" subtitle="Random Forest performance metrics on demo/synthetic dataset" />

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit,minmax(160px,1fr))', gap: 16, marginBottom: 24 }}>
        <StatCard icon="🎯" label="Accuracy" value={`${(data.accuracy * 100).toFixed(1)}%`} color="#4f46e5" />
        <StatCard icon="🎯" label="Precision" value={`${(data.precision * 100).toFixed(1)}%`} color="#10b981" />
        <StatCard icon="📡" label="Recall" value={`${(data.recall * 100).toFixed(1)}%`} color="#06b6d4" />
        <StatCard icon="⚖️" label="F1 Score" value={`${(data.f1_score * 100).toFixed(1)}%`} color="#8b5cf6" />
        <StatCard icon="📊" label="Train Samples" value={data.training_samples} color="#f59e0b" />
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 20 }}>
        <Card>
          <h3 style={{ fontWeight: 700, marginBottom: 4, fontSize: 15 }}>Confusion Matrix</h3>
          <p style={{ fontSize: 12, color: '#94a3b8', marginBottom: 20 }}>Rows = Actual class · Columns = Predicted class</p>
          {cm.length > 0 && (
            <table style={{ borderCollapse: 'collapse', margin: '0 auto' }}>
              <thead>
                <tr>
                  <th style={{ padding: '8px 12px', fontSize: 11, color: '#64748b' }}></th>
                  {labels.map(l => <th key={l} style={{ padding: '8px 12px', fontSize: 11, fontWeight: 700, color: '#64748b', textAlign: 'center' }}>Pred: {l.split(' ')[0]}</th>)}
                </tr>
              </thead>
              <tbody>
                {cm.map((row, i) => (
                  <tr key={i}>
                    <td style={{ padding: '8px 12px', fontSize: 11, fontWeight: 700, color: '#64748b', whiteSpace: 'nowrap' }}>Act: {labels[i]?.split(' ')[0]}</td>
                    {row.map((val, j) => (
                      <td key={j} style={{ padding: '16px 24px', textAlign: 'center', background: i === j ? '#d1fae5' : val > 0 ? '#fee2e2' : '#f8fafc', fontWeight: 700, fontSize: 18, color: i === j ? '#065f46' : val > 0 ? '#991b1b' : '#94a3b8', border: '2px solid white', borderRadius: 4 }}>{val}</td>
                    ))}
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </Card>

        <Card>
          <h3 style={{ fontWeight: 700, marginBottom: 16, fontSize: 15 }}>Model Details</h3>
          <div style={{ fontSize: 13, lineHeight: 2 }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', padding: '6px 0', borderBottom: '1px solid #f1f5f9' }}>
              <span style={{ color: '#64748b' }}>Algorithm</span><span style={{ fontWeight: 600 }}>Random Forest</span>
            </div>
            <div style={{ display: 'flex', justifyContent: 'space-between', padding: '6px 0', borderBottom: '1px solid #f1f5f9' }}>
              <span style={{ color: '#64748b' }}>Estimators</span><span style={{ fontWeight: 600 }}>100 trees</span>
            </div>
            <div style={{ display: 'flex', justifyContent: 'space-between', padding: '6px 0', borderBottom: '1px solid #f1f5f9' }}>
              <span style={{ color: '#64748b' }}>Max Depth</span><span style={{ fontWeight: 600 }}>10</span>
            </div>
            <div style={{ display: 'flex', justifyContent: 'space-between', padding: '6px 0', borderBottom: '1px solid #f1f5f9' }}>
              <span style={{ color: '#64748b' }}>Features</span><span style={{ fontWeight: 600 }}>{data.features?.length || 12}</span>
            </div>
            <div style={{ display: 'flex', justifyContent: 'space-between', padding: '6px 0', borderBottom: '1px solid #f1f5f9' }}>
              <span style={{ color: '#64748b' }}>Classes</span><span style={{ fontWeight: 600 }}>{labels.join(', ')}</span>
            </div>
            <div style={{ display: 'flex', justifyContent: 'space-between', padding: '6px 0', borderBottom: '1px solid #f1f5f9' }}>
              <span style={{ color: '#64748b' }}>Data Type</span>
              <span style={{ fontWeight: 600, color: '#f59e0b' }}>⚠️ {data.is_demo_data ? 'Synthetic Demo' : 'Real'}</span>
            </div>
          </div>
          <div style={{ marginTop: 16, padding: 14, background: '#fff7ed', borderRadius: 8, fontSize: 12, color: '#92400e', lineHeight: 1.7 }}>
            <strong>{data.note}</strong>
          </div>
        </Card>
      </div>

      <Card style={{ marginTop: 20 }}>
        <h3 style={{ fontWeight: 700, marginBottom: 12, fontSize: 15 }}>Feature Importance (12 Features)</h3>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill,minmax(200px,1fr))', gap: 10 }}>
          {(data.features || []).map((f, i) => (
            <div key={i} style={{ padding: '10px 14px', background: '#f8fafc', borderRadius: 8, fontSize: 13 }}>
              <div style={{ fontWeight: 600, textTransform: 'capitalize' }}>{f.replace('_score', '').replace('_', ' ')}</div>
              <div style={{ height: 6, background: '#e2e8f0', borderRadius: 999, marginTop: 6 }}>
                <div style={{ width: `${Math.max(10, 100 - i * 7)}%`, height: '100%', background: '#4f46e5', borderRadius: 999 }} />
              </div>
            </div>
          ))}
        </div>
      </Card>
    </div>
  );
}
