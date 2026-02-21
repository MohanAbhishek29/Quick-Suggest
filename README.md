<h1 align="center">
  <br>
  Quick-Suggest 🚀
  <br>
</h1>

<h4 align="center">A Lightning-Fast C++ Powered Search Engine built with WinSock2 & Tries.</h4>

<p align="center">
  <a href="#key-features">Key Features</a> •
  <a href="#architecture">Architecture</a> •
  <a href="#how-to-run">How to Run</a> •
  <a href="#nlp--comparisons">NLP Search</a>
</p>

![Screenshot of Quick-Suggest](https://raw.githubusercontent.com/MohanAbhishek29/Quick-Suggest/main/media.png)

---

## ⚡ Overview

**Quick-Suggest** is not your average autocomplete bar. Built entirely from scratch for an Advanced Data Structures and Algorithms (DSA) project, it is a fully functioning network search engine. The backend is written entirely in **C++** using low-level socket programming (`WinSock2`), while the frontend is a modern, responsive Glassmorphism UI.

The core technology relies on a custom **Trie (Prefix Tree) Data Structure** to achieve massive scalability. Search complexity is strictly **O(L)** (where L is the length of the query), completely independent of the dataset size!

## ✨ Key Features

- **Blazing Fast Autocomplete:** Powered by C++ Prefix Trees (Tries) for instant O(L) time complexity lookups.
- **Custom HTTP Web Server:** No node.js or python backends here; the HTTP request parsing, routing, and CORS handling is written directly in C++ via the WinSock2 library.
- **Dynamic NLP processing:** Stop words (e.g., "what is the meaning of...") are automatically stripped at the socket level.
- **A/B Comparison Engine:** Searches like "Difference between Stack and Queue" trigger a dual-Trie lookup, returning a side-by-side comparative UI.
- **Real-Time Voice Search:** Integrated with Browser Speech API to allow completely hands-free navigation.
- **Rich Tech Dataset:** Over 300+ Computer Science, DSA, and Software Engineering definitions parsed locally into the Trie from `dataset.txt`.

## 🏗️ Architecture Stack

### Backend (C++)
* `server.cpp`: Manual TCP/IP socket binding, static file serving, and JSON API Endpoint (`/search` and `/define`).
* `trie.h`: Core data structure for prefix storing and Depth-First-Search (DFS) retrieval.

### Frontend
* Pure `HTML`, `Vanilla JS`, and `CSS`.
* Features custom animations, fluid glassmorphism, dynamic DOM injection for dual-view comparisons, and LocalStorage for recent history.

## 🚀 How To Run (Windows)

Because the HTTP server is built on WinSock2, it requires a Windows environment to run the backend natively.

1. **Clone the repository:**
   ```bash
   git clone https://github.com/MohanAbhishek29/Quick-Suggest.git
   cd Quick-Suggest
   ```
2. **Compile the C++ Server:**
   Double-click the `build.bat` file, or run:
   ```cmd
   g++ -O3 -Wall server.cpp -o server.exe -lws2_32
   ```
   *(Ensure you have MinGW / GCC installed and added to your system PATH)*
3. **Start the Engine:**
   Double-click `run.bat`, or run:
   ```cmd
   .\server.exe
   ```
4. **Search!**
   Open your browser and navigate to `http://localhost:8080/`.

## 🧠 Advanced NLP & Comparisons

Try these exact queries in the search bar to see the NLP Engine in action:

* `what is an algorithm` *(Auto-strips the stop words and searches "algorithm")*
* `difference between stack and queue` *(Detects comparison intent and returns a split-screen view)*
* `c++ vs java` *(Parses the "vs" operator and searches both independently)*

---

<p align="center">
  <i>Built for Advanced DSA Module • 2026</i>
</p>
