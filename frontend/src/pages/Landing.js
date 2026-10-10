import React from 'react';
import { Link } from 'react-router-dom';
import { FiTarget, FiTrendingUp, FiZap, FiUsers, FiArrowRight, FiCheck } from 'react-icons/fi';

export default function Landing() {
  return (
    <div style={{ fontFamily: 'Inter, sans-serif', minHeight: '100vh', background: '#0f0c29' }}>
      {/* Nav */}
      <nav style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', padding: '20px 60px', borderBottom: '1px solid rgba(255,255,255,0.08)' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
          <div style={{ width: 38, height: 38, background: 'linear-gradient(135deg,#818cf8,#4f46e5)', borderRadius: 10, display: 'flex', alignItems: 'center', justifyContent: 'center', fontWeight: 800, color: 'white', fontSize: 14 }}>PP</div>
          <span style={{ fontSize: 20, fontWeight: 800, color: 'white' }}>PlacePilot</span>
        </div>
        <div style={{ display: 'flex', gap: 12 }}>
          <Link to="/login" style={{ padding: '9px 20px', border: '1px solid rgba(255,255,255,0.2)', color: 'white', borderRadius: 8, fontWeight: 600, fontSize: 13 }}>Login</Link>
          <Link to="/register" style={{ padding: '9px 20px', background: '#4f46e5', color: 'white', borderRadius: 8, fontWeight: 600, fontSize: 13 }}>Get Started</Link>
        </div>
      </nav>

      {/* Hero */}
      <div style={{ textAlign: 'center', padding: '100px 20px 80px', background: 'linear-gradient(180deg,#1e1b4b 0%,#0f0c29 100%)' }}>
        <div style={{ display: 'inline-block', background: 'rgba(99,102,241,0.2)', color: '#a5b4fc', padding: '6px 16px', borderRadius: 20, fontSize: 12, fontWeight: 700, letterSpacing: '0.06em', marginBottom: 24, border: '1px solid rgba(99,102,241,0.3)' }}>
          AI-POWERED PLACEMENT PREPARATION
        </div>
        <h1 style={{ fontSize: 58, fontWeight: 800, color: 'white', lineHeight: 1.15, marginBottom: 20, maxWidth: 720, margin: '0 auto 20px' }}>
          Know Exactly How<br /><span style={{ background: 'linear-gradient(135deg,#818cf8,#06b6d4)', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent' }}>Ready You Are</span>
        </h1>
        <p style={{ color: 'rgba(255,255,255,0.6)', fontSize: 18, maxWidth: 560, margin: '0 auto 40px', lineHeight: 1.7 }}>
          PlacePilot combines your coding, aptitude, interviews, resume, and LeetCode performance to give you a role-specific placement readiness score — with AI explanations and a personalised action plan.
        </p>
        <div style={{ display: 'flex', gap: 12, justifyContent: 'center', flexWrap: 'wrap' }}>
          <Link to="/register" style={{ display: 'inline-flex', alignItems: 'center', gap: 8, padding: '14px 32px', background: 'linear-gradient(135deg,#4f46e5,#818cf8)', color: 'white', borderRadius: 10, fontWeight: 700, fontSize: 15 }}>
            Start for Free <FiArrowRight />
          </Link>
          <Link to="/methodology" style={{ display: 'inline-flex', alignItems: 'center', gap: 8, padding: '14px 32px', border: '1px solid rgba(255,255,255,0.2)', color: 'white', borderRadius: 10, fontWeight: 600, fontSize: 15 }}>
            View Methodology
          </Link>
        </div>
      </div>

      {/* Features */}
      <div style={{ padding: '80px 60px', background: '#0f0c29' }}>
        <h2 style={{ textAlign: 'center', color: 'white', fontSize: 36, fontWeight: 800, marginBottom: 60 }}>
          The Adaptive Readiness Engine
        </h2>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(260px, 1fr))', gap: 24, maxWidth: 1100, margin: '0 auto' }}>
          {[
            { icon: <FiTarget size={28} />, color: '#818cf8', title: 'Random Forest Prediction', desc: 'Trained ML model predicts your readiness as Ready / Moderately Ready / Needs Improvement based on 12 performance features.' },
            { icon: <FiZap size={28} />, color: '#06b6d4', title: 'SHAP Explainability', desc: 'Understand exactly why you got this score. SHAP values show which skills helped and which pulled you down.' },
            { icon: <FiTrendingUp size={28} />, color: '#10b981', title: 'Role-Specific Gaps', desc: 'Each job role has different requirements. Your gaps for Software Developer ≠ your gaps for Data Analyst.' },
            { icon: <FiUsers size={28} />, color: '#f59e0b', title: 'GenAI Action Plan', desc: 'Gemini generates a personalised weekly study plan based on your actual scores — not generic advice.' },
          ].map((f, i) => (
            <div key={i} style={{ background: 'rgba(255,255,255,0.04)', border: '1px solid rgba(255,255,255,0.08)', borderRadius: 16, padding: '28px 24px' }}>
              <div style={{ color: f.color, marginBottom: 16 }}>{f.icon}</div>
              <h3 style={{ color: 'white', fontWeight: 700, fontSize: 16, marginBottom: 10 }}>{f.title}</h3>
              <p style={{ color: 'rgba(255,255,255,0.5)', fontSize: 13, lineHeight: 1.7 }}>{f.desc}</p>
            </div>
          ))}
        </div>
      </div>

      {/* What you get */}
      <div style={{ padding: '80px 60px', background: '#120e35' }}>
        <div style={{ maxWidth: 900, margin: '0 auto', display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 60, alignItems: 'center' }}>
          <div>
            <h2 style={{ color: 'white', fontSize: 34, fontWeight: 800, marginBottom: 20, lineHeight: 1.3 }}>Everything in One Place</h2>
            <p style={{ color: 'rgba(255,255,255,0.5)', fontSize: 14, lineHeight: 1.8, marginBottom: 28 }}>No more switching between HackerRank, IndiaBix, LinkedIn, and Naukri. PlacePilot brings your entire preparation under one roof.</p>
            {['Aptitude, Coding & Technical Tests','AI Mock Interview with instant feedback','LeetCode progress tracking','Resume analysis & scoring','Readiness score with SHAP explanation','Personalised weekly action plan','Admin dashboard for placement officers'].map((item, i) => (
              <div key={i} style={{ display: 'flex', alignItems: 'center', gap: 10, marginBottom: 10 }}>
                <FiCheck color="#10b981" size={16} />
                <span style={{ color: 'rgba(255,255,255,0.7)', fontSize: 13 }}>{item}</span>
              </div>
            ))}
          </div>
          <div style={{ background: 'rgba(255,255,255,0.04)', border: '1px solid rgba(255,255,255,0.08)', borderRadius: 16, padding: 28 }}>
            <div style={{ marginBottom: 20 }}>
              <div style={{ fontSize: 12, color: 'rgba(255,255,255,0.4)', marginBottom: 6 }}>READINESS SCORE — Software Developer</div>
              <div style={{ fontSize: 42, fontWeight: 800, color: '#818cf8' }}>72%</div>
              <div style={{ color: '#fbbf24', fontWeight: 600, fontSize: 13, marginTop: 4 }}>Moderately Ready</div>
            </div>
            {[['Aptitude', 82, '#10b981'], ['Coding', 76, '#4f46e5'], ['DSA', 75, '#4f46e5'], ['DBMS', 52, '#ef4444'], ['Interview', 61, '#f59e0b']].map(([skill, val, color]) => (
              <div key={skill} style={{ marginBottom: 10 }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: 12, color: 'rgba(255,255,255,0.6)', marginBottom: 4 }}>
                  <span>{skill}</span><span>{val}</span>
                </div>
                <div style={{ height: 6, background: 'rgba(255,255,255,0.1)', borderRadius: 9999 }}>
                  <div style={{ width: `${val}%`, height: '100%', background: color, borderRadius: 9999 }} />
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* CTA */}
      <div style={{ textAlign: 'center', padding: '80px 20px', background: 'linear-gradient(135deg,#1e1b4b,#0f0c29)' }}>
        <h2 style={{ color: 'white', fontSize: 36, fontWeight: 800, marginBottom: 16 }}>Ready to find out your readiness?</h2>
        <p style={{ color: 'rgba(255,255,255,0.5)', marginBottom: 32, fontSize: 15 }}>Join students who are preparing smarter, not harder.</p>
        <Link to="/register" style={{ display: 'inline-flex', alignItems: 'center', gap: 8, padding: '14px 36px', background: '#4f46e5', color: 'white', borderRadius: 10, fontWeight: 700, fontSize: 15 }}>
          Get Started Free <FiArrowRight />
        </Link>
      </div>

      <footer style={{ textAlign: 'center', padding: '24px', borderTop: '1px solid rgba(255,255,255,0.06)', color: 'rgba(255,255,255,0.3)', fontSize: 12 }}>
        © 2024 PlacePilot — Prototype Research Project · Demo Data Only · Not a guaranteed placement predictor
      </footer>
    </div>
  );
}
