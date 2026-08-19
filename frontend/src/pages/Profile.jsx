import React, {useEffect, useState} from 'react'
import api from '../services/api'
import Navbar from '../components/Navbar'
import './Profile.css'

const Profile = () => {
  const [profile, setProfile] = useState(null)
  const [editing, setEditing] = useState(false)
  const [form, setForm] = useState({})
  const [message, setMessage] = useState('')

  const fetchProfile = async () => {
    try {
      const res = await api.get('/user/profile')
      const profileData = res.data?.user || res.data || {}
      setProfile(profileData)
      setForm(profileData)
    } catch (err) {
      console.error(err)
      alert('Failed to load profile')
    }
  }

  useEffect(() => { fetchProfile() }, [])

  const handleChange = (key, value) => setForm((prev) => ({...prev, [key]: value}))

  const submit = async (e) => {
    e.preventDefault()
    setMessage('')
    try {
      const res = await api.put('/user/update', {
        bio: form.bio || '',
        branch: form.branch || '',
        year: form.year || ''
      })
      const updatedUser = res.data?.user || res.data
      if (updatedUser) {
        setProfile(updatedUser)
        setForm(updatedUser)
      }
      setMessage('Profile updated successfully')
      setEditing(false)
      fetchProfile()
    } catch (err) {
      console.error(err)
      setMessage('Update failed')
    }
  }

  if (!profile) return (
    <div className="profile-screen">
      <Navbar />
      <main className="profile-shell">
        <div className="profile-loading">Loading profile...</div>
      </main>
    </div>
  )

  const initials = profile.name?.split(' ').map((part) => part[0]).join('').slice(0,2).toUpperCase()

  return (
    <div className="profile-screen">
      <Navbar />
      <main className="profile-shell">
        <section className="profile-topbar">
          <div className="profile-avatar-card">
            <span className="profile-avatar">{initials || 'CC'}</span>
            <div>
              <p className="profile-label">Campus Creator</p>
              <h1>{profile.name}</h1>
              <p className="profile-bio">{profile.bio || 'Share your story, achievements, and college journey.'}</p>
            </div>
          </div>
          <div className="profile-stats">
            <div><strong>{profile.college || 'Unknown'}</strong><span>College</span></div>
            <div><strong>{profile.branch || 'N/A'}</strong><span>Branch</span></div>
            <div><strong>{profile.year || 'N/A'}</strong><span>Year</span></div>
          </div>
        </section>

        <div className="profile-grid">
          <div className="profile-card summary-card">
            <h2>Profile details</h2>
            <div className="detail-row"><span>Email</span><strong>{profile.email}</strong></div>
            <div className="detail-row"><span>College</span><strong>{profile.college || 'Not set'}</strong></div>
            <div className="detail-row"><span>Branch</span><strong>{profile.branch || 'Not set'}</strong></div>
            <div className="detail-row"><span>Year</span><strong>{profile.year || 'Not set'}</strong></div>
          </div>

          <div className="profile-card edit-card">
            <div className="profile-card-header">
              <div>
                <h2>{editing ? 'Edit profile' : 'Profile actions'}</h2>
                <p>{editing ? 'Update the fields below.' : 'Keep your campus identity sharp.'}</p>
              </div>
              <button className="ghost-button" onClick={() => setEditing((prev) => !prev)}>{editing ? 'Close' : 'Edit'}</button>
            </div>
            {message && <p className="profile-message">{message}</p>}

            {editing ? (
              <form className="profile-edit-form" onSubmit={submit}>
                <label>Name</label>
                <input value={form.name || ''} onChange={(e) => handleChange('name', e.target.value)} />
                <label>College</label>
                <input value={form.college || ''} onChange={(e) => handleChange('college', e.target.value)} />
                <label>Branch</label>
                <input value={form.branch || ''} onChange={(e) => handleChange('branch', e.target.value)} />
                <label>Year</label>
                <input value={form.year || ''} onChange={(e) => handleChange('year', e.target.value)} />
                <label>Bio</label>
                <textarea value={form.bio || ''} onChange={(e) => handleChange('bio', e.target.value)} />
                <button className="auth-submit" type="submit">Save changes</button>
              </form>
            ) : (
              <div className="profile-pro-tip">
                <p>Tip: Add a short bio and your major to make your campus profile feel more polished.</p>
              </div>
            )}
          </div>
        </div>
      </main>
    </div>
  )
}

export default Profile
