import React, { useState, useEffect, useRef, useCallback } from 'react';
import { interviewAPI, jobRolesAPI } from '../../services/api';
import { toast } from 'react-toastify';

/* ─────────────────────────────────────────────────────────────────────────────
   PlacePilot – AI HR Mock Interview
   ─ Webcam feed (student camera)
   ─ AI HR Avatar (animated, speaks questions via Web Speech TTS)
   ─ Speech recognition (student answers by voice or type)
   ─ Live transcript
   ─ AI evaluation & feedback after each answer
   ─────────────────────────────────────────────────────────────────────────── */

const SCORE_COLOR = s =>
  s >= 7 ? '#10b981' : s >= 5 ? '#f59e0b' : '#ef4444';

const HR_NAMES = {
  default: { name: 'Alex Morgan', title: 'Senior HR Manager', avatar: '👩‍💼' },
  tech:    { name: 'Priya Iyer',  title: 'Technical Recruiter', avatar: '👩‍💻' },
  data:    { name: 'Raj Sharma',  title: 'Data Science Lead',   avatar: '👨‍🔬' },
};

const INTRO_SCRIPT =
  "Hello! Welcome to your mock interview. I'm your AI interviewer today. " +
  "Please make sure your camera is on so I can see you. " +
  "When I ask a question, you can either speak your answer using the microphone button, " +
  "or type it in the box below. Take a breath, stay confident, and let's get started!";

/* ── helpers ── */
const synth = window.speechSynthesis;

function speak(text, onStart, onEnd, onWord) {
  if (!synth) return;
  synth.cancel();
  const utt = new SpeechSynthesisUtterance(text);
  utt.rate = 0.92;
  utt.pitch = 1.05;
  utt.volume = 1;
  // prefer a natural voice
  const voices = synth.getVoices();
  const preferred = voices.find(v =>
    v.name.includes('Google') || v.name.includes('Samantha') ||
    v.name.includes('Karen') || v.name.includes('Natural')
  ) || voices[0];
  if (preferred) utt.voice = preferred;
  if (onStart) utt.onstart = onStart;
  if (onEnd)   utt.onend   = onEnd;
  if (onWord)  utt.onboundary = onWord;
  synth.speak(utt);
  return utt;
}

/* ─────────────────────────────────────────────────────────────────────────── */

