import React, {useState} from 'react'
import {useNavigate, Link} from 'react-router-dom'
import api from '../services/api'
import './Auth.css'

const Register = () => {
  const [name, setName] = useState('')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [college, setCollege] = useState('')
  const [message, setMessage] = useState('')
  const navigate = useNavigate()

  const submit = async (e) => {
    e.preventDefault()
    setMessage('')
    try {
      await api.post('/auth/register', {name, email, password, college})
      setMessage('Registration successful. Redirecting to login...')
      setTimeout(() => navigate('/login'), 900)
    } catch (err) {
      setMessage(err?.response?.data?.message || 'Register failed')
    }
  }

  return (
    <div className="auth-screen auth-registration">
      <div className="auth-hero">
        <div className="auth-badge">Campus Connect</div>
        <h1>A premium campus network for student creators.</h1>
        <p>Launch your college community with a modern feed, member profiles, and polished connections.</p>
        <div className="auth-feature-grid">
          <div><strong>World-class design</strong><span>Impress with every post and profile.</span></div>
          <div><strong>Secure sign-up</strong><span>Simple onboarding for every student.</span></div>
          <div><strong>Built for teams</strong><span>Campus clubs, collabs, and events.</span></div>
        </div>
      </div>

      <div className="auth-panel">
        <div className="auth-panel-header">
          <div>
            <h2>Create your Campus Connect account</h2>
            <p>Step into the most elegant campus social experience.</p>
          </div>
          <span className="auth-pill">Startup quality</span>
        </div>
        <form className="auth-form" onSubmit={submit}>
          <label>Full Name</label>
          <input value={name} onChange={(e) => setName(e.target.value)} placeholder="Shaili" required />
          <label>College Email</label>
          <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} placeholder="you@campus.edu" required />
          <label>Password</label>
          <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} placeholder="Strong password" required />
          <label>College</label>
          <input value={college} onChange={(e) => setCollege(e.target.value)} placeholder="Jain University" required />
          <button className="auth-submit" type="submit">Start building</button>
          {message && <p className="auth-message">{message}</p>}
        </form>
        <div className="auth-footer">
          <span>Already registered?</span>
          <Link to="/login">Sign in instead</Link>
        </div>
      </div>
    </div>
  )
}

export default Register
