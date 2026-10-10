import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import { AuthProvider, useAuth } from './context/AuthContext';
import Layout from './components/common/Layout';
import { LoadingSpinner } from './components/common/Card';

// Pages – lazy loaded
const Landing       = React.lazy(() => import('./pages/Landing'));
const Login         = React.lazy(() => import('./pages/auth/Login'));
const Register      = React.lazy(() => import('./pages/auth/Register'));
const StudentDash   = React.lazy(() => import('./pages/student/Dashboard'));
const Profile       = React.lazy(() => import('./pages/student/Profile'));
const Assessment    = React.lazy(() => import('./pages/student/Assessment'));
const CodingPractice = React.lazy(() => import('./pages/student/CodingPractice'));
const LeetCode      = React.lazy(() => import('./pages/student/LeetCode'));
const ResumeAnalyzer = React.lazy(() => import('./pages/student/ResumeAnalyzer'));
const MockInterview = React.lazy(() => import('./pages/student/MockInterview'));
const Readiness     = React.lazy(() => import('./pages/student/Readiness'));
const SkillGaps     = React.lazy(() => import('./pages/student/SkillGaps'));
const Recommendations = React.lazy(() => import('./pages/student/Recommendations'));
const History       = React.lazy(() => import('./pages/student/History'));
const AdminDash     = React.lazy(() => import('./pages/admin/AdminDashboard'));
const AdminStudents = React.lazy(() => import('./pages/admin/AdminStudents'));
const AdminStudentDetail = React.lazy(() => import('./pages/admin/AdminStudentDetail'));
const AdminAnalytics = React.lazy(() => import('./pages/admin/AdminAnalytics'));
const AdminSkillGaps = React.lazy(() => import('./pages/admin/AdminSkillGaps'));
const JobRoles      = React.lazy(() => import('./pages/admin/JobRoles'));
const ModelEval     = React.lazy(() => import('./pages/admin/ModelEval'));
const Methodology   = React.lazy(() => import('./pages/Methodology'));

function ProtectedRoute({ children, adminOnly = false }) {
  const { user, loading } = useAuth();
  if (loading) return <LoadingSpinner />;
  if (!user) return <Navigate to="/login" replace />;
  if (adminOnly && user.role === 'student') return <Navigate to="/dashboard" replace />;
  return <Layout>{children}</Layout>;
}

function GuestRoute({ children }) {
  const { user, loading } = useAuth();
  if (loading) return <LoadingSpinner />;
  if (user) return <Navigate to={user.role === 'student' ? '/dashboard' : '/admin/dashboard'} replace />;
  return children;
}

function AppRoutes() {
  const { user } = useAuth();
  return (
    <React.Suspense fallback={<LoadingSpinner />}>
      <Routes>
        <Route path="/" element={<Landing />} />
        <Route path="/methodology" element={<Methodology />} />
        <Route path="/login" element={<GuestRoute><Login /></GuestRoute>} />
        <Route path="/register" element={<GuestRoute><Register /></GuestRoute>} />

        {/* Student routes */}
        <Route path="/dashboard" element={<ProtectedRoute><StudentDash /></ProtectedRoute>} />
        <Route path="/profile" element={<ProtectedRoute><Profile /></ProtectedRoute>} />
        <Route path="/assessment/:type" element={<ProtectedRoute><Assessment /></ProtectedRoute>} />
        <Route path="/coding-practice" element={<ProtectedRoute><CodingPractice /></ProtectedRoute>} />
        <Route path="/leetcode" element={<ProtectedRoute><LeetCode /></ProtectedRoute>} />
        <Route path="/resume" element={<ProtectedRoute><ResumeAnalyzer /></ProtectedRoute>} />
        <Route path="/interview" element={<ProtectedRoute><MockInterview /></ProtectedRoute>} />
        <Route path="/readiness" element={<ProtectedRoute><Readiness /></ProtectedRoute>} />
        <Route path="/skill-gaps" element={<ProtectedRoute><SkillGaps /></ProtectedRoute>} />
        <Route path="/recommendations" element={<ProtectedRoute><Recommendations /></ProtectedRoute>} />
        <Route path="/history" element={<ProtectedRoute><History /></ProtectedRoute>} />

        {/* Admin routes */}
        <Route path="/admin/dashboard" element={<ProtectedRoute adminOnly><AdminDash /></ProtectedRoute>} />
        <Route path="/admin/students" element={<ProtectedRoute adminOnly><AdminStudents /></ProtectedRoute>} />
        <Route path="/admin/students/:id" element={<ProtectedRoute adminOnly><AdminStudentDetail /></ProtectedRoute>} />
        <Route path="/admin/analytics" element={<ProtectedRoute adminOnly><AdminAnalytics /></ProtectedRoute>} />
        <Route path="/admin/skill-gaps" element={<ProtectedRoute adminOnly><AdminSkillGaps /></ProtectedRoute>} />
        <Route path="/admin/job-roles" element={<ProtectedRoute adminOnly><JobRoles /></ProtectedRoute>} />
        <Route path="/admin/model-eval" element={<ProtectedRoute adminOnly><ModelEval /></ProtectedRoute>} />

        <Route path="*" element={<Navigate to={user ? (user.role === 'student' ? '/dashboard' : '/admin/dashboard') : '/'} replace />} />
      </Routes>
    </React.Suspense>
  );
}

export default function App() {
  return (
    <BrowserRouter>
      <AuthProvider>
        <AppRoutes />
        <ToastContainer position="top-right" autoClose={3000} hideProgressBar={false} />
      </AuthProvider>
    </BrowserRouter>
  );
}
