import React, { useState, useEffect, useRef } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { assessmentAPI } from '../../services/api';
import { Card, PageHeader, Btn, LoadingSpinner } from '../../components/common/Card';
import { toast } from 'react-toastify';
import { FiClock, FiCheck, FiX } from 'react-icons/fi';

const TYPE_LABELS = { aptitude: 'Aptitude Test', coding: 'Coding (MCQ) Test', technical: 'Technical / DBMS Test' };
const TYPE_TIME = { aptitude: 20, coding: 25, technical: 20 }; // minutes

export default function Assessment() {
  const { type } = useParams();
  const navigate = useNavigate();
  const [phase, setPhase] = useState('intro'); // intro | test | result
  const [questions, setQuestions] = useState([]);
  const [answers, setAnswers] = useState({});
  const [current, setCurrent] = useState(0);
  const [result, setResult] = useState(null);
  const [timeLeft, setTimeLeft] = useState(0);
  const [loading, setLoading] = useState(false);
  const timerRef = useRef(null);
  const startTime = useRef(null);

  const loadQuestions = async () => {
    setLoading(true);
    try {
      const res = await assessmentAPI.getQuestions(type, 15);
      setQuestions(res.data);
      setPhase('test');
      setTimeLeft(TYPE_TIME[type] * 60);
      startTime.current = Date.now();
    } catch { toast.error('Failed to load questions'); }
    finally { setLoading(false); }
  };

  useEffect(() => {
    if (phase === 'test') {
      timerRef.current = setInterval(() => {
        setTimeLeft(t => {
          if (t <= 1) { clearInterval(timerRef.current); submitTest(); return 0; }
          return t - 1;
        });
      }, 1000);
    }
    return () => clearInterval(timerRef.current);
  }, [phase]);

  const submitTest = async () => {
    clearInterval(timerRef.current);
    const elapsed = Math.round((Date.now() - (startTime.current || Date.now())) / 1000);
    const payload = {
      assessment_type: type,
      answers: questions.map(q => ({ question_id: q.id, selected_option: answers[q.id] || 'A' })),
      time_taken_secs: elapsed,
    };
    setLoading(true);
    try {
      const res = await assessmentAPI.submit(payload);
      setResult(res.data);
      setPhase('result');
    } catch { toast.error('Submission failed'); }
    finally { setLoading(false); }
  };

  const fmt = (s) => `${Math.floor(s / 60).toString().padStart(2, '0')}:${(s % 60).toString().padStart(2, '0')}`;
  const answered = Object.keys(answers).length;

  if (phase === 'intro') return (
    <div style={{ maxWidth: 600, margin: '0 auto' }}>
      <PageHeader title={TYPE_LABELS[type] || 'Assessment'} subtitle={`Test your ${type} knowledge`} />
      <Card style={{ textAlign: 'center', padding: 40 }}>
        <div style={{ fontSize: 64, marginBottom: 20 }}>📝</div>
        <h2 style={{ fontSize: 20, fontWeight: 700, marginBottom: 16 }}>{TYPE_LABELS[type]}</h2>
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', gap: 16, marginBottom: 32 }}>
          {[['Questions', '15'], ['Time Limit', `${TYPE_TIME[type]} mins`], ['Type', 'MCQ']].map(([l, v]) => (
            <div key={l} style={{ background: '#f8fafc', borderRadius: 10, padding: 16 }}>
              <div style={{ fontSize: 22, fontWeight: 800, color: '#4f46e5' }}>{v}</div>
              <div style={{ fontSize: 12, color: '#64748b', marginTop: 4 }}>{l}</div>
            </div>
          ))}
        </div>
        <ul style={{ textAlign: 'left', marginBottom: 32, paddingLeft: 20, color: '#475569', fontSize: 14, lineHeight: 2 }}>
          <li>Each question has 4 options — only one is correct</li>
          <li>You can navigate between questions using the panel on the right</li>
          <li>The timer auto-submits when time runs out</li>
          <li>Results and explanations are shown after submission</li>
        </ul>
        <Btn onClick={loadQuestions} disabled={loading} size="lg">
          {loading ? 'Loading…' : '▶ Start Test'}
        </Btn>
      </Card>
    </div>
  );

  if (phase === 'test' && questions.length > 0) {
    const q = questions[current];
    return (
      <div>
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: 20 }}>
          <div>
            <h2 style={{ fontWeight: 700 }}>{TYPE_LABELS[type]}</h2>
            <p style={{ color: '#64748b', fontSize: 13 }}>Question {current + 1} of {questions.length} · {answered} answered</p>
          </div>
          <div style={{ display: 'flex', alignItems: 'center', gap: 8, background: timeLeft < 120 ? '#fee2e2' : '#f1f5f9', padding: '8px 16px', borderRadius: 10, fontWeight: 700, color: timeLeft < 120 ? '#ef4444' : '#1e293b' }}>
            <FiClock /> {fmt(timeLeft)}
          </div>
        </div>

        <div style={{ display: 'grid', gridTemplateColumns: '1fr 280px', gap: 20 }}>
          <Card>
            <div style={{ marginBottom: 6, fontSize: 11, fontWeight: 700, color: '#64748b', textTransform: 'uppercase' }}>{q.topic} · {q.difficulty}</div>
            <p style={{ fontSize: 15, fontWeight: 600, lineHeight: 1.7, marginBottom: 24 }}>{q.question_text}</p>
            {['A', 'B', 'C', 'D'].map(opt => (
              <button key={opt} onClick={() => setAnswers({ ...answers, [q.id]: opt })}
                style={{ width: '100%', textAlign: 'left', padding: '12px 16px', marginBottom: 10, border: `2px solid ${answers[q.id] === opt ? '#4f46e5' : '#e2e8f0'}`, background: answers[q.id] === opt ? '#eef2ff' : 'white', borderRadius: 10, cursor: 'pointer', fontSize: 14, fontWeight: answers[q.id] === opt ? 600 : 400, display: 'flex', alignItems: 'flex-start', gap: 12 }}>
                <span style={{ width: 28, height: 28, borderRadius: '50%', background: answers[q.id] === opt ? '#4f46e5' : '#f1f5f9', color: answers[q.id] === opt ? 'white' : '#475569', display: 'flex', alignItems: 'center', justifyContent: 'center', fontWeight: 700, fontSize: 12, flexShrink: 0 }}>{opt}</span>
                {q[`option_${opt.toLowerCase()}`]}
              </button>
            ))}
          </Card>

          <div>
            <Card style={{ marginBottom: 16 }}>
              <div style={{ fontWeight: 700, marginBottom: 12, fontSize: 13 }}>Question Navigator</div>
              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(5, 1fr)', gap: 6 }}>
                {questions.map((_, i) => (
                  <button key={i} onClick={() => setCurrent(i)}
                    style={{ padding: '8px 4px', borderRadius: 8, border: `2px solid ${i === current ? '#4f46e5' : answers[questions[i].id] ? '#10b981' : '#e2e8f0'}`, background: i === current ? '#eef2ff' : answers[questions[i].id] ? '#d1fae5' : 'white', cursor: 'pointer', fontWeight: 700, fontSize: 12 }}>
                    {i + 1}
                  </button>
                ))}
              </div>
            </Card>
            <div style={{ display: 'flex', gap: 8 }}>
              <Btn onClick={() => setCurrent(Math.max(0, current - 1))} variant="secondary" size="sm" disabled={current === 0} style={{ flex: 1 }}>← Prev</Btn>
              <Btn onClick={() => setCurrent(Math.min(questions.length - 1, current + 1))} variant="secondary" size="sm" disabled={current === questions.length - 1} style={{ flex: 1 }}>Next →</Btn>
            </div>
            <Btn onClick={submitTest} variant="success" style={{ width: '100%', marginTop: 12, justifyContent: 'center' }} disabled={loading}>
              {loading ? 'Submitting…' : '✓ Submit Test'}
            </Btn>
          </div>
        </div>
      </div>
    );
  }

  if (phase === 'result' && result) return (
    <div>
      <PageHeader title="Test Results" subtitle="Here's how you did" />
      <Card style={{ marginBottom: 20, background: result.score >= 70 ? 'linear-gradient(135deg,#065f46,#047857)' : result.score >= 50 ? 'linear-gradient(135deg,#78350f,#92400e)' : 'linear-gradient(135deg,#7f1d1d,#991b1b)', color: 'white', border: 'none' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: 16 }}>
          <div>
            <div style={{ fontSize: 48, fontWeight: 800 }}>{result.score?.toFixed(0)}%</div>
            <div style={{ fontSize: 16, opacity: 0.8, marginTop: 4 }}>{result.correct_answers} / {result.total_questions} correct · {result.time_taken_secs}s</div>
          </div>
          <div style={{ display: 'flex', gap: 12 }}>
            <Btn onClick={() => navigate('/dashboard')} variant="secondary">Dashboard</Btn>
            <Btn onClick={() => { setPhase('intro'); setAnswers({}); setCurrent(0); }} style={{ background: 'rgba(255,255,255,0.2)', color: 'white', border: '1px solid rgba(255,255,255,0.3)' }}>Retake</Btn>
          </div>
        </div>
      </Card>

      <div style={{ display: 'flex', flexDirection: 'column', gap: 12 }}>
        {(result.results || []).map((r, i) => (
          <Card key={i} style={{ borderLeft: `4px solid ${r.is_correct ? '#10b981' : '#ef4444'}`, padding: '14px 20px' }}>
            <div style={{ display: 'flex', alignItems: 'flex-start', gap: 12 }}>
              <div style={{ flexShrink: 0, marginTop: 2 }}>{r.is_correct ? <FiCheck color="#10b981" size={18} /> : <FiX color="#ef4444" size={18} />}</div>
              <div style={{ flex: 1 }}>
                <div style={{ fontWeight: 600, fontSize: 14, marginBottom: 8 }}>Q{i + 1}: {r.question_text}</div>
                <div style={{ fontSize: 13, color: '#64748b', marginBottom: 4 }}>Your answer: <strong style={{ color: r.is_correct ? '#10b981' : '#ef4444' }}>{r.selected_option}</strong> · Correct: <strong style={{ color: '#10b981' }}>{r.correct_option}</strong></div>
                {r.explanation && <div style={{ fontSize: 12, background: '#f8fafc', padding: '8px 12px', borderRadius: 6, color: '#475569', marginTop: 6 }}>💡 {r.explanation}</div>}
              </div>
            </div>
          </Card>
        ))}
      </div>
    </div>
  );

  return <LoadingSpinner />;
}
