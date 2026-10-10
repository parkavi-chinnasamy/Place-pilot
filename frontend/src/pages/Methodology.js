import React from 'react';
import { Link } from 'react-router-dom';

export default function Methodology() {
  return (
    <div style={{ fontFamily: 'Inter, sans-serif', background: '#f8fafc', minHeight: '100vh' }}>
      <nav style={{ background: '#1e1b4b', padding: '16px 40px', display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
          <div style={{ width: 36, height: 36, background: 'linear-gradient(135deg,#818cf8,#4f46e5)', borderRadius: 10, display: 'flex', alignItems: 'center', justifyContent: 'center', fontWeight: 800, color: 'white', fontSize: 13 }}>PP</div>
          <span style={{ fontSize: 18, fontWeight: 800, color: 'white' }}>PlacePilot</span>
        </div>
        <Link to="/" style={{ color: 'rgba(255,255,255,0.7)', fontSize: 13 }}>← Back to Home</Link>
      </nav>
      <div style={{ maxWidth: 900, margin: '0 auto', padding: '60px 24px' }}>
        <h1 style={{ fontSize: 38, fontWeight: 800, marginBottom: 12, color: '#1e293b' }}>Project Methodology</h1>
        <p style={{ color: '#64748b', fontSize: 16, marginBottom: 48 }}>
          PlacePilot — Adaptive Explainable Placement Readiness Engine
        </p>

        {[
          { n: '01', title: 'Problem Statement', body: `Students preparing for placements use 5–7 different platforms: HackerRank for coding, IndiaBix for aptitude, LinkedIn for resume, Pramp for interviews, and LeetCode for DSA. Their performance is scattered across all these tools, making it impossible to answer: "Am I ready for this specific job role — and why?"

Placement officers face the same challenge: they cannot easily identify which students need help, which skills are batch-wide weaknesses, or which student is closest to being placement-ready.` },
          { n: '02', title: 'Research Gap', body: `Existing platforms either focus on one domain (coding, aptitude, or resume) or provide generic recommendations that do not account for the student's individual performance. No existing platform integrates multiple data sources, applies explainable ML to predict readiness, and maps the prediction to specific job role requirements simultaneously.` },
          { n: '03', title: 'Proposed Solution', body: `PlacePilot is an integrated platform that:
• Collects student data across 7+ performance dimensions
• Builds a unified skill profile per student  
• Compares the profile against target job role requirements
• Predicts placement readiness using Random Forest (not GenAI)
• Explains the prediction using SHAP values
• Generates a personalised action plan using Gemini GenAI
• Updates readiness whenever new assessment data is added` },
          { n: '04', title: 'Core Innovation', body: `The "Adaptive Explainable Placement Readiness Engine" is the key innovation.

Unlike traditional approaches that use a single score or generic checklist, this engine:
1. Accepts 12 performance features from multiple sources
2. Runs Random Forest classification (Ready / Moderately Ready / Needs Improvement)
3. Computes SHAP values to explain each prediction in plain language
4. Calculates role-specific skill gaps by comparing against RoleRequirements
5. Ranks gaps by priority (gap × weight)
6. Sends the gap analysis to Gemini for a personalized weekly plan
7. Stores all results and updates on every new assessment

The same student will have DIFFERENT readiness levels for different roles because each role has different skill weights.` },
          { n: '05', title: 'Algorithm Details', body: `Random Forest:
• Trained on 800 synthetic samples (clearly labelled as demo data)
• 12 features: academic, DSA, programming, DBMS, OOP, aptitude, coding test, technical test, interview, resume, LeetCode, communication
• 100 estimators, max_depth=10, balanced class weights
• Demo accuracy: ~85% on synthetic test set
• Code structured so a real institutional dataset can replace synthetic data immediately

SHAP:
• TreeExplainer on the trained Random Forest
• Returns per-feature contribution values
• Positive SHAP = contributed toward "Ready"
• Negative SHAP = contributed toward lower readiness
• Falls back to rule-based approximation if shap library unavailable

GenAI (Gemini):
• Receives student name, actual skill scores, top gaps, and role name
• Generates: summary, 4-week plan, skill actions, resources, next steps
• Falls back to deterministic data-driven recommendations if API key not provided
• All recommendations clearly labelled as demo when no real Gemini key` },
          { n: '06', title: 'System Architecture', body: `Frontend:  React 18 + React Router + Recharts + Axios
Backend:   FastAPI (Python 3.11) + SQLAlchemy ORM
Database:  PostgreSQL 15
ML Layer:  scikit-learn Random Forest + SHAP
GenAI:     Google Gemini Pro API (demo fallback included)
Auth:      JWT Bearer tokens + bcrypt password hashing
Deployment: Docker Compose (db + backend + frontend)

Data Flow:
Student takes test → Score stored → Skill profile recalculated →
Random Forest predicts readiness → SHAP explains prediction →
Skill gaps identified → GenAI generates action plan →
Dashboard updated → History recorded` },
          { n: '07', title: 'Limitations & Disclaimers', body: `• The ML model is trained on SYNTHETIC data. It is a proof-of-concept demonstrating the pipeline.
• Readiness scores are NOT a guarantee of placement success.
• The model needs real historical placement outcome data from your institution for production use.
• LeetCode data is manually entered (no live API due to access restrictions).
• Resume analysis uses keyword matching, not NLP parsing.
• SHAP values on synthetic data should be interpreted as directional indicators, not absolute truths.
• GenAI recommendations use a demo engine when no Gemini API key is configured.` },
          { n: '08', title: 'Future Scope', body: `• GitHub integration — auto-pull contribution stats
• LinkedIn integration — experience and skills sync
• Company-specific mock interviews
• Recruiter dashboard
• Mobile app (React Native)
• Multi-college support with college admin role
• Real NLP-based resume parsing
• Live LeetCode API integration
• Ensemble model with XGBoost and neural network
• Continuous model retraining as placement outcomes are recorded` },
        ].map(s => (
          <div key={s.n} style={{ marginBottom: 40, display: 'flex', gap: 24 }}>
            <div style={{ fontSize: 28, fontWeight: 800, color: '#e2e8f0', flexShrink: 0, width: 40 }}>{s.n}</div>
            <div>
              <h2 style={{ fontSize: 20, fontWeight: 700, marginBottom: 12, color: '#1e293b' }}>{s.title}</h2>
              <div style={{ background: 'white', borderRadius: 12, padding: 24, border: '1px solid #e2e8f0', fontSize: 14, color: '#475569', lineHeight: 1.9, whiteSpace: 'pre-line' }}>{s.body}</div>
            </div>
          </div>
        ))}

        <div style={{ background: '#1e1b4b', color: 'white', borderRadius: 16, padding: 32, textAlign: 'center', marginTop: 40 }}>
          <h3 style={{ fontSize: 20, fontWeight: 700, marginBottom: 12 }}>PlacePilot Research Statement</h3>
          <p style={{ color: 'rgba(255,255,255,0.6)', fontSize: 14, maxWidth: 600, margin: '0 auto', lineHeight: 1.8 }}>
            "PlacePilot transforms scattered placement preparation data into a role-specific, explainable, and continuously updated student readiness profile — bridging the gap between student effort and employer expectations."
          </p>
          <div style={{ marginTop: 24 }}>
            <Link to="/register" style={{ display: 'inline-block', padding: '12px 32px', background: '#4f46e5', color: 'white', borderRadius: 8, fontWeight: 700, fontSize: 14 }}>Try the Platform</Link>
          </div>
        </div>
      </div>
    </div>
  );
}
