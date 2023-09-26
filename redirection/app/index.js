const express = require("express");
const mongoose = require("mongoose");
const { exec } = require("child_process");
const fs = require("fs");
const multer = require("multer");
const path = require("path");
const app = express();
const port = 3000;
const fileNameRegex = /^[a-zA-Z0-9_./>\s]+$/;

const storage = multer.diskStorage({
  destination: (req, file, cb) => {
    cb(null, "uploads");
  },
  filename: (req, file, cb) => {
    const date = new Date();
    const formattedDate = `${date.getFullYear()}${(date.getMonth() + 1)
      .toString()
      .padStart(2, "0")}${date.getDate().toString().padStart(2, "0")}${date
      .getHours()
      .toString()
      .padStart(2, "0")}${date.getMinutes().toString().padStart(2, "0")}${date
      .getSeconds()
      .toString()
      .padStart(2, "0")}`;
    const originalname = file.originalname.replace(/[^a-zA-Z0-9.]/g, "");
    const ext = path.extname(file.originalname);
    cb(null, `${formattedDate}${originalname}`);
  },
});

const upload = multer({
  storage,
  fileFilter: (req, file, cb) => {
    const ext = path.extname(file.originalname);
    if (ext !== ".txt") {
      return cb(new Error("Only .txt files are allowed"));
    }
    cb(null, true);
  },
});

app.get("/head/:filename", (req, res) => {
  const filename = req.params.filename;

  if (!filename.match(fileNameRegex)) {
    res.status(400).send("Invalid filename");
    return;
  }
  const folderName = "uploads";
  const command = `head ${folderName}/${filename}`;

  exec(command, (error, stdout, stderr) => {
    if (error) {
      console.error(`Error executing command: ${error}`);
      res.status(500).send(`Error executing command: ${error}`);
      return;
    }

    console.log(`Command output: ${stdout}`);

    if (stderr) {
      console.error(`Command error output: ${stderr}`);
      res.status(500).send(`Command error output: ${stderr}`);
      return;
    }

    res.send(`Command executed!`);
  });
});

app.post("/upload", upload.single("file"), (req, res, next) => {
  res.send("File uploaded successfully");
  next();
});

app.get("/files/:filename", (req, res) => {
  const filename = req.params.filename;

  if (!filename.match(fileNameRegex)) {
    res.status(400).send("Invalid filename");
    return;
  }

  const filePath = `uploads/${filename}`;

  fs.readFile(filePath, "utf-8", (err, data) => {
    if (err) {
      console.error(`Error reading file: ${err}`);
      res.status(500).send(`Error reading file: ${err}`);
      return;
    }

    console.log(`File contents: ${data}`);
    res.send(data);
  });
});

// Start the server
app.listen(port, () => {
  console.log(`App listening at http://localhost:${port}`);
});
