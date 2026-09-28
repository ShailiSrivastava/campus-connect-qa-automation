const mongoose = require("mongoose");

const connectDB = async () => {
  const mongoUri = process.env.MONGODB_URI || process.env.MONGO_URI;

  if (mongoUri) {
    try {
      await mongoose.connect(mongoUri, {
        serverSelectionTimeoutMS: 5000,
      });
      console.log("MongoDB Connected successfully.");
      return;
    } catch (error) {
      console.error("MongoDB connection error:", error.message);
      if (process.env.NODE_ENV === "production") {
        console.error("FATAL: Failed to connect to MongoDB instance in production mode.");
        process.exit(1);
      }
      console.warn("Attempting MongoMemoryServer fallback for local testing...");
    }
  }

  if (process.env.NODE_ENV === "production") {
    console.error("FATAL: MONGODB_URI or MONGO_URI environment variable is not defined in production.");
    process.exit(1);
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