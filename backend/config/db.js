const mongoose = require("mongoose");

const connectDB = async () => {
  if (process.env.MONGO_URI) {
    try {
      await mongoose.connect(process.env.MONGO_URI, {
        serverSelectionTimeoutMS: 4000
      });
      console.log("MongoDB Connected");
      return;
    } catch (error) {
      console.warn("Could not connect to configured MONGO_URI, attempting MongoMemoryServer fallback for local testing...", error.message);
    }
  }

  try {
    const { MongoMemoryServer } = require("mongodb-memory-server");
    const mongod = await MongoMemoryServer.create();
    const uri = mongod.getUri();
    await mongoose.connect(uri);
    console.log(`Connected to in-memory MongoDB at ${uri}`);
  } catch (err) {
    console.error("FATAL: Failed to connect to any MongoDB instance:", err);
    process.exit(1);
  }
};

module.exports = connectDB;