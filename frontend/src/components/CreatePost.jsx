import React, {useState} from 'react'
import api from '../services/api'
import './CreatePost.css'

const CreatePost = ({onCreated}) => {
  const [title, setTitle] = useState('')
  const [content, setContent] = useState('')
  const [loading, setLoading] = useState(false)
  const [status, setStatus] = useState('')

  const submit = async (e) => {
    e.preventDefault()
    if (!title.trim() || !content.trim()) return
    setLoading(true)
    setStatus('')
    try {
      await api.post('/posts/create', {title, content})
      setTitle('')
      setContent('')
      setStatus('Your post is live!')
      onCreated && onCreated()
    } catch (err) {
      console.error(err)
      setStatus(err?.response?.data?.message || 'Failed to create post')
    } finally {
      setLoading(false)
    }
  }

  return (
    <form className="cc-createpost" onSubmit={submit}>
      <div className="create-headline">
        <div>
          <h2>Share a campus update</h2>
          <p>Help your classmates discover what you’re building.</p>
        </div>
        <span className="status-chip">Live</span>
      </div>
      <input placeholder="Post title" value={title} onChange={(e) => setTitle(e.target.value)} />
      <textarea placeholder="What are you working on?" value={content} onChange={(e) => setContent(e.target.value)} />
      <div className="cc-create-actions">
        <button type="submit" disabled={loading}>{loading ? 'Publishing...' : 'Post update'}</button>
      </div>
      {status && <div className="cc-status">{status}</div>}
    </form>
  )
}

export default CreatePost
