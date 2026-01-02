import express from "express";
import dotenv from "dotenv";
import cors from "cors";
import cookieParser from "cookie-parser";
import connectDB from "./config/db.js";
import authRoutes from "./routes/auth.routes.js";
import imageRoutes from "./routes/image.routes.js";

dotenv.config();

const app = express();

app.use(
  cors({
    origin: [
      "http://localhost:5173",
      "https://creative-showcase-nine.vercel.app/",
    ],
    credentials: true,
  })
);

app.use(express.json({ limit: "10mb" }));
app.use(express.urlencoded({ extended: true }));
app.use(cookieParser());

connectDB();



app.use("/api/v1/auth", authRoutes);
app.use("/api/v1/images", imageRoutes);

const PORT = process.env.PORT;

app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
