import React, { useState, useEffect } from 'react';
import { resumeAPI, jobRolesAPI } from '../../services/api';
import {
  Card,
  PageHeader,
  Btn,
  LoadingSpinner,
  ProgressBar
} from '../../components/common/Card';
import { toast } from 'react-toastify';
import {
  FiUpload,
  FiFileText,
  FiCheckCircle,
  FiAlertTriangle,
  FiAward,
  FiLayers,
  FiInfo,
  FiExternalLink,
  FiClock,
  FiChevronRight
} from 'react-icons/fi';

export default function ResumeAnalyzer() {
  const [roles, setRoles] = useState([]);
  const [selectedRole, setSelectedRole] = useState('');
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(false);
  const [selectedSkillEvidence, setSelectedSkillEvidence] = useState(null);

  useEffect(() => {
    jobRolesAPI.list()
      .then(response => setRoles(response.data || []))
      .catch(() => toast.error('Could not load job roles'));

    loadHistory();
  }, []);

  const loadHistory = () => {
    resumeAPI.getHistory()
      .then(response => setHistory(response.data || []))
      .catch(() => { });
  };

  const analyze = async () => {
    if (!file) {
      toast.warning('Please select a resume file');
      return;
    }

    const allowedExtensions = ['pdf', 'doc', 'docx'];
    const extension = file.name.split('.').pop().toLowerCase();

    if (!allowedExtensions.includes(extension)) {
      toast.warning('Please upload a PDF or DOCX file');
      return;
    }

    const formData = new FormData();
    formData.append('file', file);

    if (selectedRole) {
      formData.append('job_role_id', selectedRole);
    }

    setLoading(true);
    setResult(null);
    setSelectedSkillEvidence(null);

    try {
      const response = await resumeAPI.analyze(formData);
      setResult(response.data);
      loadHistory();
      toast.success('Resume analyzed successfully!');
    } catch (error) {
      const msg = error.response?.data?.detail || 'Resume analysis failed. Please check the file.';
      toast.error(msg);
    } finally {
      setLoading(false);
    }
  };

  const loadPastAnalysis = async (historyId) => {
    try {
      setLoading(true);
      const res = await resumeAPI.getHistoryDetail(historyId);
      setResult(res.data);
      toast.info(`Loaded analysis for ${res.data.file_name}`);
    } catch (err) {
      toast.error('Could not load analysis details.');
    } finally {
      setLoading(false);
    }
  };

  const scores = result
    ? [
      {
        key: 'skills',
        label: 'Skills Match',
        value: result.skills_score,
        color: '#10b981',
        weight: result.score_breakdown_details?.skills?.weight || '35%',
        detail: result.score_breakdown_details?.skills?.detail || 'Evaluated technical skill match and taxonomy verification.'
      },
      {
        key: 'projects',
        label: 'Projects',
        value: result.projects_score,
        color: '#8b5cf6',
        weight: result.score_breakdown_details?.projects?.weight || '30%',
        detail: result.score_breakdown_details?.projects?.detail || 'Assessed project complexity, technologies, action verbs and metrics.'
      },
      {
        key: 'experience',
        label: 'Experience & Internships',
        value: result.experience_score,
        color: '#f59e0b',
        weight: result.score_breakdown_details?.experience?.weight || '15%',
        detail: result.score_breakdown_details?.experience?.detail || (result.internship_status || 'Practical readiness and work experience.')
      },
      {
        key: 'education',
        label: 'Education',
        value: result.education_score,
        color: '#06b6d4',
        weight: result.score_breakdown_details?.education?.weight || '10%',
        detail: result.score_breakdown_details?.education?.detail || 'Degree, academic background, and institution credentials.'
      },
      {
        key: 'completeness',
        label: 'Structure & ATS Format',
        value: result.completeness_score,
        color: '#ef4444',
        weight: result.score_breakdown_details?.completeness?.weight || '10%',
        detail: result.score_breakdown_details?.completeness?.detail || 'Contact information, links, ATS section headers, and clarity.'
      }
    ]
    : [];

  const getScoreLabel = score => {
    if (score >= 80) return { text: 'High Placement Readiness', bg: '#d1fae5', color: '#065f46' };
    if (score >= 65) return { text: 'Good Candidate Profile', bg: '#e0e7ff', color: '#3730a3' };
    if (score >= 50) return { text: 'Moderate Match', bg: '#fef3c7', color: '#92400e' };
    return { text: 'Action Needed', bg: '#fee2e2', color: '#991b1b' };
  };

  const sectionStyle = {
    fontWeight: 700,
    marginBottom: 14,
    fontSize: 16,
    color: '#1e293b',
    display: 'flex',
    alignItems: 'center',
    gap: 8,
  };

  const roleAnalysis = result?.role_analysis || {
    role_title: selectedRole ? 'Selected Role' : 'General Analysis',
    matched_skills: result?.extracted_skills || [],
    missing_required: result?.missing_skills || [],
    missing_preferred: result?.missing_keywords || [],
    uncertain_skills: []
  };

  const skillsByCategory = result?.skills_by_category || {
    "Detected Skills": result?.extracted_skills || []
  };

  const scoreLabelInfo = result ? getScoreLabel(Number(result.overall_score) || 0) : null;

  return (
    <div style={{ maxWidth: 1200, margin: '0 auto' }}>
      <PageHeader
        title="Resume Analyzer"
        subtitle="AI-powered ATS screening, transparent role-fit scoring, and verified skill evidence extraction"
      />

      {/* Resume Upload Form */}
      <Card style={{ marginBottom: 24, boxShadow: '0 4px 12px rgba(0,0,0,0.05)' }}>
        <h3 style={sectionStyle}>
          <FiUpload color="#4f46e5" /> Upload Resume for Placement Evaluation
        </h3>

        <div
          style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fit, minmax(260px, 1fr))',
            gap: 16,
            marginBottom: 20
          }}
        >
          <div>
            <label
              style={{
                fontSize: 12,
                fontWeight: 700,
                color: '#475569',
                display: 'block',
                marginBottom: 6,
                letterSpacing: '0.04em'
              }}
            >
              TARGET JOB ROLE
            </label>

            <select
              value={selectedRole}
              onChange={event => setSelectedRole(event.target.value)}
              style={{
                width: '100%',
                padding: '11px 14px',
                border: '1px solid #cbd5e1',
                borderRadius: 8,
                fontSize: 14,
                background: '#fff',
                outline: 'none'
              }}
            >
              <option value="">General Resume Analysis (All Tech Roles)</option>
              {roles.map(role => (
                <option key={role.id} value={role.id}>
                  {role.name}
                </option>
              ))}
            </select>

            <p style={{ fontSize: 11, color: '#64748b', marginTop: 6, lineHeight: 1.4 }}>
              Select a role like Frontend, Backend, Full Stack, AI/ML, or Data Analyst for specific skill-gap benchmarking.
            </p>
          </div>

          <div>
            <label
              style={{
                fontSize: 12,
                fontWeight: 700,
                color: '#475569',
                display: 'block',
                marginBottom: 6,
                letterSpacing: '0.04em'
              }}
            >
              RESUME FILE (.PDF OR .DOCX)
            </label>

            <input
              type="file"
              accept=".pdf,.docx,.doc"
              onChange={event => setFile(event.target.files?.[0] || null)}
              style={{
                width: '100%',
                padding: '9px 12px',
                border: '1px solid #cbd5e1',
                borderRadius: 8,
                fontSize: 13,
                boxSizing: 'border-box',
                background: '#f8fafc'
              }}
            />

            {file && (
              <p
                style={{
                  fontSize: 12,
                  color: '#059669',
                  marginTop: 6,
                  fontWeight: 600,
                  overflowWrap: 'anywhere'
                }}
              >
                Selected: {file.name} ({(file.size / 1024).toFixed(1)} KB)
              </p>
            )}
          </div>
        </div>

        <Btn onClick={analyze} disabled={loading || !file} size="lg">
          <FiUpload />
          {loading ? 'Parsing & Benchmarking Resume...' : 'Analyze Resume'}
        </Btn>
      </Card>

      {loading && <LoadingSpinner />}

      {/* Analysis Results */}
      {result && !loading && (
        <>
          {/* Parsing Warnings Alert if document has issues */}
          {result.parsing_warnings?.length > 0 && (
            <div
              style={{
                background: '#fffbeb',
                border: '1px solid #fde68a',
                borderRadius: 8,
                padding: '14px 18px',
                marginBottom: 20,
                display: 'flex',
                alignItems: 'flex-start',
                gap: 12
              }}
            >
              <FiAlertTriangle color="#d97706" size={20} style={{ flexShrink: 0, marginTop: 2 }} />
              <div>
                <strong style={{ color: '#92400e', fontSize: 13 }}>Resume Parsing Notice</strong>
                {result.parsing_warnings.map((w, idx) => (
                  <p key={idx} style={{ color: '#78350f', fontSize: 13, margin: '4px 0 0' }}>
                    {w}
                  </p>
                ))}
              </div>
            </div>
          )}

          {/* Primary ATS Overview Card */}
          <Card style={{ marginBottom: 20 }}>
            <div
              style={{
                display: 'flex',
                justifyContent: 'space-between',
                alignItems: 'flex-start',
                gap: 20,
                flexWrap: 'wrap'
              }}
            >
              <div style={{ flex: '1 1 300px' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: 10, flexWrap: 'wrap', marginBottom: 6 }}>
                  <h3 style={{ ...sectionStyle, marginBottom: 0 }}>
                    Resume Screening Evaluation
                  </h3>
                  {result.candidate_type && (
                    <span
                      style={{
                        background: result.is_fresher ? '#e0f2fe' : '#f1f5f9',
                        color: result.is_fresher ? '#0369a1' : '#334155',
                        padding: '3px 10px',
                        borderRadius: 14,
                        fontSize: 11,
                        fontWeight: 700
                      }}
                    >
                      {result.candidate_type}
                    </span>
                  )}
                </div>

                <p style={{ fontSize: 14, color: '#475569', margin: '4px 0 8px', fontWeight: 600 }}>
                  {result.file_name}
                </p>

                <p style={{ fontSize: 12, color: '#64748b', lineHeight: 1.6, margin: 0 }}>
                  {result.score_note ||
                    'Transparent ATS heuristic scoring balancing role skills, hands-on projects, verified internships, and document formatting.'}
                </p>
              </div>

              <div
                style={{
                  textAlign: 'center',
                  minWidth: 150,
                  padding: '12px 20px',
                  background: '#f8fafc',
                  borderRadius: 12,
                  border: '1px solid #e2e8f0'
                }}
              >
                <div
                  style={{
                    fontSize: 40,
                    fontWeight: 800,
                    color: '#4f46e5',
                    lineHeight: 1.1
                  }}
                >
                  {result.overall_score}
                  <span style={{ fontSize: 16, color: '#94a3b8' }}>/100</span>
                </div>

                {scoreLabelInfo && (
                  <span
                    style={{
                      display: 'inline-block',
                      marginTop: 8,
                      padding: '4px 12px',
                      background: scoreLabelInfo.bg,
                      color: scoreLabelInfo.color,
                      borderRadius: 20,
                      fontSize: 12,
                      fontWeight: 700
                    }}
                  >
                    {scoreLabelInfo.text}
                  </span>
                )}
              </div>
            </div>
          </Card>

          {/* Component Score Breakdown */}
          <div
            style={{
              display: 'grid',
              gridTemplateColumns: 'repeat(auto-fit, minmax(210px, 1fr))',
              gap: 14,
              marginBottom: 20
            }}
          >
            {scores.map(s => {
              const val = Math.max(0, Math.min(100, Number(s.value) || 0));
              return (
                <Card key={s.label} style={{ padding: 16, display: 'flex', flexDirection: 'column', justifyContent: 'space-between' }}>
                  <div>
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                      <span style={{ fontSize: 13, fontWeight: 700, color: '#334155' }}>{s.label}</span>
                      <span style={{ fontSize: 11, fontWeight: 600, color: '#64748b' }}>Weight: {s.weight}</span>
                    </div>

                    <div style={{ fontSize: 26, fontWeight: 800, color: s.color, margin: '8px 0 4px' }}>
                      {val}<span style={{ fontSize: 12, color: '#94a3b8' }}>/100</span>
                    </div>

                    <ProgressBar value={val} color={s.color} showLabel={false} />
                  </div>

                  <p style={{ fontSize: 11, color: '#64748b', marginTop: 10, marginBottom: 0, lineHeight: 1.4 }}>
                    {s.detail}
                  </p>
                </Card>
              );
            })}
          </div>

          {/* Role-Specific Alignment */}
          <Card style={{ marginBottom: 20 }}>
            <h3 style={sectionStyle}>
              <FiLayers color="#4f46e5" /> Role-Specific Fit Analysis: {roleAnalysis.role_title}
            </h3>

            <div
              style={{
                display: 'grid',
                gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))',
                gap: 16
              }}
            >
              {/* Matched Skills */}
              <div style={{ background: '#f0fdf4', padding: 14, borderRadius: 8, border: '1px solid #bbf7d0' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: 6, marginBottom: 10 }}>
                  <FiCheckCircle color="#16a34a" size={16} />
                  <strong style={{ fontSize: 13, color: '#15803d' }}>
                    Matched Skills ({roleAnalysis.matched_skills?.length || 0})
                  </strong>
                </div>

                {roleAnalysis.matched_skills?.length > 0 ? (
                  <div style={{ display: 'flex', flexWrap: 'wrap', gap: 6 }}>
                    {roleAnalysis.matched_skills.map((skill, idx) => (
                      <span
                        key={idx}
                        style={{
                          background: '#dcfce7',
                          color: '#166534',
                          padding: '4px 10px',
                          borderRadius: 16,
                          fontSize: 12,
                          fontWeight: 600
                        }}
                      >
                        ✓ {skill}
                      </span>
                    ))}
                  </div>
                ) : (
                  <p style={{ fontSize: 12, color: '#64748b', margin: 0 }}>
                    No specific role matches found yet.
                  </p>
                )}
              </div>

              {/* Missing Required Skills */}
              <div style={{ background: '#fef2f2', padding: 14, borderRadius: 8, border: '1px solid #fecaca' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: 6, marginBottom: 10 }}>
                  <FiAlertTriangle color="#dc2626" size={16} />
                  <strong style={{ fontSize: 13, color: '#b91c1c' }}>
                    Missing Required Skills ({roleAnalysis.missing_required?.length || 0})
                  </strong>
                </div>

                {roleAnalysis.missing_required?.length > 0 ? (
                  <div style={{ display: 'flex', flexWrap: 'wrap', gap: 6 }}>
                    {roleAnalysis.missing_required.map((skill, idx) => (
                      <span
                        key={idx}
                        style={{
                          background: '#fee2e2',
                          color: '#991b1b',
                          padding: '4px 10px',
                          borderRadius: 16,
                          fontSize: 12,
                          fontWeight: 600
                        }}
                      >
                        ! {skill}
                      </span>
                    ))}
                  </div>
                ) : (
                  <p style={{ fontSize: 12, color: '#15803d', margin: 0 }}>
                    Great! All primary core requirements for this role are represented.
                  </p>
                )}
              </div>

              {/* Missing Preferred Skills */}
              <div style={{ background: '#fffbeb', padding: 14, borderRadius: 8, border: '1px solid #fef3c7' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: 6, marginBottom: 10 }}>
                  <FiInfo color="#d97706" size={16} />
                  <strong style={{ fontSize: 13, color: '#b45309' }}>
                    Missing Preferred / Bonus Skills ({roleAnalysis.missing_preferred?.length || 0})
                  </strong>
                </div>

                {roleAnalysis.missing_preferred?.length > 0 ? (
                  <div style={{ display: 'flex', flexWrap: 'wrap', gap: 6 }}>
                    {roleAnalysis.missing_preferred.map((skill, idx) => (
                      <span
                        key={idx}
                        style={{
                          background: '#fef3c7',
                          color: '#92400e',
                          padding: '4px 10px',
                          borderRadius: 16,
                          fontSize: 12,
                          fontWeight: 600
                        }}
                      >
                        + {skill}
                      </span>
                    ))}
                  </div>
                ) : (
                  <p style={{ fontSize: 12, color: '#64748b', margin: 0 }}>
                    No pending preferred skills.
                  </p>
                )}
              </div>
            </div>
          </Card>

          {/* Categorized Skills & Evidence */}
          <Card style={{ marginBottom: 20 }}>
            <h3 style={sectionStyle}>
              <FiCheckCircle color="#10b981" /> Verified Technical Skills (by Domain)
            </h3>
            <p style={{ fontSize: 12, color: '#64748b', marginTop: -6, marginBottom: 14 }}>
              Click any skill badge to inspect the exact line and section evidence extracted from your resume.
            </p>

            {Object.keys(skillsByCategory).length > 0 ? (
              <div style={{ display: 'flex', flexDirection: 'column', gap: 14 }}>
                {Object.entries(skillsByCategory).map(([cat, skills]) => (
                  <div key={cat} style={{ borderBottom: '1px solid #f1f5f9', paddingBottom: 12 }}>
                    <div style={{ fontSize: 12, fontWeight: 700, color: '#475569', marginBottom: 8, textTransform: 'uppercase', letterSpacing: '0.04em' }}>
                      {cat} ({skills.length})
                    </div>
                    <div style={{ display: 'flex', flexWrap: 'wrap', gap: 8 }}>
                      {skills.map((skillName, idx) => {
                        const ev = result.skills_with_evidence?.[skillName];
                        const isSelected = selectedSkillEvidence?.skill === skillName;
                        return (
                          <button
                            key={idx}
                            onClick={() => setSelectedSkillEvidence(ev || { skill: skillName, evidence: 'Verified keyword in resume body', section: 'Resume Text' })}
                            style={{
                              background: isSelected ? '#10b981' : '#f0fdf4',
                              color: isSelected ? '#fff' : '#065f46',
                              border: '1px solid #bbf7d0',
                              padding: '5px 12px',
                              borderRadius: 16,
                              fontSize: 12,
                              fontWeight: 600,
                              cursor: 'pointer',
                              display: 'flex',
                              alignItems: 'center',
                              gap: 6,
                              transition: 'all 0.2s ease'
                            }}
                          >
                            <span>{skillName}</span>
                            <span style={{ fontSize: 10, opacity: 0.8 }}>🔍</span>
                          </button>
                        );
                      })}
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <p style={{ fontSize: 13, color: '#64748b' }}>No verified technical skills detected.</p>
            )}

            {/* Evidence Modal / Box */}
            {selectedSkillEvidence && (
              <div
                style={{
                  marginTop: 16,
                  padding: '14px 16px',
                  background: '#f8fafc',
                  border: '1px solid #cbd5e1',
                  borderRadius: 8,
                  display: 'flex',
                  justifyContent: 'space-between',
                  alignItems: 'flex-start',
                  gap: 12
                }}
              >
                <div>
                  <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 4 }}>
                    <strong style={{ fontSize: 13, color: '#0f172a' }}>
                      Evidence for "{selectedSkillEvidence.skill}"
                    </strong>
                    <span style={{ fontSize: 11, background: '#e2e8f0', color: '#334155', padding: '2px 8px', borderRadius: 10 }}>
                      Section: {selectedSkillEvidence.section || 'Resume'}
                    </span>
                  </div>
                  <p style={{ fontSize: 12, color: '#334155', margin: 0, fontStyle: 'italic', lineHeight: 1.5 }}>
                    "{selectedSkillEvidence.evidence}"
                  </p>
                </div>
                <button
                  onClick={() => setSelectedSkillEvidence(null)}
                  style={{
                    background: 'none',
                    border: 'none',
                    color: '#64748b',
                    cursor: 'pointer',
                    fontSize: 14,
                    padding: '2px 6px'
                  }}
                >
                  ✕
                </button>
              </div>
            )}
          </Card>

          {/* Certifications — Confirmed */}
          <Card style={{ marginBottom: 20 }}>
            <h3 style={sectionStyle}>
              <FiAward color="#f59e0b" /> Certifications
            </h3>

            {(result.certifications_confirmed || result.certifications)?.length > 0 ? (
              <div style={{ display: 'flex', flexDirection: 'column', gap: 10 }}>
                {(result.certifications_confirmed || result.certifications.map(c => typeof c === 'string' ? { title: c } : c)).map((cert, idx) => (
                  <div
                    key={idx}
                    style={{
                      display: 'flex',
                      justifyContent: 'space-between',
                      alignItems: 'flex-start',
                      padding: '10px 14px',
                      background: '#f0fdf4',
                      borderRadius: 8,
                      border: '1px solid #bbf7d0',
                      gap: 10,
                    }}
                  >
                    <div>
                      <div style={{ fontSize: 13, fontWeight: 600, color: '#1e293b', lineHeight: 1.5 }}>
                        {cert.title || cert.name || (typeof cert === 'string' ? cert : JSON.stringify(cert))}
                      </div>
                      {cert.issuer && (
                        <span style={{
                          display: 'inline-block',
                          marginTop: 4,
                          fontSize: 11,
                          color: '#475569',
                          background: '#e2e8f0',
                          padding: '2px 8px',
                          borderRadius: 10,
                        }}>
                          Issuer: {cert.issuer}
                        </span>
                      )}
                    </div>
                    {cert.confidence && (
                      <span style={{
                        fontSize: 10,
                        fontWeight: 700,
                        padding: '3px 8px',
                        borderRadius: 10,
                        flexShrink: 0,
                        background: cert.confidence === 'high' ? '#dcfce7' : '#e0f2fe',
                        color: cert.confidence === 'high' ? '#166534' : '#0369a1',
                        textTransform: 'uppercase',
                        letterSpacing: '0.05em',
                      }}>
                        {cert.confidence}
                      </span>
                    )}
                  </div>
                ))}
              </div>
            ) : (
              <p style={{ color: '#64748b', fontSize: 13, margin: 0 }}>
                No certifications were extracted from this resume.
                Academic degrees, college names, school qualifications, and declaration texts are excluded from certification results.
              </p>
            )}
          </Card>

          {/* Certifications — Uncertain / Needs Review */}
          {result.certifications_uncertain?.length > 0 && (
            <Card style={{ marginBottom: 20 }}>
              <h3 style={sectionStyle}>
                <FiAlertTriangle color="#d97706" /> Possible Certifications — Review Needed
              </h3>
              <p style={{ fontSize: 12, color: '#92400e', marginTop: -6, marginBottom: 14, lineHeight: 1.5 }}>
                These items were found in your resume but could not be confidently classified as certifications.
                Please verify if they are legitimate credentials.
              </p>
              <div style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
                {result.certifications_uncertain.map((cert, idx) => (
                  <div
                    key={idx}
                    style={{
                      padding: '8px 14px',
                      background: '#fffbeb',
                      borderRadius: 8,
                      border: '1px solid #fde68a',
                      display: 'flex',
                      justifyContent: 'space-between',
                      alignItems: 'center',
                      gap: 10,
                    }}
                  >
                    <span style={{ fontSize: 13, color: '#78350f', fontWeight: 500 }}>
                      {cert.title || (typeof cert === 'string' ? cert : JSON.stringify(cert))}
                    </span>
                    <span style={{
                      fontSize: 10,
                      fontWeight: 700,
                      padding: '3px 8px',
                      borderRadius: 10,
                      background: '#fef3c7',
                      color: '#92400e',
                      textTransform: 'uppercase',
                      letterSpacing: '0.05em',
                      flexShrink: 0,
                    }}>
                      Needs Review
                    </span>
                  </div>
                ))}
              </div>
            </Card>
          )}

          {/* Actionable Suggestions */}
          <Card style={{ marginBottom: 20 }}>
            <h3 style={sectionStyle}>
              <FiInfo color="#4f46e5" /> Actionable Resume Improvement Steps
            </h3>

            {result.improvement_suggestions?.length > 0 ? (
              <div style={{ display: 'flex', flexDirection: 'column', gap: 10 }}>
                {result.improvement_suggestions.map((sug, idx) => (
                  <div
                    key={idx}
                    style={{
                      display: 'flex',
                      flexDirection: 'column',
                      gap: 4,
                      padding: '12px 16px',
                      background: '#fff7ed',
                      borderRadius: 8,
                      borderLeft: '4px solid #f59e0b'
                    }}
                  >
                    <strong style={{ fontSize: 13, color: '#9a3412' }}>{sug.area}</strong>
                    <span style={{ fontSize: 13, color: '#7c2d12', lineHeight: 1.5 }}>{sug.tip}</span>
                  </div>
                ))}
              </div>
            ) : (
              <p style={{ color: '#64748b', fontSize: 13 }}>
                Your resume meets all foundational criteria! Keep your project repositories and live demos updated.
              </p>
            )}
          </Card>
        </>
      )}

      {/* Analysis History */}
      {history.length > 0 && (
        <Card style={{ marginTop: 24 }}>
          <h3 style={sectionStyle}>
            <FiClock color="#64748b" /> Analysis History
          </h3>

          <div style={{ display: 'flex', flexDirection: 'column' }}>
            {history.map((item, idx) => (
              <div
                key={item.id || idx}
                style={{
                  display: 'flex',
                  justifyContent: 'space-between',
                  alignItems: 'center',
                  flexWrap: 'wrap',
                  gap: 12,
                  padding: '12px 0',
                  borderBottom: idx === history.length - 1 ? 'none' : '1px solid #f1f5f9'
                }}
              >
                <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
                  <FiFileText color="#64748b" size={18} />
                  <div>
                    <span style={{ fontSize: 13, fontWeight: 600, color: '#1e293b' }}>
                      {item.file_name}
                    </span>
                    <div style={{ fontSize: 11, color: '#94a3b8' }}>
                      {item.job_role_name || 'General Analysis'} • {item.analyzed_at ? new Date(item.analyzed_at).toLocaleDateString() : 'Recent'}
                    </div>
                  </div>
                </div>

                <div style={{ display: 'flex', alignItems: 'center', gap: 14 }}>
                  <strong style={{ color: '#4f46e5', fontSize: 15 }}>
                    {item.overall_score}/100
                  </strong>

                  {item.id && (
                    <button
                      onClick={() => loadPastAnalysis(item.id)}
                      style={{
                        background: '#f1f5f9',
                        border: 'none',
                        borderRadius: 6,
                        padding: '5px 10px',
                        fontSize: 12,
                        color: '#475569',
                        cursor: 'pointer',
                        display: 'flex',
                        alignItems: 'center',
                        gap: 4
                      }}
                    >
                      <span>View</span>
                      <FiChevronRight size={12} />
                    </button>
                  )}
                </div>
              </div>
            ))}
          </div>
        </Card>
      )}
    </div>
  );
}
