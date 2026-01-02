import express from "express";
import {
  uploadImage,
  getMyImages,
  getUserImages,
  deleteImage,
  getRandomImages,
} from "../controllers/image.controller.js";
import authMiddleware from "../middlewares/auth.middleware.js";

const imageRoutes = express.Router();



imageRoutes.post("/upload", authMiddleware, uploadImage);
imageRoutes.get("/myimages", authMiddleware, getMyImages);
imageRoutes.get("/user/:username", getUserImages);
imageRoutes.delete("/:id", authMiddleware, deleteImage);
imageRoutes.get("/random", getRandomImages);

export default imageRoutes;
