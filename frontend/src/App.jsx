import React from 'react'
import { HashRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import Login from './pages/Login'
import Register from './pages/Register'
import Feed from './pages/Feed'
import Profile from './pages/Profile'
import './App.css'

const RequireAuth = ({children}) => {
  const token = localStorage.getItem('token')
  if (!token) return <Navigate to="/login" replace />
  return children
}

function App() {
  const token = localStorage.getItem('token')
  return (
    <div className="app-shell">
      <div className="background-blobs">
        <span className="blob blob-1" />
        <span className="blob blob-2" />
        <span className="blob blob-3" />
      </div>
      <Router>
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route path="/feed" element={<RequireAuth><Feed /></RequireAuth>} />
          <Route path="/profile" element={<RequireAuth><Profile /></RequireAuth>} />
          <Route path="/" element={<Navigate to={token ? '/feed' : '/login'} replace />} />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </Router>
    </div>
  )
}

export default App