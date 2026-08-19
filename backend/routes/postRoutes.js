const express = require("express");
const router = express.Router();

const protect = require("../middleware/authMiddleware");

const {
  createPost,
  getPosts,
  likePost,
  commentPost,
  deletePost
} = require("../controllers/postController");

router.post("/create", protect, createPost);
router.get("/", getPosts);
router.post("/like/:id", protect, likePost);
router.post("/comment/:id", protect, commentPost);
router.delete("/:id", protect, deletePost);

module.exports = router;