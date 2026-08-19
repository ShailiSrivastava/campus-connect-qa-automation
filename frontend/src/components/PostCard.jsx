import React, {useState} from 'react'
import './PostCard.css'

const PostCard = ({post}) => {
  const [likes, setLikes] = useState(Array.isArray(post.likes) ? post.likes.length : post.likes || 0)
  const created = new Date(post.createdAt || post.created || Date.now())

  const handleLike = () => setLikes((prev) => prev + 1)

  const authorName = post.authorName || (post.author && post.author.name) || post.author || 'Unknown'
  const likesCount = likes

  return (
    <article className="cc-postcard">
      <div className="post-badge">Campus life</div>
      <header className="cc-post-header">
        <h3>{post.title || 'Untitled update'}</h3>
        <div className="cc-post-meta">by {authorName} • {created.toLocaleString()}</div>
      </header>
      <div className="cc-post-body">{post.content || 'No description available.'}</div>
      <div className="cc-post-actions">
        <button type="button" className="cc-like" onClick={handleLike}>
          <span>👍</span> Like <strong>{likesCount}</strong>
        </button>
      </div>
    </article>
  )
}

export default PostCard
