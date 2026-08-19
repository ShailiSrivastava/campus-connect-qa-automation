import React, {useEffect, useState, useCallback} from 'react'
import api from '../services/api'
import Navbar from '../components/Navbar'
import PostCard from '../components/PostCard'
import CreatePost from '../components/CreatePost'
import './Feed.css'

const Feed = () => {
  const [posts, setPosts] = useState([])
  const [loading, setLoading] = useState(true)

  const fetchPosts = useCallback(async () => {
    setLoading(true)
    try {
      const res = await api.get('/posts')
      const payload = res.data?.posts ?? res.data ?? []
      setPosts(Array.isArray(payload) ? payload : [])
    } catch (err) {
      console.error(err)
      alert('Failed to load posts')
    } finally {
      setLoading(false)
    }
  }, [])

  useEffect(() => { fetchPosts() }, [fetchPosts])

  return (
    <div className="feed-screen">
      <Navbar />
      <main className="feed-shell">
        <section className="feed-hero-panel">
          <div className="feed-hero-copy">
            <span className="pill">Campus Network</span>
            <h1>Stay visible, share wins, and build campus momentum.</h1>
            <p>Modern feed, polished cards, and fast campus discovery designed for student teams.</p>
          </div>
          <div className="feed-hero-charts">
            <div className="stat-card">
              <span>Members</span>
              <strong>1.2k</strong>
            </div>
            <div className="stat-card">
              <span>Live threads</span>
              <strong>{posts.length}</strong>
            </div>
            <div className="stat-card">
              <span>Weekly reactions</span>
              <strong>{posts.length * 4}</strong>
            </div>
          </div>
        </section>

        <div className="feed-grid">
          <section className="feed-main">
            <CreatePost onCreated={fetchPosts} />
            {loading ? (
              <div className="feed-loading">
                <div className="spinner" />
                <p>Loading campus posts...</p>
              </div>
            ) : posts.length ? (
              posts.map((post) => <PostCard key={post._id || post.id} post={post} />)
            ) : (
              <div className="feed-empty-state">
                <div className="empty-illustration">
                  <div className="empty-blob empty-blob-1" />
                  <div className="empty-blob empty-blob-2" />
                  <div className="empty-illustration-card">
                    <h2>No posts yet</h2>
                    <p>Your campus community is just warming up. Share the first update to spark a conversation.</p>
                    <button onClick={() => document.querySelector('.cc-createpost input')?.focus()}>Create first post</button>
                  </div>
                </div>
              </div>
            )}
          </section>

          <aside className="feed-sidebar">
            <div className="panel-card">
              <div className="panel-header">
                <h3>Trending on Campus</h3>
                <span>Live</span>
              </div>
              <ul>
                <li>#Hackathon2026</li>
                <li>#ProjectShowcase</li>
                <li>#CollegeLife</li>
              </ul>
            </div>
            <div className="panel-card">
              <h3>Upcoming events</h3>
              <div className="event-chip">
                <strong>Design Sprint</strong>
                <span>Tomorrow • 6PM</span>
              </div>
              <div className="event-chip">
                <strong>Club Meetup</strong>
                <span>Fri • 4PM</span>
              </div>
            </div>
            <div className="panel-card panel-coaching">
              <h3>Pro tip</h3>
              <p>Use crisp headlines and clear contexts so your campus post gets more engagement.</p>
            </div>
          </aside>
        </div>
      </main>
    </div>
  )
}

export default Feed
