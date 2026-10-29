import React, { useState, useEffect, useRef } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { assessmentAPI } from '../../services/api';
import { Card, PageHeader, Btn, LoadingSpinner, Badge } from '../../components/common/Card';
import { toast } from 'react-toastify';
import { FiClock, FiCheck, FiX, FiHelpCircle, FiAward, FiLayers, FiSliders, FiRotateCcw } from 'react-icons/fi';

const TYPE_LABELS = {
  aptitude: 'Aptitude Test',
  coding: 'Coding (MCQ) Test',
  technical: 'Technical / Core Test'
};

const DIFFICULTY_LABELS = {
  all: 'All Difficulties',
  easy: 'Easy',
  medium: 'Medium',
  hard: 'Hard'
};

export default function Assessment() {
  const { type } = useParams();
  const navigate = useNavigate();

  // Test setup states
  const [phase, setPhase] = useState('intro'); // 'intro' | 'test' | 'result'
  const [meta, setMeta] = useState(null);
  const [statusInfo, setStatusInfo] = useState(null);
  const [selectedTopic, setSelectedTopic] = useState('all');
  const [selectedDifficulty, setSelectedDifficulty] = useState('all');
  // questionCount removed – backend default will be used

  // Active test states
  const [assessmentId, setAssessmentId] = useState(null);
  const [questions, setQuestions] = useState([]);
  const [answers, setAnswers] = useState({});
  const [current, setCurrent] = useState(0);
  const [result, setResult] = useState(null);
  const [timeLeft, setTimeLeft] = useState(0);
  const [loading, setLoading] = useState(false);

  const timerRef = useRef(null);
  const startTime = useRef(null);

  // Load metadata and previous completion status on mount/type change
  useEffect(() => {
    let isMounted = true;
    setLoading(true);
    setPhase('intro');
    setAnswers({});
    setCurrent(0);
    setResult(null);

    Promise.all([
      assessmentAPI.getMeta(type).catch(() => ({ data: null })),
      assessmentAPI.getStatus().catch(() => ({ data: {} }))
    ]).then(([metaRes, statusRes]) => {
      if (!isMounted) return;
      if (metaRes.data) setMeta(metaRes.data);
      if (statusRes.data && statusRes.data[type]) {
        setStatusInfo(statusRes.data[type]);
      }
    }).finally(() => {
      if (isMounted) setLoading(false);
    });

    return () => { isMounted = false; };
  }, [type]);

  // Reset test state when filters change
  useEffect(() => {
    // Reset any lingering state before starting a new test
    setQuestions([]);
    setAnswers({});
    setCurrent(0);
    setResult(null);
    setPhase('intro');
  }, [selectedTopic, selectedDifficulty]);

  // Timer effect
  useEffect(() => {
    if (phase === 'test') {
      timerRef.current = setInterval(() => {
        setTimeLeft(t => {
          if (t <= 1) {
            clearInterval(timerRef.current);
            submitTest();
            return 0;
          }
          return t - 1;
        });
      }, 1000);
    }
    return () => clearInterval(timerRef.current);
  }, [phase]);

  const startTest = async () => {
    setLoading(true);
    try {
      const res = await assessmentAPI.start({
        assessment_type: type,
        topic: selectedTopic === 'all' ? null : selectedTopic,
        difficulty: selectedDifficulty === 'all' ? null : selectedDifficulty

      });

      if (!res.data.questions || res.data.questions.length === 0) {
        toast.error('No questions available with the selected filters.');
        return;
      }

      setAssessmentId(res.data.assessment_id);
      setQuestions(res.data.questions);
      setAnswers({});
      setCurrent(0);
      setPhase('test');

      // Estimate time: ~90 seconds per question
      const totalSecs = Math.max(120, res.data.questions.length * 90);
      setTimeLeft(totalSecs);
      startTime.current = Date.now();
      toast.success(`Test started! Total questions: ${res.data.questions.length}`);
    } catch (err) {
      if (err.response && err.response.status === 404) {
        const msg = err.response.data?.detail || 'No questions available for the selected topic and difficulty.';
        toast.error(msg);
      } else {
        toast.error('Failed to start test. Please try again.');
      }
    } finally {
      setLoading(false);
    }
  };

  const submitTest = async () => {
    clearInterval(timerRef.current);
    const elapsed = Math.round((Date.now() - (startTime.current || Date.now())) / 1000);

    // Build payload: do NOT default unanswered questions to 'A'
    const payload = {
      assessment_id: assessmentId,
      assessment_type: type,
      answers: questions.map(q => ({
        question_id: q.id,
        selected_option: answers[q.id] || null
      })),
      time_taken_secs: elapsed,
    };

    setLoading(true);
    try {
      const res = await assessmentAPI.submit(payload);
      setResult(res.data);
      setPhase('result');
      toast.success('Assessment submitted successfully!');
    } catch (err) {
      toast.error('Submission failed. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const fmt = (s) => `${Math.floor(s / 60).toString().padStart(2, '0')}:${(s % 60).toString().padStart(2, '0')}`;
  const answeredCount = Object.values(answers).filter(Boolean).length;

  // ─────────────────────────────────────────────────────────────────────────────
  // INTRO / CONFIGURATION PHASE
  // ─────────────────────────────────────────────────────────────────────────────
  if (phase === 'intro') {
    if (loading) return <LoadingSpinner />;

    const currentStatus = statusInfo?.status || 'Not Started';
    const statusBadgeType =
      currentStatus === 'Completed' ? 'success' :
      currentStatus === 'In Progress' ? 'warning' : 'default';

    return (
      <div style={{ maxWidth: 760, margin: '0 auto' }}>
        <PageHeader
          title={TYPE_LABELS[type] || 'Assessment'}
          subtitle={`Customizable skills test with real-time scoring and persistent progress`}
        />

        {/* Current Module Status Banner */}
        <Card style={{ marginBottom: 20, display: 'flex', alignItems: 'center', justifyContent: 'space-between', flexWrap: 'wrap', gap: 16 }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: 14 }}>
            <div style={{ width: 44, height: 44, borderRadius: 10, background: '#eef2ff', display: 'flex', alignItems: 'center', justifyContent: 'center', color: '#4f46e5', fontSize: 22 }}>
              <FiAward />
            </div>
            <div>
              <div style={{ fontSize: 13, color: '#64748b', fontWeight: 600 }}>Completion Status</div>
              <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginTop: 4 }}>
                <Badge label={currentStatus} type={statusBadgeType} />
                {statusInfo?.last_score !== null && statusInfo?.last_score !== undefined && (
                  <span style={{ fontSize: 13, color: '#334155', fontWeight: 600 }}>
                    Latest Score: <strong style={{ color: '#4f46e5' }}>{statusInfo.last_score.toFixed(0)}%</strong>
                  </span>
                )}
              </div>
            </div>
          </div>
          {statusInfo?.attempts_count > 0 && (
            <div style={{ textAlign: 'right', fontSize: 12, color: '#64748b' }}>
              Attempts: <strong>{statusInfo.attempts_count}</strong>
              {statusInfo.best_score !== null && (
                <div>Best Score: <strong style={{ color: '#10b981' }}>{statusInfo.best_score.toFixed(0)}%</strong></div>
              )}
            </div>
          )}
        </Card>

        {/* Test Customization Card */}
        <Card style={{ padding: 28 }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: 10, marginBottom: 20 }}>
            <FiSliders color="#4f46e5" size={20} />
            <h2 style={{ fontSize: 18, fontWeight: 700, margin: 0 }}>Configure Your Test</h2>
          </div>

          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: 18, marginBottom: 24 }}>
            {/* Topic Filter */}
            <div>
              <label style={{ display: 'block', fontSize: 13, fontWeight: 600, color: '#334155', marginBottom: 6 }}>
                Topic / Domain
              </label>
              <select
                value={selectedTopic}
                onChange={e => setSelectedTopic(e.target.value)}
                style={{ width: '100%', padding: '10px 12px', borderRadius: 8, border: '1px solid #cbd5e1', fontSize: 14, background: 'white' }}
              >
                <option value="all">All Topics ({meta?.total_available || 'All'} questions)</option>
                {(meta?.topics || []).map(t => (
                  <option key={t} value={t}>{t}</option>
                ))}
              </select>
            </div>

            {/* Difficulty Filter */}
            <div>
              <label style={{ display: 'block', fontSize: 13, fontWeight: 600, color: '#334155', marginBottom: 6 }}>
                Difficulty Level
              </label>
              <select
                value={selectedDifficulty}
                onChange={e => setSelectedDifficulty(e.target.value)}
                style={{ width: '100%', padding: '10px 12px', borderRadius: 8, border: '1px solid #cbd5e1', fontSize: 14, background: 'white' }}
              >
                <option value="all">Mixed (All Levels)</option>
                <option value="easy">Easy ({meta?.difficulty_counts?.easy || 0})</option>
                <option value="medium">Medium ({meta?.difficulty_counts?.medium || 0})</option>
                <option value="hard">Hard ({meta?.difficulty_counts?.hard || 0})</option>
              </select>
            </div>


          </div>

          {/* Quick Rules */}
          <div style={{ background: '#f8fafc', borderRadius: 10, padding: 18, marginBottom: 28 }}>
            <div style={{ fontWeight: 700, fontSize: 13, marginBottom: 8, color: '#1e293b' }}>
              Test Guidelines & Scoring:
            </div>
            <ul style={{ margin: 0, paddingLeft: 20, color: '#475569', fontSize: 13, lineHeight: 1.8 }}>
              <li>Each question has exactly 4 options with 1 correct answer.</li>
              <li><strong>Zero Marks Policy:</strong> Submitting with zero answers will result in <strong>0% marks</strong>.</li>
              <li>Questions you leave unselected will be recorded accurately as <em>Unanswered</em>.</li>
              <li>Progress and status are automatically saved in the database upon starting and submitting.</li>
              <li>Your verified score feeds directly into your Placement Readiness calculation.</li>
            </ul>
          </div>

          <div style={{ textAlign: 'center' }}>
            <Btn onClick={startTest} disabled={loading} size="lg" style={{ minWidth: 200, justifyContent: 'center' }}>
              {loading ? 'Preparing Test…' : '▶ Start Assessment'}
            </Btn>
          </div>
        </Card>
      </div>
    );
  }

  // ─────────────────────────────────────────────────────────────────────────────
  // ACTIVE TEST PHASE
  // ─────────────────────────────────────────────────────────────────────────────
  if (phase === 'test' && questions.length > 0) {
    const q = questions[current];

    return (
      <div>
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: 20, flexWrap: 'wrap', gap: 12 }}>
          <div>
            <h2 style={{ fontWeight: 700, margin: 0 }}>{TYPE_LABELS[type]}</h2>
            <p style={{ color: '#64748b', fontSize: 13, marginTop: 4 }}>
              Question {current + 1} of {questions.length} · <strong style={{ color: '#4f46e5' }}>{answeredCount}</strong> answered · {questions.length - answeredCount} unanswered
            </p>
          </div>
          <div style={{
            display: 'flex',
            alignItems: 'center',
            gap: 8,
            background: timeLeft < 120 ? '#fee2e2' : '#f1f5f9',
            padding: '10px 18px',
            borderRadius: 10,
            fontWeight: 700,
            color: timeLeft < 120 ? '#ef4444' : '#1e293b'
          }}>
            <FiClock size={18} /> {fmt(timeLeft)}
          </div>
        </div>

        <div style={{ display: 'grid', gridTemplateColumns: '1fr 300px', gap: 20 }}>
          {/* Main Question Card */}
          <Card>
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: 12 }}>
              <span style={{ fontSize: 11, fontWeight: 700, color: '#64748b', textTransform: 'uppercase' }}>
                {q.topic} · <span style={{ color: q.difficulty === 'hard' ? '#ef4444' : q.difficulty === 'medium' ? '#f59e0b' : '#10b981' }}>{q.difficulty}</span>
              </span>
              {answers[q.id] && (
                <button
                  onClick={() => {
                    const nextAnswers = { ...answers };
                    delete nextAnswers[q.id];
                    setAnswers(nextAnswers);
                  }}
                  style={{ background: 'transparent', border: 'none', color: '#94a3b8', fontSize: 12, cursor: 'pointer', textDecoration: 'underline' }}
                >
                  Clear choice
                </button>
              )}
            </div>

            <p style={{ fontSize: 16, fontWeight: 600, lineHeight: 1.7, marginBottom: 24, color: '#1e293b' }}>
              {q.question_text}
            </p>

            {['A', 'B', 'C', 'D'].map(opt => {
              const isSelected = answers[q.id] === opt;
              return (
                <button
                  key={opt}
                  onClick={() => setAnswers({ ...answers, [q.id]: opt })}
                  style={{
                    width: '100%',
                    textAlign: 'left',
                    padding: '14px 18px',
                    marginBottom: 12,
                    border: `2px solid ${isSelected ? '#4f46e5' : '#e2e8f0'}`,
                    background: isSelected ? '#eef2ff' : 'white',
                    borderRadius: 10,
                    cursor: 'pointer',
                    fontSize: 14,
                    fontWeight: isSelected ? 600 : 400,
                    display: 'flex',
                    alignItems: 'flex-start',
                    gap: 14,
                    transition: 'all 0.15s ease'
                  }}
                >
                  <span style={{
                    width: 28,
                    height: 28,
                    borderRadius: '50%',
                    background: isSelected ? '#4f46e5' : '#f1f5f9',
                    color: isSelected ? 'white' : '#475569',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    fontWeight: 700,
                    fontSize: 12,
                    flexShrink: 0
                  }}>
                    {opt}
                  </span>
                  <span style={{ marginTop: 4 }}>{q[`option_${opt.toLowerCase()}`]}</span>
                </button>
              );
            })}
          </Card>

          {/* Navigator Sidebar */}
          <div>
            <Card style={{ marginBottom: 16 }}>
              <div style={{ fontWeight: 700, marginBottom: 12, fontSize: 13, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <span>Question Navigator</span>
                <span style={{ fontSize: 11, color: '#64748b' }}>{answeredCount}/{questions.length}</span>
              </div>
              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(5, 1fr)', gap: 6 }}>
                {questions.map((item, i) => {
                  const isCurrent = i === current;
                  const isAnswered = !!answers[item.id];
                  return (
                    <button
                      key={i}
                      onClick={() => setCurrent(i)}
                      style={{
                        padding: '10px 4px',
                        borderRadius: 8,
                        border: `2px solid ${isCurrent ? '#4f46e5' : isAnswered ? '#10b981' : '#e2e8f0'}`,
                        background: isCurrent ? '#eef2ff' : isAnswered ? '#d1fae5' : 'white',
                        color: isAnswered ? '#065f46' : '#1e293b',
                        cursor: 'pointer',
                        fontWeight: 700,
                        fontSize: 12
                      }}
                    >
                      {i + 1}
                    </button>
                  );
                })}
              </div>
            </Card>

            <div style={{ display: 'flex', gap: 8 }}>
              <Btn
                onClick={() => setCurrent(Math.max(0, current - 1))}
                variant="secondary"
                size="md"
                disabled={current === 0}
                style={{ flex: 1, justifyContent: 'center' }}
              >
                ← Prev
              </Btn>
              <Btn
                onClick={() => setCurrent(Math.min(questions.length - 1, current + 1))}
                variant="secondary"
                size="md"
                disabled={current === questions.length - 1}
                style={{ flex: 1, justifyContent: 'center' }}
              >
                Next →
              </Btn>
            </div>

            <Btn
              onClick={submitTest}
              variant="success"
              style={{ width: '100%', marginTop: 14, justifyContent: 'center', padding: '12px' }}
              disabled={loading}
            >
              {loading ? 'Submitting…' : '✓ Submit Test'}
            </Btn>
          </div>
        </div>
      </div>
    );
  }

  // ─────────────────────────────────────────────────────────────────────────────
  // RESULT & REVIEW PHASE
  // ─────────────────────────────────────────────────────────────────────────────
  if (phase === 'result' && result) {
    const isPassing = (result.score || 0) >= 60;

    return (
      <div>
        <PageHeader title="Assessment Results" subtitle="Detailed performance breakdown and verified score" />

        {/* Hero Score Card */}
        <Card style={{
          marginBottom: 24,
          background: result.score >= 70
            ? 'linear-gradient(135deg,#065f46,#047857)'
            : result.score >= 50
            ? 'linear-gradient(135deg,#78350f,#92400e)'
            : 'linear-gradient(135deg,#7f1d1d,#991b1b)',
          color: 'white',
          border: 'none',
          padding: 28
        }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: 20 }}>
            <div>
              <div style={{ fontSize: 13, opacity: 0.85, textTransform: 'uppercase', letterSpacing: '0.5px' }}>
                {TYPE_LABELS[type]} · Verified Result
              </div>
              <div style={{ fontSize: 52, fontWeight: 800, marginTop: 4 }}>
                {result.score?.toFixed(0)}%
              </div>
              <div style={{ fontSize: 15, opacity: 0.9, marginTop: 4 }}>
                Status: <strong>Completed</strong> · Time: {result.time_taken_secs}s
              </div>
            </div>

            <div style={{ display: 'flex', gap: 12, flexWrap: 'wrap' }}>
              <Btn onClick={() => navigate('/dashboard')} variant="secondary">
                Go to Dashboard
              </Btn>
              <Btn
                onClick={() => {
                  setPhase('intro');
                  setAnswers({});
                  setCurrent(0);
                  setResult(null);
                }}
                style={{ background: 'rgba(255,255,255,0.2)', color: 'white', border: '1px solid rgba(255,255,255,0.3)' }}
              >
                <FiRotateCcw /> Retake Test
              </Btn>
            </div>
          </div>
        </Card>

        {/* Detailed Metrics Row */}
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(160px, 1fr))', gap: 16, marginBottom: 28 }}>
          <Card style={{ textAlign: 'center', padding: 18 }}>
            <div style={{ fontSize: 12, color: '#64748b', fontWeight: 600 }}>Total Questions</div>
            <div style={{ fontSize: 26, fontWeight: 800, color: '#1e293b', marginTop: 4 }}>{result.total_questions}</div>
          </Card>
          <Card style={{ textAlign: 'center', padding: 18 }}>
            <div style={{ fontSize: 12, color: '#64748b', fontWeight: 600 }}>Attempted</div>
            <div style={{ fontSize: 26, fontWeight: 800, color: '#4f46e5', marginTop: 4 }}>{result.attempted_questions || 0}</div>
          </Card>
          <Card style={{ textAlign: 'center', padding: 18 }}>
            <div style={{ fontSize: 12, color: '#64748b', fontWeight: 600 }}>Correct Answers</div>
            <div style={{ fontSize: 26, fontWeight: 800, color: '#10b981', marginTop: 4 }}>{result.correct_answers || 0}</div>
          </Card>
          <Card style={{ textAlign: 'center', padding: 18 }}>
            <div style={{ fontSize: 12, color: '#64748b', fontWeight: 600 }}>Incorrect Answers</div>
            <div style={{ fontSize: 26, fontWeight: 800, color: '#ef4444', marginTop: 4 }}>{result.incorrect_answers || 0}</div>
          </Card>
          <Card style={{ textAlign: 'center', padding: 18 }}>
            <div style={{ fontSize: 12, color: '#64748b', fontWeight: 600 }}>Unanswered</div>
            <div style={{ fontSize: 26, fontWeight: 800, color: '#94a3b8', marginTop: 4 }}>{result.unanswered_questions || 0}</div>
          </Card>
        </div>

        {/* Detailed Question Review */}
        <h3 style={{ fontSize: 16, fontWeight: 700, marginBottom: 14 }}>Question-by-Question Review</h3>
        <div style={{ display: 'flex', flexDirection: 'column', gap: 14 }}>
          {(result.results || []).map((r, i) => {
            const isAnswered = !!r.selected_option;
            const borderCol = !isAnswered ? '#94a3b8' : r.is_correct ? '#10b981' : '#ef4444';

            return (
              <Card key={i} style={{ borderLeft: `5px solid ${borderCol}`, padding: '18px 22px' }}>
                <div style={{ display: 'flex', alignItems: 'flex-start', gap: 14 }}>
                  <div style={{ flexShrink: 0, marginTop: 4 }}>
                    {!isAnswered ? (
                      <span style={{ fontSize: 12, fontWeight: 700, color: '#94a3b8', background: '#f1f5f9', padding: '3px 8px', borderRadius: 6 }}>
                        SKIPPED
                      </span>
                    ) : r.is_correct ? (
                      <FiCheck color="#10b981" size={20} />
                    ) : (
                      <FiX color="#ef4444" size={20} />
                    )}
                  </div>

                  <div style={{ flex: 1 }}>
                    <div style={{ fontSize: 11, fontWeight: 700, color: '#64748b', textTransform: 'uppercase', marginBottom: 4 }}>
                      {r.topic} · {r.difficulty}
                    </div>
                    <div style={{ fontWeight: 600, fontSize: 15, marginBottom: 10, color: '#1e293b' }}>
                      Q{i + 1}: {r.question_text}
                    </div>

                    <div style={{ fontSize: 13, color: '#475569', marginBottom: 6 }}>
                      Your Answer:{' '}
                      {isAnswered ? (
                        <strong style={{ color: r.is_correct ? '#10b981' : '#ef4444' }}>
                          Option {r.selected_option}
                        </strong>
                      ) : (
                        <strong style={{ color: '#94a3b8' }}>Not Answered (0 marks)</strong>
                      )}
                      {' · '}
                      Correct Answer: <strong style={{ color: '#10b981' }}>Option {r.correct_option}</strong>
                    </div>

                    {r.explanation && (
                      <div style={{ fontSize: 13, background: '#f8fafc', padding: '10px 14px', borderRadius: 8, color: '#334155', marginTop: 8, border: '1px solid #f1f5f9' }}>
                        💡 <strong>Explanation:</strong> {r.explanation}
                      </div>
                    )}
                  </div>
                </div>
              </Card>
            );
          })}
        </div>
      </div>
    );
  }

  return <LoadingSpinner />;
}
