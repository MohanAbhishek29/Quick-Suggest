# Task 2: Scalable Microservice Architecture using Docker

This document explains the containerization and microservice architecture implemented for the **Quick-Suggest** C++ backend.

## Overview
The Quick-Suggest search engine originally ran natively on Windows utilizing `WinSock2` APIs. To satisfy the requirements for deploying a **scalable microservice architecture** using Docker, the C++ networking logic was refactored with cross-platform preprocessor macros (`#ifdef _WIN32`). 

This architecture allows the exact same `server.cpp` code to compile natively on Windows and simultaneously inside a lightweight Linux Docker container utilizing standard POSIX sockets (`<sys/socket.h>`).

## Container Architecture
The microservice architecture relies on **Docker Compose** to spin up multiple instances of the backend service and a reverse proxy load balancer.

### 1. Backend Service (C++)
The custom C++ HTTP Server is containerized using an `alpine` Linux image. 
- **Base Image:** `alpine:latest`
- **Compiler:** GNU C++ Compiler (`g++`)
- **Port:** Exposes Port `8080`
- **Data Load:** Each container loads the `dataset.txt` into memory (Trie Data Structure) upon startup.

### 2. Load Balancer (Nginx)
To make the architecture **scalable**, a single backend instance is not enough. We deployed **three (3) identical replicas** of the C++ backend service and placed an Nginx load balancer in front of them.
- **Base Image:** `nginx:alpine`
- **Port:** Listens on Port `80` (Standard HTTP)
- **Routing:** Configured to distribute incoming API requests (`/search?q=`, `/define?q=`) across `backend1`, `backend2`, and `backend3` in a **round-robin** fashion.

## How It Works (Microservice Flow)
1. A user accesses `http://localhost/` in their web browser.
2. The request hits the **Nginx Load Balancer** container running on Port 80.
3. Nginx transparently forwards the request to one of the three backend containers (e.g., `backend2:8080`).
4. The C++ Server inside `backend2` processes the GET request, traverses its in-memory Trie data structure in `O(L)` time, and constructs a JSON response.
5. The JSON response is returned back through Nginx to the user's browser.

## Scaling Up
If the search engine experiences heavier traffic, the architecture is designed to scale horizontally. By modifying the `docker-compose.yml`, or using Docker Swarm / Kubernetes, additional replicas of the C++ backend can be spun up instantly. The Nginx upstream block dynamically balances the load across all available nodes, preventing any single C++ server from being overwhelmed.

## Execution
To spin up the entire microservice architecture:
```bash
docker-compose up --build -d
```
The application will then be available universally at `http://localhost/`.
