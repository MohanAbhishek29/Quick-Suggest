<h1 align="center">
  <br>
  🚀 Quick-Suggest
  <br>
</h1>

<h4 align="center">A Lightning-Fast C++ Powered Search Engine built with Prefix Tries, Docker Microservices, and WinSock2/POSIX Sockets.</h4>

<p align="center">
  <a href="#-core-technology">Core Technology</a> •
  <a href="#-key-features">Key Features</a> •
  <a href="#-architecture--microservices">Architecture</a> •
  <a href="#-how-to-run-locally">How to Run</a> •
  <a href="#-cloud-deployment">Deployment</a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/C++-00599C?style=for-the-badge&logo=c%2B%2B&logoColor=white" />
  <img src="https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white" />
  <img src="https://img.shields.io/badge/Nginx-009639?style=for-the-badge&logo=nginx&logoColor=white" />
  <img src="https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white" />
  <img src="https://img.shields.io/badge/Vanilla_JS-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black" />
</p>

![Screenshot of Quick-Suggest](https://raw.githubusercontent.com/MohanAbhishek29/Quick-Suggest/main/media.png)

---

## ⚡ Overview

**Quick-Suggest** is far more than a simple autocomplete bar. Originally built for an Advanced Data Structures and Algorithms (DSA) project, it has evolved into a highly scalable, containerized network search engine. 

The backend is written entirely from scratch in **C++** using cross-platform socket programming (`WinSock2` & `POSIX`). The frontend boasts a stunning, responsive **Glassmorphism UI** equipped with Voice Search and Natural Language Processing (NLP).

## 🧠 Core Technology

At the heart of the engine lies a custom **Trie (Prefix Tree) Data Structure**. 
Unlike traditional databases that search in $O(N)$ or $O(\log N)$ time, this engine retrieves results in strict **$O(L)$ time complexity** (where $L$ is the length of your query), completely irrespective of the dataset size!

## ✨ Key Features

- 🏎️ **Blazing Fast Autocomplete:** Powered by C++ Prefix Trees for instantaneous keystroke-level responses.
- 🌐 **Custom HTTP Web Server:** Zero backend frameworks (No Node.js/Python). HTTP parsing, routing, and CORS handling are written natively in C++.
- 🗣️ **Real-Time Voice Search:** Integrated with the Web Speech API for a completely hands-free, sci-fi search experience.
- 🤖 **Advanced NLP Engine:** Automatically strips conversational "stop words" (e.g., *"what is the meaning of..."*) at the socket level.
- ⚖️ **A/B Comparison View:** Queries like *"Difference between Stack and Queue"* trigger a dual-Trie lookup, dynamically rendering a side-by-side comparison UI.
- 🐳 **Dockerized Microservices:** Fully orchestrated with Docker Compose and an Nginx Load Balancer to achieve true horizontal scalability.

## 🏗️ Architecture & Microservices

The project utilizes a scalable microservice architecture:
1. **The Backend Nodes:** Three (3) identical instances of the C++ HTTP server running simultaneously inside lightweight Alpine Linux containers.
2. **The Load Balancer:** An Nginx reverse proxy listening on port 80, distributing incoming traffic across the three C++ backends using a round-robin algorithm.

*For detailed microservice documentation, see [MICROSERVICES_DOCS.md](./MICROSERVICES_DOCS.md).*

## 🚀 How To Run Locally

You can run this project either natively on Windows or via Docker.

### Option 1: Native Windows (MinGW)
1. Double-click `build.bat` to compile `server.cpp` using WinSock2.
2. Double-click `run.bat` to start the server.
3. Open `http://localhost:8080/` in your browser.

### Option 2: Docker Microservices (Any OS)
1. Ensure you have Docker Desktop installed.
2. Run the following command in your terminal:
   ```bash
   docker-compose up --build -d
   ```
3. Open `http://localhost/` (Port 80) in your browser.

## ☁️ Cloud Deployment (Netlify)

To deploy this project globally without managing a cloud server, the frontend includes a static fallback engine!
- Upload the contents of the `/dist` folder to **Netlify**, **Vercel**, or **GitHub Pages**.
- The UI will automatically detect that the C++ server is offline and seamlessly switch to the standalone **JavaScript-powered Trie Engine** (`trie_engine.js`), providing the exact same experience directly in the browser!

---

<p align="center">
  <i>Engineered for Advanced DSA & Scalable Systems Architecture • 2026</i>
</p>