export default function MockInterview() {
  /* phase: setup | lobby | interview | result */
  const [phase, setPhase] = useState('setup');
  const [roles, setRoles] = useState([]);
  const [selectedRole, setSelectedRole] = useState('');
  const [session, setSession] = useState(null);
  const [qIdx, setQIdx] = useState(0);
  const [feedback, setFeedback] = useState([]);
  const [history, setHistory] = useState([]);

  /* camera */
  const videoRef = useRef(null);
  const streamRef = useRef(null);
  const [camOn, setCamOn] = useState(false);
  const [camError, setCamError] = useState('');
  const [micOn, setMicOn] = useState(false);

  /* AI HR state */
  const [hrSpeaking, setHrSpeaking] = useState(false);
  const [hrMouth, setHrMouth] = useState(false); // mouth animation tick
  const mouthTimer = useRef(null);

  /* speech recognition */
  const recognitionRef = useRef(null);
  const [listening, setListening] = useState(false);
  const [transcript, setTranscript] = useState('');
  const [answer, setAnswer] = useState('');
  const [speechSupported, setSpeechSupported] = useState(false);

  /* loading */
  const [startLoading, setStartLoading] = useState(false);
  const [evalLoading, setEvalLoading] = useState(false);

  /* timer */
  const [elapsed, setElapsed] = useState(0);
  const timerRef = useRef(null);

  /* ── init ── */
  useEffect(() => {
    jobRolesAPI.list().then(r => setRoles(r.data)).catch(() => {});
    interviewAPI.getHistory().then(r => setHistory(r.data)).catch(() => {});
    // Check speech support
    if ('SpeechRecognition' in window || 'webkitSpeechRecognition' in window) {
      setSpeechSupported(true);
    }
    return () => {
      synth?.cancel();
      stopCamera();
      clearInterval(timerRef.current);
      clearInterval(mouthTimer.current);
    };
  }, []);

  /* ── camera ── */
  const startCamera = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({
        video: { width: 640, height: 480, facingMode: 'user' },
        audio: true,
      });
      streamRef.current = stream;
      if (videoRef.current) videoRef.current.srcObject = stream;
      setCamOn(true);
      setMicOn(true);
      setCamError('');
    } catch (err) {
      setCamError('Camera/mic access denied. You can still type your answers.');
      setCamOn(false);
    }
  };

  const stopCamera = () => {
    streamRef.current?.getTracks().forEach(t => t.stop());
    streamRef.current = null;
    setCamOn(false);
    setMicOn(false);
  };

  /* ── HR mouth animation ── */
  const startMouthAnim = () => {
    clearInterval(mouthTimer.current);
    mouthTimer.current = setInterval(() => setHrMouth(p => !p), 180);
  };
  const stopMouthAnim = () => {
    clearInterval(mouthTimer.current);
    setHrMouth(false);
  };

  /* ── HR speaks ── */
  const hrSpeak = useCallback((text, onDone) => {
    setHrSpeaking(true);
    startMouthAnim();
    speak(
      text,
      null,
      () => { setHrSpeaking(false); stopMouthAnim(); if (onDone) onDone(); },
      null
    );
  }, []);

  /* ── Speech recognition ── */
  const startListening = () => {
    const SpeechRecognition =
      window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SpeechRecognition) return;

    const rec = new SpeechRecognition();
    rec.continuous = true;
    rec.interimResults = true;
    rec.lang = 'en-US';

    rec.onresult = (e) => {
      let interim = '';
      let final = '';
      for (let i = e.resultIndex; i < e.results.length; i++) {
        if (e.results[i].isFinal) final += e.results[i][0].transcript;
        else interim += e.results[i][0].transcript;
      }
      setTranscript(interim);
      if (final) setAnswer(prev => prev + ' ' + final);
    };
    rec.onerror = () => setListening(false);
    rec.onend   = () => { setListening(false); setTranscript(''); };

    recognitionRef.current = rec;
    rec.start();
    setListening(true);
  };

  const stopListening = () => {
    recognitionRef.current?.stop();
    setListening(false);
    setTranscript('');
  };

  /* ── Start interview ── */
  const goToLobby = async () => {
    if (!selectedRole) return toast.warning('Select a job role first');
    setPhase('lobby');
    await startCamera();
  };

  const beginInterview = async () => {
    setStartLoading(true);
    try {
      const res = await interviewAPI.start(selectedRole);
      setSession(res.data);
      setQIdx(0);
      setFeedback([]);
      setAnswer('');
      setTranscript('');
      setElapsed(0);
      setPhase('interview');

      // Start elapsed timer
      timerRef.current = setInterval(() =>
        setElapsed(p => p + 1), 1000);

      // HR intro speech
      setTimeout(() => {
        hrSpeak(INTRO_SCRIPT, () => {
          // then ask first question
          setTimeout(() => {
            const q = res.data.questions[0];
            hrSpeak(`Question 1. ${q.text}`);
          }, 800);
        });
      }, 600);
    } catch (e) {
      toast.error(e.response?.data?.detail || 'Failed to start interview');
    } finally {
      setStartLoading(false);
    }
  };

  /* ── Submit answer ── */
  const submitAnswer = async () => {
    const finalAnswer = answer.trim();
    if (!finalAnswer) return toast.warning('Please give an answer first');
    if (listening) stopListening();
    synth?.cancel();

    const q = session.questions[qIdx];
    setEvalLoading(true);

    // HR acknowledgement
    const acks = [
      "Thank you for that answer. Let me note that down.",
      "Good, I've recorded your response.",
      "Alright, noted. Moving on.",
      "Got it, thank you.",
    ];
    hrSpeak(acks[qIdx % acks.length]);

    try {
      const res = await interviewAPI.evaluate({
        interview_id: session.interview_id,
        question_number: q.number,
        question_text: q.text,
        student_answer: finalAnswer,
        topic: q.topic,
      });

      const newFeedback = [...feedback, {
        question: q.text, topic: q.topic, answer: finalAnswer, ...res.data
      }];
      setFeedback(newFeedback);
      setAnswer('');
      setTranscript('');

      const isLast = qIdx + 1 >= session.total_questions;

      if (isLast) {
        await interviewAPI.complete(session.interview_id);
        clearInterval(timerRef.current);
        setTimeout(() => {
          hrSpeak(
            "That was your final question. You've completed the interview. " +
            "Please wait while I compile your results. Great effort today!",
            () => setTimeout(() => setPhase('result'), 1500)
          );
        }, 1200);
      } else {
        const nextIdx = qIdx + 1;
        setQIdx(nextIdx);
        setTimeout(() => {
          const nextQ = session.questions[nextIdx];
          hrSpeak(`Next question. Question ${nextIdx + 1}. ${nextQ.text}`);
        }, 1500);
      }
    } catch { toast.error('Evaluation failed'); }
    finally { setEvalLoading(false); }
  };

  const fmtTime = s =>
    `${Math.floor(s / 60).toString().padStart(2, '0')}:${(s % 60).toString().padStart(2, '0')}`;

  const avgScore = feedback.length
    ? feedback.reduce((s, f) => s + (f.scores?.overall || 0), 0) / feedback.length
    : 0;

  const roleForHR = roles.find(r => r.id === selectedRole);
  const hrProfile = roleForHR?.name?.includes('Data') ? HR_NAMES.data
    : roleForHR?.name?.includes('Full') || roleForHR?.name?.includes('Frontend') ? HR_NAMES.tech
    : HR_NAMES.default;

  /* ════════════════════════════════════════════════════════════════════════
     RENDER
  ════════════════════════════════════════════════════════════════════════ */

  /* ── SETUP ── */
  if (phase === 'setup') return (
    <div style={{ maxWidth: 900, margin: '0 auto' }}>
      <div style={{ marginBottom: 24 }}>
        <h1 style={{ fontSize: 24, fontWeight: 800, marginBottom: 6 }}>AI Mock Interview</h1>
        <p style={{ color: '#64748b', fontSize: 14 }}>
          Real HR-style interview — AI interviewer speaks questions, you answer by voice or text, get instant feedback.
        </p>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 20 }}>
        {/* Setup card */}
        <div style={{ background: 'white', borderRadius: 16, border: '1px solid #e2e8f0', padding: 28 }}>
          <h3 style={{ fontWeight: 700, marginBottom: 20 }}>Configure Interview</h3>

          <label style={{ fontSize: 12, fontWeight: 700, color: '#64748b', display: 'block', marginBottom: 6 }}>
            JOB ROLE
          </label>
          <select value={selectedRole} onChange={e => setSelectedRole(e.target.value)}
            style={{ width: '100%', padding: '11px 14px', border: '1.5px solid #e2e8f0', borderRadius: 10, fontSize: 14, background: 'white', marginBottom: 24 }}>
            <option value="">Select a role…</option>
            {roles.map(r => <option key={r.id} value={r.id}>{r.name}</option>)}
          </select>

          {/* Features */}
          {[
            ['🎥', 'Live Camera', 'Your webcam shows your video feed throughout'],
            ['🎙️', 'Voice Recognition', 'Speak your answers — auto-transcribed in real time'],
            ['🤖', 'AI HR Interviewer', 'Reads every question aloud with natural voice'],
            ['📊', 'Instant Scoring', '5-dimension AI evaluation per answer'],
          ].map(([icon, title, desc]) => (
            <div key={title} style={{ display: 'flex', gap: 12, marginBottom: 14 }}>
              <span style={{ fontSize: 20 }}>{icon}</span>
              <div>
                <div style={{ fontWeight: 600, fontSize: 13 }}>{title}</div>
                <div style={{ fontSize: 12, color: '#94a3b8' }}>{desc}</div>
              </div>
            </div>
          ))}

          <button onClick={goToLobby} disabled={!selectedRole}
            style={{ width: '100%', marginTop: 12, padding: '13px', background: selectedRole ? 'linear-gradient(135deg,#4f46e5,#7c3aed)' : '#e2e8f0', color: selectedRole ? 'white' : '#94a3b8', border: 'none', borderRadius: 12, fontWeight: 700, fontSize: 15, cursor: selectedRole ? 'pointer' : 'not-allowed', transition: 'all 0.2s' }}>
            🎬 Enter Interview Room
          </button>
        </div>

        {/* Past interviews */}
        <div style={{ background: 'white', borderRadius: 16, border: '1px solid #e2e8f0', padding: 28 }}>
          <h3 style={{ fontWeight: 700, marginBottom: 16 }}>Past Interviews</h3>
          {history.length === 0 ? (
            <div style={{ textAlign: 'center', padding: 40, color: '#94a3b8' }}>
              <div style={{ fontSize: 40, marginBottom: 10 }}>🎤</div>
              <p>No interviews yet. Start your first one!</p>
            </div>
          ) : history.map((h, i) => (
            <div key={i} style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '12px 0', borderBottom: '1px solid #f1f5f9' }}>
              <div>
                <div style={{ fontWeight: 600, fontSize: 13 }}>{h.job_role}</div>
                <div style={{ fontSize: 11, color: '#94a3b8', marginTop: 2 }}>
                  {new Date(h.completed_at).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })}
                </div>
              </div>
              <div style={{ textAlign: 'right' }}>
                <div style={{ fontSize: 20, fontWeight: 800, color: SCORE_COLOR(h.average_score) }}>
                  {h.average_score?.toFixed(1)}
                </div>
                <div style={{ fontSize: 11, color: '#94a3b8' }}>/10</div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );

  /* ── LOBBY (camera check) ── */
  if (phase === 'lobby') return (
    <div style={{ maxWidth: 800, margin: '0 auto' }}>
      <h2 style={{ fontWeight: 800, marginBottom: 6, fontSize: 22 }}>Camera & Mic Check</h2>
      <p style={{ color: '#64748b', marginBottom: 24, fontSize: 14 }}>
        Make sure your camera and microphone are working before you begin.
      </p>

      <div style={{ background: '#1e1b4b', borderRadius: 20, overflow: 'hidden', marginBottom: 20, position: 'relative' }}>
        {camOn ? (
          <video ref={videoRef} autoPlay muted playsInline
            style={{ width: '100%', height: 360, objectFit: 'cover', display: 'block', transform: 'scaleX(-1)' }} />
        ) : (
          <div style={{ height: 360, display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', color: 'white' }}>
            <div style={{ fontSize: 60, marginBottom: 16 }}>📷</div>
            <p style={{ fontSize: 16, opacity: 0.7 }}>Camera not available</p>
            {camError && <p style={{ fontSize: 12, opacity: 0.5, marginTop: 8, maxWidth: 360, textAlign: 'center' }}>{camError}</p>}
          </div>
        )}
        {/* Status badges */}
        <div style={{ position: 'absolute', top: 14, left: 14, display: 'flex', gap: 8 }}>
          <span style={{ background: camOn ? 'rgba(16,185,129,0.9)' : 'rgba(239,68,68,0.9)', color: 'white', padding: '4px 12px', borderRadius: 20, fontSize: 12, fontWeight: 700 }}>
            {camOn ? '● CAMERA ON' : '○ NO CAMERA'}
          </span>
          <span style={{ background: micOn ? 'rgba(16,185,129,0.9)' : 'rgba(239,68,68,0.9)', color: 'white', padding: '4px 12px', borderRadius: 20, fontSize: 12, fontWeight: 700 }}>
            {micOn ? '🎙 MIC ON' : '🔇 NO MIC'}
          </span>
        </div>
      </div>

      {camError && (
        <div style={{ background: '#fff7ed', border: '1px solid #fcd34d', borderRadius: 10, padding: '12px 16px', fontSize: 13, color: '#92400e', marginBottom: 16 }}>
          ⚠️ {camError} — you can still continue and type your answers.
        </div>
      )}

      <div style={{ display: 'flex', gap: 12 }}>
        {!camOn && (
          <button onClick={startCamera}
            style={{ flex: 1, padding: 14, border: '1.5px solid #e2e8f0', borderRadius: 12, background: 'white', fontWeight: 700, fontSize: 14, cursor: 'pointer' }}>
            🔄 Retry Camera
          </button>
        )}
        <button onClick={beginInterview} disabled={startLoading}
          style={{ flex: 2, padding: 14, background: 'linear-gradient(135deg,#4f46e5,#7c3aed)', color: 'white', border: 'none', borderRadius: 12, fontWeight: 700, fontSize: 15, cursor: startLoading ? 'not-allowed' : 'pointer', opacity: startLoading ? 0.7 : 1 }}>
          {startLoading ? '⏳ Setting up…' : '✅ I\'m Ready — Start Interview'}
        </button>
        <button onClick={() => { stopCamera(); setPhase('setup'); }}
          style={{ padding: '14px 20px', border: '1.5px solid #e2e8f0', borderRadius: 12, background: 'white', fontWeight: 600, fontSize: 14, cursor: 'pointer' }}>
          ← Back
        </button>
      </div>
    </div>
  );

  /* ── INTERVIEW ── */
  if (phase === 'interview' && session) {
    const q = session.questions[qIdx];
    const progress = ((qIdx) / session.total_questions) * 100;

    return (
      <div style={{ height: 'calc(100vh - 100px)', display: 'flex', flexDirection: 'column', gap: 0 }}>

        {/* ── Top bar ── */}
        <div style={{ background: '#1e1b4b', padding: '10px 20px', display: 'flex', alignItems: 'center', justifyContent: 'space-between', borderRadius: '12px 12px 0 0' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
            <div style={{ width: 10, height: 10, borderRadius: '50%', background: '#10b981', boxShadow: '0 0 8px #10b981' }} />
            <span style={{ color: 'white', fontWeight: 700, fontSize: 14 }}>{session.job_role} Interview</span>
          </div>
          <div style={{ display: 'flex', alignItems: 'center', gap: 16 }}>
            <span style={{ color: '#a5b4fc', fontSize: 13 }}>
              Q {qIdx + 1} / {session.total_questions}
            </span>
            <span style={{ background: 'rgba(255,255,255,0.1)', color: 'white', padding: '4px 12px', borderRadius: 20, fontSize: 13, fontWeight: 700 }}>
              ⏱ {fmtTime(elapsed)}
            </span>
          </div>
        </div>

        {/* Progress bar */}
        <div style={{ height: 4, background: '#312e81' }}>
          <div style={{ height: '100%', background: 'linear-gradient(90deg,#818cf8,#06b6d4)', width: `${progress}%`, transition: 'width 0.5s ease' }} />
        </div>

        {/* ── Main video area ── */}
        <div style={{ flex: 1, display: 'grid', gridTemplateColumns: '1fr 1fr', background: '#0f0c29', position: 'relative', overflow: 'hidden' }}>

          {/* LEFT: AI HR Panel */}
          <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', padding: 24, borderRight: '1px solid rgba(255,255,255,0.08)', position: 'relative' }}>
            {/* HR Avatar */}
            <div style={{ position: 'relative', marginBottom: 20 }}>
              {/* Outer glow when speaking */}
              <div style={{ width: 160, height: 160, borderRadius: '50%', background: hrSpeaking ? 'linear-gradient(135deg,#4f46e5,#7c3aed)' : 'linear-gradient(135deg,#1e1b4b,#312e81)', display: 'flex', alignItems: 'center', justifyContent: 'center', boxShadow: hrSpeaking ? '0 0 40px rgba(99,102,241,0.6)' : '0 0 20px rgba(0,0,0,0.4)', transition: 'all 0.3s', border: `3px solid ${hrSpeaking ? '#818cf8' : '#312e81'}` }}>
                {/* Face */}
                <div style={{ position: 'relative', textAlign: 'center' }}>
                  <div style={{ fontSize: 80 }}>{hrProfile.avatar}</div>
                  {/* Animated mouth */}
                  {hrSpeaking && (
                    <div style={{ position: 'absolute', bottom: 14, left: '50%', transform: 'translateX(-50%)', display: 'flex', gap: 3 }}>
                      {[1,2,3,4,3,2].map((h, i) => (
                        <div key={i} style={{ width: 4, background: '#a5b4fc', borderRadius: 2, height: hrMouth ? h * 4 : 2, transition: 'height 0.1s', animationDelay: `${i * 0.05}s` }} />
                      ))}
                    </div>
                  )}
                </div>
              </div>

              {/* Speaking indicator ring */}
              {hrSpeaking && (
                <div style={{ position: 'absolute', inset: -8, borderRadius: '50%', border: '2px solid rgba(129,140,248,0.4)', animation: 'pulse-ring 1.5s infinite' }} />
              )}
            </div>

            <div style={{ color: 'white', fontWeight: 700, fontSize: 16, marginBottom: 4 }}>{hrProfile.name}</div>
            <div style={{ color: '#a5b4fc', fontSize: 12, marginBottom: 16 }}>{hrProfile.title}</div>

            {/* HR status badge */}
            <div style={{ background: hrSpeaking ? 'rgba(99,102,241,0.3)' : 'rgba(255,255,255,0.05)', border: `1px solid ${hrSpeaking ? '#818cf8' : 'rgba(255,255,255,0.1)'}`, borderRadius: 20, padding: '6px 16px', fontSize: 12, color: hrSpeaking ? '#a5b4fc' : 'rgba(255,255,255,0.4)', fontWeight: 600, transition: 'all 0.3s' }}>
              {hrSpeaking ? '🔊 Speaking…' : '👂 Listening to you'}
            </div>

            {/* Sound wave when speaking */}
            {hrSpeaking && (
              <div style={{ display: 'flex', alignItems: 'center', gap: 3, marginTop: 16 }}>
                {[3,5,8,10,7,9,6,4,8,5,3].map((h, i) => (
                  <div key={i} style={{ width: 3, borderRadius: 2, background: '#818cf8', height: h * 3, animation: `wave-bar 0.8s ease-in-out ${i * 0.07}s infinite alternate` }} />
                ))}
              </div>
            )}

            {/* Question card overlay */}
            <div style={{ position: 'absolute', bottom: 16, left: 16, right: 16, background: 'rgba(255,255,255,0.07)', backdropFilter: 'blur(10px)', borderRadius: 12, padding: 14, border: '1px solid rgba(255,255,255,0.1)' }}>
              <div style={{ fontSize: 10, color: '#818cf8', fontWeight: 700, marginBottom: 6, letterSpacing: '0.06em' }}>Q{qIdx + 1} · {q?.topic?.toUpperCase()}</div>
              <p style={{ fontSize: 13, color: 'rgba(255,255,255,0.85)', lineHeight: 1.6, margin: 0 }}>{q?.text}</p>
              {!hrSpeaking && (
                <button onClick={() => hrSpeak(`Question ${qIdx + 1}. ${q?.text}`)}
                  style={{ marginTop: 8, padding: '4px 12px', background: 'rgba(129,140,248,0.2)', border: '1px solid rgba(129,140,248,0.4)', borderRadius: 20, color: '#a5b4fc', fontSize: 11, cursor: 'pointer', fontWeight: 600 }}>
                  🔊 Repeat Question
                </button>
              )}
            </div>
          </div>

          {/* RIGHT: Student Camera */}
          <div style={{ position: 'relative', background: '#0a0820' }}>
            {camOn ? (
              <video ref={videoRef} autoPlay muted playsInline
                style={{ width: '100%', height: '100%', objectFit: 'cover', transform: 'scaleX(-1)' }} />
            ) : (
              <div style={{ width: '100%', height: '100%', display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', color: 'rgba(255,255,255,0.3)' }}>
                <div style={{ fontSize: 60, marginBottom: 12, opacity: 0.4 }}>👤</div>
                <p style={{ fontSize: 14 }}>Camera not available</p>
              </div>
            )}

            {/* Overlay: name tag */}
            <div style={{ position: 'absolute', bottom: 16, left: 16, background: 'rgba(0,0,0,0.6)', backdropFilter: 'blur(8px)', borderRadius: 8, padding: '6px 14px' }}>
              <span style={{ color: 'white', fontSize: 12, fontWeight: 700 }}>You (Candidate)</span>
            </div>

            {/* Listening indicator */}
            {listening && (
              <div style={{ position: 'absolute', top: 14, right: 14, background: 'rgba(239,68,68,0.9)', borderRadius: 20, padding: '6px 14px', display: 'flex', alignItems: 'center', gap: 6 }}>
                <div style={{ width: 8, height: 8, borderRadius: '50%', background: 'white', animation: 'blink 1s infinite' }} />
                <span style={{ color: 'white', fontSize: 12, fontWeight: 700 }}>🔴 LIVE</span>
              </div>
            )}

            {/* Question progress dots */}
            <div style={{ position: 'absolute', top: 14, left: 14, display: 'flex', gap: 6 }}>
              {session.questions.map((_, i) => (
                <div key={i} style={{ width: 10, height: 10, borderRadius: '50%', background: i < feedback.length ? '#10b981' : i === qIdx ? '#818cf8' : 'rgba(255,255,255,0.2)', border: i === qIdx ? '2px solid white' : 'none' }} />
              ))}
            </div>
          </div>
        </div>

        {/* ── Bottom answer panel ── */}
        <div style={{ background: '#1a1730', borderTop: '1px solid rgba(255,255,255,0.08)', padding: '16px 20px', borderRadius: '0 0 12px 12px' }}>
          {/* Live transcript */}
          {(transcript || answer) && (
            <div style={{ marginBottom: 12, padding: '10px 14px', background: 'rgba(255,255,255,0.04)', borderRadius: 10, border: '1px solid rgba(255,255,255,0.08)' }}>
              {answer && <span style={{ color: 'rgba(255,255,255,0.8)', fontSize: 13 }}>{answer}</span>}
              {transcript && <span style={{ color: '#818cf8', fontSize: 13 }}> {transcript}</span>}
            </div>
          )}

          <div style={{ display: 'flex', gap: 10, alignItems: 'flex-end' }}>
            {/* Text input */}
            <textarea
              value={answer} onChange={e => setAnswer(e.target.value)}
              placeholder={listening ? '🎙 Listening… speak now, text appears here' : 'Type your answer or use the mic button…'}
              rows={2}
              disabled={evalLoading}
              style={{ flex: 1, padding: '11px 14px', background: 'rgba(255,255,255,0.05)', border: '1.5px solid rgba(255,255,255,0.12)', borderRadius: 12, color: 'white', fontSize: 14, resize: 'none', outline: 'none', lineHeight: 1.6 }}
              onFocus={e => e.target.style.borderColor = '#818cf8'}
              onBlur={e => e.target.style.borderColor = 'rgba(255,255,255,0.12)'}
            />

            {/* Mic button */}
            {speechSupported && (
              <button
                onClick={listening ? stopListening : startListening}
                disabled={evalLoading}
                style={{ width: 52, height: 52, borderRadius: '50%', border: 'none', background: listening ? '#ef4444' : 'rgba(255,255,255,0.1)', color: 'white', fontSize: 22, cursor: 'pointer', flexShrink: 0, boxShadow: listening ? '0 0 20px rgba(239,68,68,0.6)' : 'none', transition: 'all 0.2s' }}
                title={listening ? 'Stop listening' : 'Start voice input'}
              >
                {listening ? '⏹' : '🎙'}
              </button>
            )}

            {/* Repeat question */}
            <button onClick={() => hrSpeak(`Question ${qIdx + 1}. ${q?.text}`)} disabled={hrSpeaking}
              style={{ width: 52, height: 52, borderRadius: '50%', border: '1px solid rgba(255,255,255,0.15)', background: 'rgba(255,255,255,0.05)', color: 'rgba(255,255,255,0.6)', fontSize: 20, cursor: hrSpeaking ? 'not-allowed' : 'pointer', flexShrink: 0 }}
              title="Repeat question">
              🔊
            </button>

            {/* Submit */}
            <button onClick={submitAnswer} disabled={evalLoading || !answer.trim()}
              style={{ padding: '0 28px', height: 52, borderRadius: 12, background: answer.trim() && !evalLoading ? 'linear-gradient(135deg,#4f46e5,#7c3aed)' : 'rgba(255,255,255,0.08)', border: 'none', color: answer.trim() && !evalLoading ? 'white' : 'rgba(255,255,255,0.3)', fontWeight: 700, fontSize: 14, cursor: answer.trim() && !evalLoading ? 'pointer' : 'not-allowed', flexShrink: 0, transition: 'all 0.2s' }}>
              {evalLoading ? '⏳ Evaluating…' : qIdx + 1 >= session.total_questions ? '✅ Finish' : '➤ Submit'}
            </button>
          </div>

          {/* Tip */}
          <div style={{ marginTop: 8, fontSize: 11, color: 'rgba(255,255,255,0.3)', textAlign: 'center' }}>
            💡 Tip: Be specific, use examples, mention relevant technologies. {speechSupported ? 'Click 🎙 to speak your answer.' : 'Type your answer above.'}
          </div>
        </div>

        {/* CSS animations */}
        <style>{`
          @keyframes pulse-ring { 0%{transform:scale(1);opacity:0.6} 100%{transform:scale(1.25);opacity:0} }
          @keyframes wave-bar { from{transform:scaleY(0.4)} to{transform:scaleY(1)} }
          @keyframes blink { 0%,100%{opacity:1} 50%{opacity:0} }
        `}</style>
      </div>
    );
  }

  /* ── RESULT ── */
  if (phase === 'result') {
    const grade = avgScore >= 8 ? { label: 'Excellent', color: '#10b981', emoji: '🏆' }
      : avgScore >= 6 ? { label: 'Good',      color: '#06b6d4', emoji: '👍' }
      : avgScore >= 4 ? { label: 'Average',   color: '#f59e0b', emoji: '📈' }
      : { label: 'Needs Work', color: '#ef4444', emoji: '📚' };

    return (
      <div style={{ maxWidth: 900, margin: '0 auto' }}>
        {/* Header result card */}
        <div style={{ background: 'linear-gradient(135deg,#1e1b4b,#312e81)', borderRadius: 20, padding: '32px 36px', marginBottom: 24, color: 'white' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: 20 }}>
            <div>
              <div style={{ fontSize: 13, color: 'rgba(255,255,255,0.5)', marginBottom: 8, letterSpacing: '0.06em' }}>
                INTERVIEW COMPLETE · {session?.job_role}
              </div>
              <div style={{ display: 'flex', alignItems: 'baseline', gap: 12, marginBottom: 10 }}>
                <span style={{ fontSize: 64, fontWeight: 800, color: grade.color }}>
                  {avgScore.toFixed(1)}
                </span>
                <span style={{ fontSize: 24, color: 'rgba(255,255,255,0.4)' }}>/10</span>
                <span style={{ fontSize: 36 }}>{grade.emoji}</span>
              </div>
              <span style={{ background: grade.color + '30', color: grade.color, border: `1px solid ${grade.color}50`, padding: '6px 18px', borderRadius: 20, fontWeight: 700, fontSize: 14 }}>
                {grade.label}
              </span>
            </div>
            <div style={{ display: 'flex', gap: 16 }}>
              {[
                ['Questions', feedback.length],
                ['Duration', fmtTime(elapsed)],
              ].map(([l, v]) => (
                <div key={l} style={{ background: 'rgba(255,255,255,0.07)', borderRadius: 12, padding: '14px 20px', textAlign: 'center' }}>
                  <div style={{ fontSize: 22, fontWeight: 800, color: 'white' }}>{v}</div>
                  <div style={{ fontSize: 11, color: 'rgba(255,255,255,0.4)', marginTop: 4 }}>{l}</div>
                </div>
              ))}
            </div>
          </div>

          <div style={{ display: 'flex', gap: 12, marginTop: 20, flexWrap: 'wrap' }}>
            <button onClick={() => { stopCamera(); setPhase('setup'); setFeedback([]); setSession(null); interviewAPI.getHistory().then(r => setHistory(r.data)).catch(() => {}); }}
              style={{ padding: '10px 24px', background: 'rgba(255,255,255,0.1)', border: '1px solid rgba(255,255,255,0.2)', color: 'white', borderRadius: 10, fontWeight: 600, fontSize: 13, cursor: 'pointer' }}>
              🔄 New Interview
            </button>
            <a href="/recommendations"
              style={{ padding: '10px 24px', background: '#4f46e5', color: 'white', borderRadius: 10, fontWeight: 600, fontSize: 13, textDecoration: 'none' }}>
              📋 View Recommendations
            </a>
          </div>
        </div>

        {/* Per-question feedback */}
        <h3 style={{ fontWeight: 700, marginBottom: 16, fontSize: 16 }}>Detailed Question Feedback</h3>
        <div style={{ display: 'flex', flexDirection: 'column', gap: 16 }}>
          {feedback.map((f, i) => (
            <div key={i} style={{ background: 'white', borderRadius: 16, border: '1px solid #e2e8f0', overflow: 'hidden' }}>
              {/* Header */}
              <div style={{ background: '#f8fafc', padding: '14px 20px', display: 'flex', justifyContent: 'space-between', alignItems: 'center', borderBottom: '1px solid #e2e8f0' }}>
                <div>
                  <span style={{ fontSize: 11, fontWeight: 700, color: '#64748b', textTransform: 'uppercase', letterSpacing: '0.04em' }}>
                    Q{i + 1} · {f.topic}
                  </span>
                  <p style={{ fontWeight: 600, fontSize: 14, color: '#1e293b', margin: '4px 0 0' }}>{f.question}</p>
                </div>
                <div style={{ textAlign: 'center', flexShrink: 0, marginLeft: 16 }}>
                  <div style={{ fontSize: 32, fontWeight: 800, color: SCORE_COLOR(f.scores?.overall) }}>
                    {f.scores?.overall?.toFixed(1)}
                  </div>
                  <div style={{ fontSize: 11, color: '#94a3b8' }}>/ 10</div>
                </div>
              </div>

              <div style={{ padding: '16px 20px' }}>
                {/* Score bars */}
                <div style={{ display: 'grid', gridTemplateColumns: 'repeat(5,1fr)', gap: 8, marginBottom: 16 }}>
                  {[
                    ['Technical', f.scores?.technical],
                    ['Relevance', f.scores?.relevance],
                    ['Clarity', f.scores?.clarity],
                    ['Comm.', f.scores?.communication],
                    ['Complete', f.scores?.completeness],
                  ].map(([label, val]) => (
                    <div key={label} style={{ textAlign: 'center' }}>
                      <div style={{ fontSize: 18, fontWeight: 800, color: SCORE_COLOR(val) }}>{val?.toFixed(1)}</div>
                      <div style={{ fontSize: 10, color: '#94a3b8', marginTop: 2 }}>{label}</div>
                      <div style={{ height: 4, background: '#f1f5f9', borderRadius: 9999, marginTop: 4 }}>
                        <div style={{ width: `${(val / 10) * 100}%`, height: '100%', background: SCORE_COLOR(val), borderRadius: 9999 }} />
                      </div>
                    </div>
                  ))}
                </div>

                {/* Your answer */}
                <div style={{ background: '#f8fafc', borderRadius: 8, padding: '10px 14px', marginBottom: 12 }}>
                  <div style={{ fontSize: 11, fontWeight: 700, color: '#64748b', marginBottom: 6 }}>YOUR ANSWER</div>
                  <p style={{ fontSize: 13, color: '#374151', lineHeight: 1.7, margin: 0 }}>{f.answer}</p>
                </div>

                {/* Strengths / Weaknesses */}
                <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 12, marginBottom: 12 }}>
                  <div style={{ background: '#f0fdf4', borderRadius: 8, padding: 12, borderLeft: '3px solid #10b981' }}>
                    <div style={{ fontSize: 11, fontWeight: 700, color: '#065f46', marginBottom: 6 }}>✅ STRENGTHS</div>
                    {f.strengths?.map((s, j) => (
                      <div key={j} style={{ fontSize: 12, color: '#166534', marginBottom: 3 }}>• {s}</div>
                    ))}
                  </div>
                  <div style={{ background: '#fff7ed', borderRadius: 8, padding: 12, borderLeft: '3px solid #f59e0b' }}>
                    <div style={{ fontSize: 11, fontWeight: 700, color: '#92400e', marginBottom: 6 }}>🔧 IMPROVEMENTS</div>
                    {f.weaknesses?.map((w, j) => (
                      <div key={j} style={{ fontSize: 12, color: '#78350f', marginBottom: 3 }}>• {w}</div>
                    ))}
                  </div>
                </div>

                {/* Suggested answer */}
                <div style={{ background: '#eef2ff', borderRadius: 8, padding: 12, borderLeft: '3px solid #4f46e5' }}>
                  <div style={{ fontSize: 11, fontWeight: 700, color: '#3730a3', marginBottom: 6 }}>💡 IDEAL ANSWER</div>
                  <p style={{ fontSize: 12, color: '#3730a3', lineHeight: 1.7, margin: 0 }}>{f.suggested_answer}</p>
                </div>

                {f.improvement_tips && (
                  <div style={{ marginTop: 10, fontSize: 12, color: '#64748b', background: '#f8fafc', padding: '8px 12px', borderRadius: 6 }}>
                    📌 <strong>Tip:</strong> {f.improvement_tips}
                  </div>
                )}
              </div>
            </div>
          ))}
        </div>
      </div>
    );
  }

  return (
    <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: 400 }}>
      <div style={{ width: 40, height: 40, border: '3px solid #e2e8f0', borderTopColor: '#4f46e5', borderRadius: '50%', animation: 'spin 0.8s linear infinite' }} />
      <style>{`@keyframes spin{to{transform:rotate(360deg)}}`}</style>
    </div>
  );
}
