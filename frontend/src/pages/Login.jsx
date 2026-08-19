import React, {useState} from 'react'
import {useNavigate, Link} from 'react-router-dom'
import api from '../services/api'
import './Auth.css'

const Login = () => {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [loading, setLoading] = useState(false)
  const [message, setMessage] = useState('')
  const navigate = useNavigate()

  const submit = async (e) => {
    e.preventDefault()
    setLoading(true)
    setMessage('')
    try {
      const res = await api.post('/auth/login', {email, password})
      const token = res.data.token || res.data
      localStorage.setItem('token', token)
      navigate('/feed')
    } catch (err) {
      setMessage(err?.response?.data?.message || 'Login failed')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="auth-screen">
      <div className="auth-hero">
        <div className="auth-badge">Campus Connect</div>
        <h1>Where campus stories become momentum.</h1>
        <p>Build your student network with a sleek feed, interactive groups, and polished profile presence.</p>
        <div className="auth-feature-grid">
          <div><strong>Share ideas</strong><span>Post updates in real time.</span></div>
          <div><strong>Stay visible</strong><span>Showcase your campus identity.</span></div>
          <div><strong>Grow fast</strong><span>Connect with classmates and alumni.</span></div>
        </div>
      </div>

      <div className="auth-panel">
        <div className="auth-panel-header">
          <div>
            <h2>Login to your campus hub</h2>
            <p>Secure, fast, and beautiful for college communities.</p>
          </div>
          <span className="auth-pill">Hackathon-ready</span>
        </div>
        <form className="auth-form" onSubmit={submit}>
          <label>Email</label>
          <input type="email" placeholder="hello@college.edu" value={email} onChange={(e) => setEmail(e.target.value)} required />
          <label>Password</label>
          <input type="password" placeholder="••••••••" value={password} onChange={(e) => setPassword(e.target.value)} required />
          <button className="auth-submit" type="submit" disabled={loading}>{loading ? 'Entering campus...' : 'Login'}</button>
          {message && <p className="auth-message">{message}</p>}
        </form>
        <div className="auth-footer">
          <span>New to Campus Connect?</span>
          <Link to="/register">Create an account</Link>
        </div>
      </div>
    </div>
  )
}

export default Login
