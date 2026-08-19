const User = require("../models/User");

// GET PROFILE
const getProfile = async (req, res) => {
  try {
    const user = await User.findById(req.user.id).select("-password");

    res.status(200).json({
      success: true,
      user
    });

  } catch (error) {
    res.status(500).json({
      success: false,
      error: error.message
    });
  }
};

// UPDATE PROFILE
const updateProfile = async (req, res) => {
  try {
    const { bio, branch, year } = req.body;

    const user = await User.findByIdAndUpdate(
      req.user.id,
      {
        bio,
        branch,
        year
      },
      {
        new: true
      }
    ).select("-password");

    res.status(200).json({
      success: true,
      message: "Profile updated successfully",
      user
    });

  } catch (error) {
    res.status(500).json({
      success: false,
      error: error.message
    });
  }
};

module.exports = {
  getProfile,
  updateProfile
};