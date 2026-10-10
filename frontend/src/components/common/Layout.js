import React, { useState } from 'react';
import { NavLink, useNavigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import {
  FiHome, FiUser, FiCode, FiBookOpen, FiBarChart2, FiFileText,
  FiMessageSquare, FiTarget, FiTrendingUp, FiAward, FiUsers,
  FiSettings, FiLogOut, FiMenu, FiX, FiZap, FiGrid, FiBriefcase,
  FiClock, FiList
} from 'react-icons/fi';
import './Layout.css';

const studentNav = [
  { to: '/dashboard', icon: <FiHome />, label: 'Dashboard' },
  { to: '/profile', icon: <FiUser />, label: 'My Profile' },
  { label: 'Assessments', divider: true },
  { to: '/assessment/aptitude', icon: <FiBookOpen />, label: 'Aptitude Test' },
  { to: '/assessment/coding', icon: <FiCode />, label: 'Coding Test' },
  { to: '/assessment/technical', icon: <FiList />, label: 'Technical Test' },
  { label: 'Practice', divider: true },
  { to: '/coding-practice', icon: <FiZap />, label: 'Coding Practice' },
  { to: '/leetcode', icon: <FiAward />, label: 'LeetCode' },
  { to: '/resume', icon: <FiFileText />, label: 'Resume Analyzer' },
  { to: '/interview', icon: <FiMessageSquare />, label: 'Mock Interview' },
  { label: 'Analytics', divider: true },
  { to: '/readiness', icon: <FiTarget />, label: 'Readiness' },
  { to: '/skill-gaps', icon: <FiBarChart2 />, label: 'Skill Gaps' },
  { to: '/recommendations', icon: <FiTrendingUp />, label: 'Recommendations' },
  { to: '/history', icon: <FiClock />, label: 'Progress History' },
];

const adminNav = [
  { to: '/admin/dashboard', icon: <FiGrid />, label: 'Dashboard' },
  { to: '/admin/students', icon: <FiUsers />, label: 'Students' },
  { to: '/admin/analytics', icon: <FiBarChart2 />, label: 'Analytics' },
  { to: '/admin/skill-gaps', icon: <FiTarget />, label: 'Skill Gap Heatmap' },
  { to: '/admin/job-roles', icon: <FiBriefcase />, label: 'Job Roles' },
  { to: '/admin/model-eval', icon: <FiSettings />, label: 'Model Evaluation' },
];

export default function Layout({ children }) {
  const { user, logout, isAdmin } = useAuth();
  const navigate = useNavigate();
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const nav = isAdmin ? adminNav : studentNav;

  const handleLogout = () => { logout(); navigate('/login'); };

  return (
    <div className="layout">
      <aside className={`sidebar ${sidebarOpen ? 'open' : ''}`}>
        <div className="sidebar-header">
          <div className="logo">
            <div className="logo-icon">PP</div>
            <span className="logo-text">PlacePilot</span>
          </div>
          <button className="sidebar-close" onClick={() => setSidebarOpen(false)}><FiX /></button>
        </div>

        <div className="user-info">
          <div className="avatar">{user?.full_name?.[0]?.toUpperCase() || 'U'}</div>
          <div>
            <div className="user-name">{user?.full_name}</div>
            <div className="user-role">{isAdmin ? 'Admin' : 'Student'}</div>
          </div>
        </div>

        <nav className="sidebar-nav">
          {nav.map((item, i) =>
            item.divider ? (
              <div key={i} className="nav-section-label">{item.label}</div>
            ) : (
              <NavLink key={item.to} to={item.to} className={({ isActive }) => `nav-item ${isActive ? 'active' : ''}`} onClick={() => setSidebarOpen(false)}>
                <span className="nav-icon">{item.icon}</span>
                <span className="nav-label">{item.label}</span>
              </NavLink>
            )
          )}
        </nav>

        <div className="sidebar-footer">
          <button className="logout-btn" onClick={handleLogout}>
            <FiLogOut /> Sign Out
          </button>
        </div>
      </aside>

      {sidebarOpen && <div className="overlay" onClick={() => setSidebarOpen(false)} />}

      <main className="main-content">
        <header className="topbar">
          <button className="menu-btn" onClick={() => setSidebarOpen(true)}><FiMenu /></button>
          <div className="topbar-right">
            <span className="topbar-name">{user?.full_name}</span>
          </div>
        </header>
        <div className="page-body">{children}</div>
      </main>
    </div>
  );
}
