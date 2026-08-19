const Post = require("../models/Post");

// Create Post
const createPost = async (req, res) => {
  try {
    const { title, content } = req.body;

    const post = await Post.create({
      title,
      content,
      author: req.user.id
    });

    res.status(201).json({
      success: true,
      post
    });

  } catch (error) {
    res.status(500).json({
      success: false,
      error: error.message
    });
  }
};

// Get All Posts
const getPosts = async (req, res) => {
  try {
    const posts = await Post.find()
      .populate("author", "name email")
      .sort({ createdAt: -1 });

    res.status(200).json({
      success: true,
      posts
    });

  } catch (error) {
    res.status(500).json({
      success: false,
      error: error.message
    });
  }
};

// Like Post
const likePost = async (req, res) => {
  res.json({
    success: true,
    message: "Like route working"
  });
};

// Comment Post
const commentPost = async (req, res) => {
  res.json({
    success: true,
    message: "Comment route working"
  });
};

// Delete Post
const deletePost = async (req, res) => {
  res.json({
    success: true,
    message: "Delete route working"
  });
};

module.exports = {
  createPost,
  getPosts,
  likePost,
  commentPost,
  deletePost
};