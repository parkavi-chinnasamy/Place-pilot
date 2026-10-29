import React, { useState, useEffect, useRef } from 'react';
import Editor from '@monaco-editor/react';
import { toast } from 'react-toastify';
import {
  FiCode, FiPlay, FiCheck, FiClock, FiTerminal, FiRefreshCw,
  FiFilter, FiSearch, FiAlertCircle, FiCheckCircle, FiXCircle,
  FiList, FiHelpCircle, FiChevronDown, FiChevronRight, FiCpu,
  FiActivity, FiArrowLeft
} from 'react-icons/fi';
import { codingAPI } from '../../services/api';
import { Card, Badge, LoadingSpinner } from '../../components/common/Card';

const DIFF_COLORS = {
  easy: { bg: 'rgba(16,185,129,0.15)', color: '#10b981', border: 'rgba(16,185,129,0.3)' },
  medium: { bg: 'rgba(245,158,11,0.15)', color: '#f59e0b', border: 'rgba(245,158,11,0.3)' },
  hard: { bg: 'rgba(239,68,68,0.15)', color: '#ef4444', border: 'rgba(239,68,68,0.3)' },
};

const MONACO_LANG_MAP = {
  python: 'python',
  cpp: 'cpp',
  java: 'java',
};

export default function CodingPractice() {
  // Navigation & Problem list state
  const [problems, setProblems] = useState([]);
  const [selectedProblem, setSelectedProblem] = useState(null);
  const [loadingProblems, setLoadingProblems] = useState(true);
  const [loadingDetail, setLoadingDetail] = useState(false);
  const [stats, setStats] = useState(null);

  // Filters
  const [diffFilter, setDiffFilter] = useState('all');
  const [topicFilter, setTopicFilter] = useState('all');
  const [searchQuery, setSearchQuery] = useState('');
  const [viewMode, setViewMode] = useState('catalog'); // 'catalog' | 'workspace'

  // Workspace state
  const [language, setLanguage] = useState('python');
  const [code, setCode] = useState('');
  const [leftTab, setLeftTab] = useState('description'); // 'description' | 'submissions' | 'editorial'
  const [bottomTab, setBottomTab] = useState('testcases'); // 'testcases' | 'custom' | 'result'
  const [customInput, setCustomInput] = useState('');
  const [activeTestCaseIdx, setActiveTestCaseIdx] = useState(0);

  // Submissions & Execution
  const [submissions, setSubmissions] = useState([]);
  const [running, setRunning] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const [runResult, setRunResult] = useState(null);
  const [submitResult, setSubmitResult] = useState(null);
  const [expandedHints, setExpandedHints] = useState({});

  // ── Fetch problems & stats on mount ─────────────────────────────────────────
  useEffect(() => {
    fetchProblemList();
    fetchStats();
  }, []);

  const fetchProblemList = async () => {
    setLoadingProblems(true);
    try {
      const res = await codingAPI.getProblems();
      const list = res.data.problems || [];
      setProblems(list);
    } catch (err) {
      toast.error('Failed to load coding problems');
    } finally {
      setLoadingProblems(false);
    }
  };

  const fetchStats = async () => {
    try {
      const res = await codingAPI.getStats();
      setStats(res.data);
    } catch (err) {
      console.log('Stats error:', err);
    }
  };

  const loadProblem = async (idOrSlug) => {
    setLoadingDetail(true);
    try {
      const res = await codingAPI.getProblem(idOrSlug);
      const prob = res.data;
      setSelectedProblem(prob);

      // Set starter code for active language
      const starter = prob.starter_code?.[language] || prob.starter_code?.python || '';
      setCode(starter);

      // Pre-fill custom input with sample input
      setCustomInput(prob.sample_input || '');
      setRunResult(null);
      setSubmitResult(null);
      setBottomTab('testcases');
      setActiveTestCaseIdx(0);
      setViewMode('workspace');

      // Load past submissions for this problem
      loadSubmissions(prob.id);
    } catch (err) {
      toast.error('Could not load problem details');
    } finally {
      setLoadingDetail(false);
    }
  };

  const loadSubmissions = async (probId) => {
    try {
      const res = await codingAPI.getSubmissions(probId);
      setSubmissions(res.data || []);
    } catch (err) {
      console.log('Submissions error:', err);
    }
  };

  // ── Language Change ────────────────────────────────────────────────────────
  const handleLanguageChange = (newLang) => {
    setLanguage(newLang);
    if (selectedProblem?.starter_code?.[newLang]) {
      setCode(selectedProblem.starter_code[newLang]);
    }
  };

  const handleResetCode = () => {
    if (selectedProblem?.starter_code?.[language]) {
      setCode(selectedProblem.starter_code[language]);
      toast.info('Code reset to default starter template');
    }
  };

  // ── Run Code (Sample Tests or Custom Input) ──────────────────────────────────
  const handleRunCode = async (useCustom = false) => {
    if (!code.trim()) {
      return toast.warning('Please enter some code to execute');
    }

    setRunning(true);
    setRunResult(null);
    setBottomTab('result');

    try {
      const payload = {
        problem_id: selectedProblem?.id,
        language,
        code,
      };

      if (useCustom || bottomTab === 'custom') {
        payload.custom_input = customInput;
      }

      const res = await codingAPI.runCode(payload);
      setRunResult(res.data);

      if (res.data.status === 'Compilation Error') {
        toast.error('Compilation Error');
      } else if (res.data.all_passed) {
        toast.success('Sample tests passed!');
      } else if (res.data.mode === 'custom' && res.data.success) {
        toast.success('Execution completed successfully');
      }
    } catch (err) {
      const msg = err.response?.data?.detail || 'Code execution failed';
      toast.error(msg);
      setRunResult({
        status: 'Execution Error',
        stderr: msg,
      });
    } finally {
      setRunning(false);
    }
  };

  // ── Submit Solution (All Test Cases) ─────────────────────────────────────────
  const handleSubmitCode = async () => {
    if (!code.trim()) {
      return toast.warning('Please enter some code before submitting');
    }

    setSubmitting(true);
    setSubmitResult(null);
    setBottomTab('result');

    try {
      const res = await codingAPI.submitCode({
        problem_id: selectedProblem.id,
        language,
        code,
      });

      const data = res.data;
      setSubmitResult(data);

      if (data.is_accepted) {
        toast.success(`🎉 Accepted! All ${data.total_count} test cases passed.`);
        // Mark problem as solved locally
        setSelectedProblem(prev => ({ ...prev, is_solved: true }));
        setProblems(prev => prev.map(p => p.id === selectedProblem.id ? { ...p, is_solved: true } : p));
        fetchStats();
      } else if (data.verdict === 'Compilation Error') {
        toast.error('Compilation Error');
      } else {
        toast.warning(`${data.verdict}: ${data.passed_count}/${data.total_count} test cases passed.`);
      }

      // Refresh submission history
      loadSubmissions(selectedProblem.id);
    } catch (err) {
      const msg = err.response?.data?.detail || 'Submission failed';
      toast.error(msg);
      setSubmitResult({
        verdict: 'Submission Error',
        feedback: msg,
      });
    } finally {
      setSubmitting(false);
    }
  };

  // ── Filtering ───────────────────────────────────────────────────────────────
  const topics = ['all', ...Array.from(new Set(problems.map(p => p.topic).filter(Boolean)))];

  const filteredProblems = problems.filter(p => {
    if (diffFilter !== 'all' && p.difficulty !== diffFilter) return false;
    if (topicFilter !== 'all' && p.topic !== topicFilter) return false;
    if (searchQuery.trim()) {
      const q = searchQuery.toLowerCase();
      return p.title.toLowerCase().includes(q) || (p.topic && p.topic.toLowerCase().includes(q));
    }
    return true;
  });

  // ═══════════════════════════════════════════════════════════════════════════
  // CATALOG VIEW (Problem List / Overview)
  // ═══════════════════════════════════════════════════════════════════════════
  if (viewMode === 'catalog') {
    return (
      <div style={{ maxWidth: 1200, margin: '0 auto', padding: '24px 16px' }}>
        {/* Header & Stats Banner */}
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 24, flexWrap: 'wrap', gap: 16 }}>
          <div>
            <h1 style={{ fontSize: 24, fontWeight: 800, color: '#1e293b', marginBottom: 6 }}>
              💻 Coding Practice Platform
            </h1>
            <p style={{ color: '#64748b', fontSize: 14 }}>
              Sandboxed code execution, real LeetCode-style problem suite, and automated placement skill tracking.
            </p>
          </div>
          {selectedProblem && (
            <button
              onClick={() => setViewMode('workspace')}
              style={{
                display: 'flex', alignItems: 'center', gap: 8,
                padding: '10px 18px', background: '#4f46e5', color: 'white',
                border: 'none', borderRadius: 10, fontWeight: 700, fontSize: 13, cursor: 'pointer',
              }}
            >
              Resume Problem: {selectedProblem.title} →
            </button>
          )}
        </div>

        {/* Stats Row */}
        {stats && (
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))', gap: 16, marginBottom: 24 }}>
            <div style={{ background: 'white', borderRadius: 12, padding: 18, border: '1px solid #e2e8f0', boxShadow: '0 1px 3px rgba(0,0,0,0.05)' }}>
              <div style={{ fontSize: 12, color: '#64748b', fontWeight: 600, textTransform: 'uppercase' }}>Solved Progress</div>
              <div style={{ fontSize: 28, fontWeight: 800, color: '#1e293b', marginTop: 4 }}>
                {stats.total_solved} <span style={{ fontSize: 16, color: '#94a3b8' }}>/ {stats.total_problems}</span>
              </div>
              <div style={{ height: 6, background: '#f1f5f9', borderRadius: 9999, marginTop: 8, overflow: 'hidden' }}>
                <div style={{ width: `${stats.total_problems ? (stats.total_solved / stats.total_problems) * 100 : 0}%`, height: '100%', background: '#10b981', borderRadius: 9999 }} />
              </div>
            </div>

            <div style={{ background: 'white', borderRadius: 12, padding: 18, border: '1px solid #e2e8f0', boxShadow: '0 1px 3px rgba(0,0,0,0.05)' }}>
              <div style={{ fontSize: 12, color: '#64748b', fontWeight: 600, textTransform: 'uppercase' }}>Difficulty Breakdown</div>
              <div style={{ display: 'flex', gap: 12, marginTop: 8 }}>
                <div><span style={{ color: '#10b981', fontWeight: 700 }}>{stats.easy_solved}</span><span style={{ fontSize: 11, color: '#94a3b8' }}>/{stats.total_easy} Easy</span></div>
                <div><span style={{ color: '#f59e0b', fontWeight: 700 }}>{stats.medium_solved}</span><span style={{ fontSize: 11, color: '#94a3b8' }}>/{stats.total_medium} Med</span></div>
                <div><span style={{ color: '#ef4444', fontWeight: 700 }}>{stats.hard_solved}</span><span style={{ fontSize: 11, color: '#94a3b8' }}>/{stats.total_hard} Hard</span></div>
              </div>
            </div>

            <div style={{ background: 'white', borderRadius: 12, padding: 18, border: '1px solid #e2e8f0', boxShadow: '0 1px 3px rgba(0,0,0,0.05)' }}>
              <div style={{ fontSize: 12, color: '#64748b', fontWeight: 600, textTransform: 'uppercase' }}>Acceptance Rate</div>
              <div style={{ fontSize: 28, fontWeight: 800, color: '#4f46e5', marginTop: 4 }}>
                {stats.acceptance_rate}%
              </div>
              <div style={{ fontSize: 11, color: '#94a3b8', marginTop: 4 }}>
                Across {stats.total_submissions} total submissions
              </div>
            </div>
          </div>
        )}

        {/* Filters & Search */}
        <div style={{ background: 'white', borderRadius: 12, padding: 16, border: '1px solid #e2e8f0', marginBottom: 20, display: 'flex', gap: 12, flexWrap: 'wrap', alignItems: 'center' }}>
          <div style={{ flex: 1, minWidth: 240, position: 'relative' }}>
            <FiSearch style={{ position: 'absolute', left: 12, top: 12, color: '#94a3b8' }} />
            <input
              type="text"
              placeholder="Search problems by title or topic..."
              value={searchQuery}
              onChange={e => setSearchQuery(e.target.value)}
              style={{
                width: '100%', padding: '10px 14px 10px 36px',
                borderRadius: 8, border: '1px solid #cbd5e1', fontSize: 13, outline: 'none'
              }}
            />
          </div>

          {/* Difficulty pills */}
          <div style={{ display: 'flex', gap: 6 }}>
            {['all', 'easy', 'medium', 'hard'].map(d => (
              <button
                key={d}
                onClick={() => setDiffFilter(d)}
                style={{
                  padding: '7px 14px', borderRadius: 8, border: 'none',
                  background: diffFilter === d ? '#1e293b' : '#f1f5f9',
                  color: diffFilter === d ? 'white' : '#64748b',
                  fontSize: 12, fontWeight: 600, cursor: 'pointer', textTransform: 'capitalize'
                }}
              >
                {d}
              </button>
            ))}
          </div>

          {/* Topic dropdown */}
          <select
            value={topicFilter}
            onChange={e => setTopicFilter(e.target.value)}
            style={{ padding: '8px 12px', borderRadius: 8, border: '1px solid #cbd5e1', fontSize: 12, color: '#334155', background: 'white', outline: 'none' }}
          >
            {topics.map(t => (
              <option key={t} value={t}>{t === 'all' ? 'All Topics' : t}</option>
            ))}
          </select>
        </div>

        {/* Problems Table */}
        <div style={{ background: 'white', borderRadius: 12, border: '1px solid #e2e8f0', overflow: 'hidden' }}>
          {loadingProblems ? (
            <LoadingSpinner />
          ) : filteredProblems.length === 0 ? (
            <div style={{ textAlign: 'center', padding: 48, color: '#94a3b8' }}>
              <FiCode size={40} style={{ opacity: 0.3, marginBottom: 12 }} />
              <p>No matching coding problems found.</p>
            </div>
          ) : (
            <table style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left', fontSize: 13 }}>
              <thead>
                <tr style={{ background: '#f8fafc', borderBottom: '1px solid #e2e8f0', color: '#64748b', fontWeight: 600 }}>
                  <th style={{ padding: '14px 20px', width: 60 }}>Status</th>
                  <th style={{ padding: '14px 20px' }}>Title</th>
                  <th style={{ padding: '14px 20px', width: 140 }}>Difficulty</th>
                  <th style={{ padding: '14px 20px', width: 180 }}>Topic</th>
                  <th style={{ padding: '14px 20px', width: 120, textAlign: 'right' }}>Action</th>
                </tr>
              </thead>
              <tbody>
                {filteredProblems.map((p, idx) => {
                  const dStyle = DIFF_COLORS[p.difficulty] || DIFF_COLORS.medium;
                  return (
                    <tr
                      key={p.id}
                      style={{ borderBottom: '1px solid #f1f5f9', background: idx % 2 === 0 ? 'white' : '#fafafa', cursor: 'pointer' }}
                      onClick={() => loadProblem(p.id)}
                    >
                      <td style={{ padding: '14px 20px' }}>
                        {p.is_solved ? (
                          <span title="Solved" style={{ display: 'inline-flex', alignItems: 'center', justifyContent: 'center', width: 22, height: 22, borderRadius: '50%', background: '#dcfce7', color: '#16a34a' }}>
                            <FiCheck size={14} />
                          </span>
                        ) : p.is_attempted ? (
                          <span title="Attempted" style={{ display: 'inline-flex', alignItems: 'center', justifyContent: 'center', width: 22, height: 22, borderRadius: '50%', background: '#fef3c7', color: '#d97706', fontSize: 10, fontWeight: 700 }}>
                            ⋯
                          </span>
                        ) : (
                          <span style={{ color: '#cbd5e1' }}>○</span>
                        )}
                      </td>
                      <td style={{ padding: '14px 20px', fontWeight: 600, color: '#1e293b' }}>
                        {p.title}
                      </td>
                      <td style={{ padding: '14px 20px' }}>
                        <span style={{ display: 'inline-block', padding: '3px 10px', borderRadius: 12, fontSize: 11, fontWeight: 700, textTransform: 'capitalize', background: dStyle.bg, color: dStyle.color, border: `1px solid ${dStyle.border}` }}>
                          {p.difficulty}
                        </span>
                      </td>
                      <td style={{ padding: '14px 20px', color: '#64748b' }}>
                        <span style={{ background: '#f1f5f9', padding: '2px 8px', borderRadius: 6, fontSize: 11 }}>
                          {p.topic}
                        </span>
                      </td>
                      <td style={{ padding: '14px 20px', textAlign: 'right' }}>
                        <button
                          onClick={(e) => { e.stopPropagation(); loadProblem(p.id); }}
                          style={{
                            padding: '6px 14px', borderRadius: 6, border: '1px solid #e2e8f0',
                            background: 'white', color: '#4f46e5', fontWeight: 600, fontSize: 12, cursor: 'pointer'
                          }}
                        >
                          Code →
                        </button>
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          )}
        </div>
      </div>
    );
  }

  // ═══════════════════════════════════════════════════════════════════════════
  // WORKSPACE VIEW (LeetCode-style Split IDE)
  // ═══════════════════════════════════════════════════════════════════════════
  const diffStyle = DIFF_COLORS[selectedProblem?.difficulty] || DIFF_COLORS.medium;

  return (
    <div style={{ display: 'flex', flexDirection: 'column', height: 'calc(100vh - 80px)', background: '#0f172a' }}>

      {/* ── Top Navigation Bar ────────────────────────────────────────────── */}
      <div style={{
        background: '#1e293b', borderBottom: '1px solid #334155', padding: '8px 16px',
        display: 'flex', alignItems: 'center', justifyContent: 'space-between', color: 'white', flexShrink: 0
      }}>
        {/* Left: Back button & Problem title */}
        <div style={{ display: 'flex', alignItems: 'center', gap: 14 }}>
          <button
            onClick={() => {
              setViewMode('catalog');
              fetchProblemList();
              fetchStats();
            }}
            style={{
              display: 'flex', alignItems: 'center', gap: 6, background: '#334155', border: '1px solid #475569',
              color: '#e2e8f0', padding: '6px 14px', borderRadius: 8, fontSize: 12, fontWeight: 700, cursor: 'pointer',
              transition: 'background 0.2s',
            }}
            onMouseEnter={e => e.currentTarget.style.background = '#475569'}
            onMouseLeave={e => e.currentTarget.style.background = '#334155'}
          >
            <FiArrowLeft size={14} /> Back to Problems
          </button>

          <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
            <span style={{ fontWeight: 700, fontSize: 15, color: '#f8fafc' }}>
              {selectedProblem?.title}
            </span>
            <span style={{
              padding: '2px 8px', borderRadius: 10, fontSize: 11, fontWeight: 700,
              textTransform: 'capitalize', background: diffStyle.bg, color: diffStyle.color, border: `1px solid ${diffStyle.border}`
            }}>
              {selectedProblem?.difficulty}
            </span>
            {selectedProblem?.is_solved && (
              <span style={{ display: 'flex', alignItems: 'center', gap: 4, color: '#10b981', fontSize: 12, fontWeight: 700 }}>
                <FiCheckCircle /> Solved
              </span>
            )}
          </div>
        </div>

        {/* Center: Language selector & reset */}
        <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
          <select
            value={language}
            onChange={e => handleLanguageChange(e.target.value)}
            style={{
              background: '#0f172a', color: '#f8fafc', border: '1px solid #475569',
              borderRadius: 6, padding: '5px 12px', fontSize: 12, fontWeight: 600, outline: 'none', cursor: 'pointer'
            }}
          >
            <option value="python">Python 3.8</option>
            <option value="cpp">C++ (GCC 9.2)</option>
            <option value="java">Java (OpenJDK 13)</option>
          </select>

          <button
            onClick={handleResetCode}
            title="Reset code to starter template"
            style={{
              background: 'transparent', border: '1px solid #475569', color: '#94a3b8',
              borderRadius: 6, padding: '5px 10px', fontSize: 12, cursor: 'pointer', display: 'flex', alignItems: 'center', gap: 4
            }}
          >
            <FiRefreshCw size={12} /> Reset
          </button>
        </div>

        {/* Right: Run & Submit Actions */}
        <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
          <button
            onClick={() => handleRunCode(bottomTab === 'custom')}
            disabled={running || submitting}
            style={{
              display: 'flex', alignItems: 'center', gap: 6,
              background: running ? '#475569' : '#334155', color: '#f8fafc', border: '1px solid #475569',
              borderRadius: 6, padding: '6px 16px', fontSize: 13, fontWeight: 600,
              cursor: running ? 'not-allowed' : 'pointer', transition: 'all 0.2s'
            }}
          >
            <FiPlay size={13} color="#38bdf8" /> {running ? 'Running…' : 'Run Code'}
          </button>

          <button
            onClick={handleSubmitCode}
            disabled={running || submitting}
            style={{
              display: 'flex', alignItems: 'center', gap: 6,
              background: submitting ? '#059669' : 'linear-gradient(135deg, #10b981, #059669)',
              color: 'white', border: 'none', borderRadius: 6, padding: '6px 20px', fontSize: 13, fontWeight: 700,
              cursor: submitting ? 'not-allowed' : 'pointer', boxShadow: '0 2px 8px rgba(16,185,129,0.3)'
            }}
          >
            <FiCheck size={14} /> {submitting ? 'Judging…' : 'Submit'}
          </button>
        </div>
      </div>

      {/* ── Main Two-Column Layout ────────────────────────────────────────── */}
      <div style={{ flex: 1, display: 'grid', gridTemplateColumns: '45% 55%', overflow: 'hidden' }}>

        {/* ── LEFT PANEL: Problem Details / Submissions ──────────────────── */}
        <div style={{
          background: '#1e293b', borderRight: '1px solid #334155', display: 'flex',
          flexDirection: 'column', height: '100%', overflow: 'hidden'
        }}>
          {/* Tabs */}
          <div style={{ display: 'flex', borderBottom: '1px solid #334155', background: '#0f172a', padding: '0 12px' }}>
            <button
              onClick={() => setLeftTab('description')}
              style={{
                padding: '10px 16px', background: 'transparent', border: 'none',
                borderBottom: leftTab === 'description' ? '2px solid #38bdf8' : '2px solid transparent',
                color: leftTab === 'description' ? '#38bdf8' : '#94a3b8',
                fontWeight: 600, fontSize: 12, cursor: 'pointer'
              }}
            >
              Description
            </button>
            <button
              onClick={() => setLeftTab('submissions')}
              style={{
                padding: '10px 16px', background: 'transparent', border: 'none',
                borderBottom: leftTab === 'submissions' ? '2px solid #38bdf8' : '2px solid transparent',
                color: leftTab === 'submissions' ? '#38bdf8' : '#94a3b8',
                fontWeight: 600, fontSize: 12, cursor: 'pointer'
              }}
            >
              Submissions ({submissions.length})
            </button>
          </div>

          {/* Left Tab Body */}
          <div style={{ flex: 1, overflowY: 'auto', padding: 20, color: '#e2e8f0', fontSize: 13, lineHeight: 1.7 }}>
            {leftTab === 'description' ? (
              <div>
                {/* Topic and stats */}
                <div style={{ display: 'flex', gap: 8, marginBottom: 16 }}>
                  <span style={{ background: '#334155', color: '#94a3b8', padding: '2px 10px', borderRadius: 6, fontSize: 11, fontWeight: 600 }}>
                    {selectedProblem?.topic}
                  </span>
                </div>

                {/* Description Text */}
                <div style={{ whiteSpace: 'pre-wrap', marginBottom: 20, color: '#f1f5f9' }}>
                  {selectedProblem?.description}
                </div>

                {/* Examples */}
                {selectedProblem?.sample_test_cases?.map((ex, i) => (
                  <div key={i} style={{ background: '#0f172a', border: '1px solid #334155', borderRadius: 8, padding: 14, marginBottom: 14 }}>
                    <div style={{ fontWeight: 700, fontSize: 12, color: '#38bdf8', marginBottom: 8 }}>
                      Example {ex.test_number}:
                    </div>
                    <div style={{ fontFamily: 'monospace', fontSize: 12, color: '#cbd5e1' }}>
                      <div><strong style={{ color: '#94a3b8' }}>Input:</strong> {ex.input}</div>
                      <div><strong style={{ color: '#94a3b8' }}>Output:</strong> {ex.expected_output}</div>
                      {ex.explanation && (
                        <div style={{ marginTop: 4, color: '#94a3b8' }}>
                          <strong>Explanation:</strong> {ex.explanation}
                        </div>
                      )}
                    </div>
                  </div>
                ))}

                {/* Constraints */}
                {selectedProblem?.constraints && (
                  <div style={{ marginTop: 20 }}>
                    <div style={{ fontWeight: 700, fontSize: 13, color: '#f8fafc', marginBottom: 8 }}>
                      Constraints:
                    </div>
                    <pre style={{
                      background: '#0f172a', border: '1px solid #334155', borderRadius: 8,
                      padding: 12, fontSize: 12, color: '#cbd5e1', whiteSpace: 'pre-wrap', fontFamily: 'monospace'
                    }}>
                      {selectedProblem.constraints}
                    </pre>
                  </div>
                )}

                {/* Hints accordion */}
                {selectedProblem?.hints && selectedProblem.hints.length > 0 && (
                  <div style={{ marginTop: 20 }}>
                    <div style={{ fontWeight: 700, fontSize: 13, color: '#f8fafc', marginBottom: 8 }}>
                      Hints:
                    </div>
                    {selectedProblem.hints.map((h, i) => (
                      <div key={i} style={{ marginBottom: 8, border: '1px solid #334155', borderRadius: 6, overflow: 'hidden' }}>
                        <button
                          onClick={() => setExpandedHints(p => ({ ...p, [i]: !p[i] }))}
                          style={{
                            width: '100%', background: '#0f172a', border: 'none', padding: '8px 12px',
                            color: '#94a3b8', fontSize: 12, fontWeight: 600, display: 'flex', alignItems: 'center',
                            justifyContent: 'space-between', cursor: 'pointer'
                          }}
                        >
                          <span>💡 Hint {i + 1}</span>
                          {expandedHints[i] ? <FiChevronDown /> : <FiChevronRight />}
                        </button>
                        {expandedHints[i] && (
                          <div style={{ padding: '10px 14px', background: '#1e293b', fontSize: 12, color: '#cbd5e1', borderTop: '1px solid #334155' }}>
                            {h}
                          </div>
                        )}
                      </div>
                    ))}
                  </div>
                )}
              </div>
            ) : (
              /* Submissions History */
              <div>
                <h3 style={{ fontWeight: 700, fontSize: 14, marginBottom: 14, color: '#f8fafc' }}>
                  Your Submissions for {selectedProblem?.title}
                </h3>
                {submissions.length === 0 ? (
                  <div style={{ textAlign: 'center', padding: 40, color: '#64748b' }}>
                    <FiTerminal size={32} style={{ opacity: 0.3, marginBottom: 8 }} />
                    <p>No submissions recorded yet for this problem.</p>
                  </div>
                ) : (
                  <div style={{ display: 'flex', flexDirection: 'column', gap: 10 }}>
                    {submissions.map((s) => {
                      const isAcc = s.verdict === 'Accepted';
                      return (
                        <div key={s.id} style={{
                          background: '#0f172a', border: `1px solid ${isAcc ? '#10b98150' : '#ef444450'}`,
                          borderRadius: 8, padding: 12
                        }}>
                          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 6 }}>
                            <span style={{ fontWeight: 700, fontSize: 13, color: isAcc ? '#10b981' : '#ef4444' }}>
                              {s.verdict}
                            </span>
                            <span style={{ fontSize: 11, color: '#64748b' }}>
                              {new Date(s.submitted_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                            </span>
                          </div>
                          <div style={{ display: 'flex', gap: 14, fontSize: 11, color: '#94a3b8' }}>
                            <span>Lang: <strong>{s.language}</strong></span>
                            <span>Runtime: <strong>{s.runtime_ms} ms</strong></span>
                            <span>Memory: <strong>{s.memory_kb} KB</strong></span>
                            <span>Score: <strong>{s.score}%</strong></span>
                          </div>
                        </div>
                      );
                    })}
                  </div>
                )}
              </div>
            )}
          </div>
        </div>

        {/* ── RIGHT PANEL: Code Editor + Console ─────────────────────────── */}
        <div style={{ display: 'flex', flexDirection: 'column', height: '100%', overflow: 'hidden' }}>

          {/* Monaco Editor Container */}
          <div style={{ flex: 1, minHeight: 280, position: 'relative' }}>
            <Editor
              height="100%"
              language={MONACO_LANG_MAP[language] || 'python'}
              theme="vs-dark"
              value={code}
              onChange={val => setCode(val || '')}
              options={{
                fontSize: 14,
                minimap: { enabled: false },
                scrollBeyondLastLine: false,
                lineNumbers: 'on',
                automaticLayout: true,
                tabSize: 4,
                wordWrap: 'on',
                fontFamily: "'Fira Code', 'Cascadia Code', Consolas, monospace",
              }}
            />
          </div>

          {/* ── Console / Output Drawer ───────────────────────────────────── */}
          <div style={{
            height: '42%', minHeight: 200, background: '#0b1120', borderTop: '2px solid #334155',
            display: 'flex', flexDirection: 'column', color: '#e2e8f0'
          }}>
            {/* Console Header Tabs */}
            <div style={{
              background: '#1e293b', padding: '0 12px', borderBottom: '1px solid #334155',
              display: 'flex', alignItems: 'center', justifyContent: 'space-between'
            }}>
              <div style={{ display: 'flex' }}>
                <button
                  onClick={() => setBottomTab('testcases')}
                  style={{
                    padding: '8px 14px', background: 'transparent', border: 'none',
                    borderBottom: bottomTab === 'testcases' ? '2px solid #38bdf8' : '2px solid transparent',
                    color: bottomTab === 'testcases' ? '#38bdf8' : '#94a3b8',
                    fontWeight: 600, fontSize: 12, cursor: 'pointer'
                  }}
                >
                  Test Cases
                </button>
                <button
                  onClick={() => setBottomTab('custom')}
                  style={{
                    padding: '8px 14px', background: 'transparent', border: 'none',
                    borderBottom: bottomTab === 'custom' ? '2px solid #38bdf8' : '2px solid transparent',
                    color: bottomTab === 'custom' ? '#38bdf8' : '#94a3b8',
                    fontWeight: 600, fontSize: 12, cursor: 'pointer'
                  }}
                >
                  Custom Input
                </button>
                <button
                  onClick={() => setBottomTab('result')}
                  style={{
                    padding: '8px 14px', background: 'transparent', border: 'none',
                    borderBottom: bottomTab === 'result' ? '2px solid #38bdf8' : '2px solid transparent',
                    color: bottomTab === 'result' ? '#38bdf8' : '#94a3b8',
                    fontWeight: 600, fontSize: 12, cursor: 'pointer'
                  }}
                >
                  Console Output {(runResult || submitResult) && '•'}
                </button>
              </div>

              {(running || submitting) && (
                <div style={{ fontSize: 11, color: '#38bdf8', display: 'flex', alignItems: 'center', gap: 6 }}>
                  <div style={{ width: 8, height: 8, borderRadius: '50%', background: '#38bdf8', animation: 'spin 1s infinite' }} />
                  {running ? 'Executing Sandbox…' : 'Judging Testcases…'}
                </div>
              )}
            </div>

            {/* Console Body */}
            <div style={{ flex: 1, overflowY: 'auto', padding: 14, fontFamily: 'monospace', fontSize: 12 }}>

              {/* TAB 1: Test Cases */}
              {bottomTab === 'testcases' && (
                <div>
                  {/* Test case tabs */}
                  <div style={{ display: 'flex', gap: 8, marginBottom: 12 }}>
                    {selectedProblem?.sample_test_cases?.map((tc, idx) => (
                      <button
                        key={idx}
                        onClick={() => setActiveTestCaseIdx(idx)}
                        style={{
                          padding: '4px 12px', borderRadius: 6, border: 'none',
                          background: activeTestCaseIdx === idx ? '#334155' : '#1e293b',
                          color: activeTestCaseIdx === idx ? '#38bdf8' : '#94a3b8',
                          fontSize: 11, fontWeight: 600, cursor: 'pointer'
                        }}
                      >
                        Case {idx + 1}
                      </button>
                    ))}
                  </div>

                  {/* Active Test Case Detail */}
                  {selectedProblem?.sample_test_cases?.[activeTestCaseIdx] && (
                    <div>
                      <div style={{ fontSize: 11, color: '#94a3b8', marginBottom: 4 }}>Input:</div>
                      <pre style={{ background: '#0f172a', padding: '8px 12px', borderRadius: 6, margin: '0 0 10px', color: '#f8fafc', whiteSpace: 'pre-wrap' }}>
                        {selectedProblem.sample_test_cases[activeTestCaseIdx].input}
                      </pre>
                      <div style={{ fontSize: 11, color: '#94a3b8', marginBottom: 4 }}>Expected Output:</div>
                      <pre style={{ background: '#0f172a', padding: '8px 12px', borderRadius: 6, margin: 0, color: '#f8fafc', whiteSpace: 'pre-wrap' }}>
                        {selectedProblem.sample_test_cases[activeTestCaseIdx].expected_output}
                      </pre>
                    </div>
                  )}
                </div>
              )}

              {/* TAB 2: Custom Input */}
              {bottomTab === 'custom' && (
                <div>
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 6 }}>
                    <span style={{ fontSize: 11, color: '#94a3b8' }}>Standard Input (stdin):</span>
                    <button
                      onClick={() => handleRunCode(true)}
                      disabled={running}
                      style={{
                        padding: '3px 10px', background: '#38bdf820', border: '1px solid #38bdf8',
                        color: '#38bdf8', borderRadius: 4, fontSize: 11, fontWeight: 600, cursor: 'pointer'
                      }}
                    >
                      Run with this input
                    </button>
                  </div>
                  <textarea
                    rows={5}
                    value={customInput}
                    onChange={e => setCustomInput(e.target.value)}
                    placeholder="Enter custom input here..."
                    style={{
                      width: '100%', background: '#0f172a', color: '#f8fafc', border: '1px solid #334155',
                      borderRadius: 6, padding: '8px 12px', fontFamily: 'monospace', fontSize: 12, resize: 'none', outline: 'none'
                    }}
                  />
                </div>
              )}

              {/* TAB 3: Execution Output / Result */}
              {bottomTab === 'result' && (
                <div>
                  {/* Submission Result */}
                  {submitResult ? (
                    <div>
                      <div style={{
                        display: 'flex', alignItems: 'center', justifyContent: 'space-between',
                        padding: '10px 14px', borderRadius: 8, marginBottom: 12,
                        background: submitResult.is_accepted ? '#064e3b' : '#7f1d1d',
                        border: `1px solid ${submitResult.is_accepted ? '#10b981' : '#ef4444'}`
                      }}>
                        <div>
                          <div style={{ fontWeight: 800, fontSize: 15, color: submitResult.is_accepted ? '#34d399' : '#fca5a5' }}>
                            {submitResult.verdict}
                          </div>
                          <div style={{ fontSize: 12, color: 'white', marginTop: 2 }}>
                            {submitResult.feedback}
                          </div>
                        </div>
                        <div style={{ textAlign: 'right', fontSize: 12 }}>
                          <div>Tests: <strong>{submitResult.passed_count} / {submitResult.total_count}</strong></div>
                          <div>Runtime: <strong>{submitResult.runtime_ms} ms</strong></div>
                        </div>
                      </div>

                      {submitResult.compile_output && (
                        <div style={{ marginTop: 8 }}>
                          <div style={{ color: '#fca5a5', fontWeight: 700, marginBottom: 4 }}>Compiler Output:</div>
                          <pre style={{ background: '#0f172a', padding: 10, borderRadius: 6, color: '#f87171', whiteSpace: 'pre-wrap' }}>
                            {submitResult.compile_output}
                          </pre>
                        </div>
                      )}

                      {/* Test cases list */}
                      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(140px, 1fr))', gap: 8, marginTop: 10 }}>
                        {submitResult.test_results?.map((tr, idx) => (
                          <div key={idx} style={{
                            background: tr.passed ? '#064e3b40' : '#7f1d1d40',
                            border: `1px solid ${tr.passed ? '#10b981' : '#ef4444'}`,
                            borderRadius: 6, padding: '6px 10px', fontSize: 11
                          }}>
                            <div style={{ fontWeight: 700, color: tr.passed ? '#34d399' : '#f87171' }}>
                              Case {tr.test_number}: {tr.status}
                            </div>
                            <div style={{ color: '#94a3b8', fontSize: 10 }}>
                              {tr.runtime_ms} ms · {tr.is_hidden ? 'Hidden' : 'Sample'}
                            </div>
                          </div>
                        ))}
                      </div>
                    </div>
                  ) : runResult ? (
                    /* Sample Run Result */
                    <div>
                      {runResult.status === 'Compilation Error' ? (
                        <div>
                          <div style={{ color: '#f87171', fontWeight: 700, marginBottom: 6 }}>
                            ❌ Compilation Error
                          </div>
                          <pre style={{ background: '#0f172a', padding: 10, borderRadius: 6, color: '#fca5a5', whiteSpace: 'pre-wrap' }}>
                            {runResult.compile_output}
                          </pre>
                        </div>
                      ) : runResult.mode === 'custom' ? (
                        <div>
                          <div style={{ display: 'flex', gap: 16, color: '#94a3b8', marginBottom: 8, fontSize: 11 }}>
                            <span>Status: <strong style={{ color: runResult.success ? '#10b981' : '#ef4444' }}>{runResult.status}</strong></span>
                            <span>Runtime: <strong>{runResult.runtime_ms} ms</strong></span>
                            <span>Memory: <strong>{runResult.memory_kb} KB</strong></span>
                          </div>
                          <div style={{ color: '#94a3b8', marginBottom: 4 }}>Standard Output:</div>
                          <pre style={{ background: '#0f172a', padding: 10, borderRadius: 6, color: '#f8fafc', whiteSpace: 'pre-wrap' }}>
                            {runResult.stdout || '(No output)'}
                          </pre>
                          {runResult.stderr && (
                            <div>
                              <div style={{ color: '#f87171', marginTop: 8, marginBottom: 4 }}>Standard Error:</div>
                              <pre style={{ background: '#0f172a', padding: 10, borderRadius: 6, color: '#fca5a5', whiteSpace: 'pre-wrap' }}>
                                {runResult.stderr}
                              </pre>
                            </div>
                          )}
                        </div>
                      ) : (
                        /* Sample Tests Result */
                        <div>
                          <div style={{
                            color: runResult.all_passed ? '#10b981' : '#f59e0b',
                            fontWeight: 700, fontSize: 13, marginBottom: 10
                          }}>
                            {runResult.status}
                          </div>
                          {runResult.test_results?.map((tc, idx) => (
                            <div key={idx} style={{
                              background: '#0f172a', border: `1px solid ${tc.passed ? '#10b98140' : '#ef444440'}`,
                              borderRadius: 6, padding: 10, marginBottom: 8
                            }}>
                              <div style={{ display: 'flex', justifyContent: 'space-between', fontWeight: 700, marginBottom: 4 }}>
                                <span style={{ color: tc.passed ? '#34d399' : '#f87171' }}>
                                  Test Case {tc.test_number}: {tc.status}
                                </span>
                                <span style={{ color: '#64748b', fontSize: 11 }}>{tc.runtime_ms} ms</span>
                              </div>
                              <div style={{ fontSize: 11, color: '#94a3b8' }}>
                                <div>Input: <code style={{ color: '#cbd5e1' }}>{tc.input}</code></div>
                                <div>Expected: <code style={{ color: '#cbd5e1' }}>{tc.expected_output}</code></div>
                                <div>Output: <code style={{ color: tc.passed ? '#34d399' : '#f87171' }}>{tc.actual_output || '(Empty)'}</code></div>
                              </div>
                              {tc.stderr && (
                                <pre style={{ marginTop: 6, color: '#fca5a5', fontSize: 11, whiteSpace: 'pre-wrap' }}>
                                  {tc.stderr}
                                </pre>
                              )}
                            </div>
                          ))}
                        </div>
                      )}
                    </div>
                  ) : (
                    <div style={{ color: '#64748b', textAlign: 'center', padding: '30px 0' }}>
                      Click <strong>"Run Code"</strong> to test against sample test cases or <strong>"Submit"</strong> to evaluate against all judging test cases.
                    </div>
                  )}
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
