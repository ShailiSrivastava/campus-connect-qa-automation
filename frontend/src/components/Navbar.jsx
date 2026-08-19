import React from 'react'
import { NavLink, useNavigate } from 'react-router-dom'
import './Navbar.css'

const Navbar = () => {
  const navigate = useNavigate()

  const handleLogout = () => {
    localStorage.removeItem('token')
    navigate('/login')
  }

  return (
    <nav className="cc-navbar">
      <div className="cc-brand" onClick={() => navigate('/feed')}>
        <span className="brand-mark">CC</span>
        <div>
          <strong>Campus Connect</strong>
          <span>Campus social made premium</span>
        </div>
      </div>
      <div className="cc-links">
        <NavLink to="/feed" className={({isActive}) => isActive ? 'active' : ''}>Feed</NavLink>
        <NavLink to="/profile" className={({isActive}) => isActive ? 'active' : ''}>Profile</NavLink>
        <button className="cc-logout" onClick={handleLogout}>Logout</button>
      </div>
    </nav>
  )
}

export default Navbar
