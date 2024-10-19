# Video Transcription & Clipper

This is a Python-based desktop application for video transcription and clipping, built with Tkinter. The app allows users to upload videos, transcribe the content into subtitles (.srt), and cut videos into smaller clips based on user-defined timestamps.

## Features

- Upload video files (.mp4, .mov, .avi)
- Generate transcription files (.srt) using Whisper (AI transcription)
- Create video clips by specifying start and end timestamps
- Save generated clips and transcription files to a designated folder

---

## Table of Contents

- [Requirements](#requirements)
- [Installation](#installation)
  - [Setup for Development](#setup-for-development)
  - [Build as Executable](#build-as-executable)
  - [Create an Installer](#create-an-installer)
- [Usage](#usage)
- [Folder Structure](#folder-structure)
- [License](#license)

---

## Requirements

Make sure you have the following installed before running or building the application:

1. **Python 3.8+**
2. **Pip package manager**

### Required Python Packages:

```bash
pip install tkinter Pillow pyinstaller moviepy whisper
