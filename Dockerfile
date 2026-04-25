# Use a lightweight Alpine Linux image with GCC
FROM alpine:latest

# Install g++ and required libraries
RUN apk add --no-cache g++ libstdc++

# Set working directory
WORKDIR /app

# Copy source code and dataset
COPY server.cpp trie.h dataset.txt ./
COPY index.html definition.html about.html style.css script.js trie_engine.js ./

# Compile the C++ application
# Since we are on Linux, the #else block in server.cpp will use POSIX sockets
RUN g++ -O3 -Wall server.cpp -o server

# Expose the API port
EXPOSE 8080

# Run the server
CMD ["./server"]
