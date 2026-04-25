#include <iostream>
#include <string>
#include <vector>
#include <sstream>
#include <fstream>
#ifdef _WIN32
#include <winsock2.h>
#include <ws2tcpip.h>
#pragma comment(lib, "ws2_32.lib")
#else
#include <sys/socket.h>
#include <netinet/in.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <cstring>
#define SOCKET int
#define INVALID_SOCKET -1
#define SOCKET_ERROR -1
#define closesocket close
#define WSACleanup()
#endif
#include "trie.h"

using namespace std;

const int PORT = 8080;
const int BUFFER_SIZE = 4096;

// Global Trie instance
Trie trie;

// Function to load dictionary words with descriptions from file
void loadDictionary() {
    ifstream file("dataset.txt");
    if (!file.is_open()) {
        cerr << "ERROR: Could not open dataset.txt! Make sure it exists in the same directory." << endl;
        return;
    }

    string line;
    int count = 0;
    while (getline(file, line)) {
        size_t delimiterPos = line.find('|');
        if (delimiterPos != string::npos) {
            string word = line.substr(0, delimiterPos);
            string desc = line.substr(delimiterPos + 1);
            
            // Trim potential whitespace (though dataset.txt should be clean)
            // Sticking to simple logic for now
            
            trie.insert(word, desc);
            count++;
        }
    }
    file.close();
    cout << "Dictionary loaded with " << count << " definitions from dataset.txt." << endl;
}

// Function to read file content
string readFile(const string& path) {
    ifstream file(path, ios::binary); // Open in binary mode
    if (!file) return "";
    stringstream buffer;
    buffer << file.rdbuf();
    return buffer.str();
}

// Function to get MIME type
string getMimeType(const string& path) {
    if (path.find(".html") != string::npos) return "text/html";
    if (path.find(".css") != string::npos) return "text/css";
    if (path.find(".js") != string::npos) return "application/javascript";
    if (path.find(".json") != string::npos) return "application/json";
    return "text/plain";
}

struct NLPResult {
    bool isComparison = false;
    string mainWord1 = "";
    string mainWord2 = "";
    string singleWord = "";
};

string urlDecode(string str) {
    string ret;
    for (size_t i=0; i<str.length(); i++) {
        if (str[i] == '%') {
            if (i + 2 < str.length()) {
                int ii = stoi(str.substr(i+1, 2), nullptr, 16);
                ret += static_cast<char>(ii);
                i += 2;
            }
        } else if (str[i] == '+') {
            ret += ' ';
        } else {
            ret += str[i];
        }
    }
    return ret;
}

NLPResult processQuery(string query) {
    NLPResult res;
    string decoded = urlDecode(query);
    
    // Convert to lowercase
    for (char& c : decoded) {
        c = tolower(c);
    }

    // Is it a comparison?
    size_t vsPos = decoded.find(" vs ");
    size_t diffPos = decoded.find("difference");
    size_t andPos = decoded.find(" and ");

    if (vsPos != string::npos) {
        res.isComparison = true;
        res.mainWord1 = decoded.substr(0, vsPos);
        res.mainWord2 = decoded.substr(vsPos + 4);
    } else if (diffPos != string::npos && andPos != string::npos && andPos > diffPos) {
        res.isComparison = true;
        size_t betweenPos = decoded.find("between ");
        size_t startWord1 = (betweenPos != string::npos) ? betweenPos + 8 : diffPos + 10;
        
        if (andPos > startWord1) {
            res.mainWord1 = decoded.substr(startWord1, andPos - startWord1);
            res.mainWord2 = decoded.substr(andPos + 5);
        }
    }

    auto cleanWord = [](string w) {
        vector<string> prefixesToRemove = {
            "what is a ", "what is an ", "what is the ", "what is ",
            "what are ", "explain ", "define ", "meaning of ", "who is ", "the "
        };
        for (string prefix : prefixesToRemove) {
            if (w.find(prefix) == 0) {
                w = w.substr(prefix.length());
                break;
            }
        }
        while(!w.empty() && (w.front() == ' ' || w.front() == '?')) w.erase(w.begin());
        while(!w.empty() && (w.back() == ' ' || w.back() == '?')) w.pop_back();
        return w;
    };

    if (res.isComparison) {
        res.mainWord1 = cleanWord(res.mainWord1);
        res.mainWord2 = cleanWord(res.mainWord2);
        return res;
    }

    res.singleWord = cleanWord(decoded);
    return res;
}

// Function to escape string for JSON
string escapeJson(const string& s) {
    string result = "";
    for (char c : s) {
        if (c == '"') result += "\\\"";
        else if (c == '\\') result += "\\\\";
        else if (c == '\b') result += "\\b";
        else if (c == '\f') result += "\\f";
        else if (c == '\n') result += "\\n";
        else if (c == '\r') result += "\\r";
        else if (c == '\t') result += "\\t";
        else result += c;
    }
    return result;
}

// Function to handle client requests
void handleClient(SOCKET clientSocket) {
    char buffer[BUFFER_SIZE];
    int bytesReceived = recv(clientSocket, buffer, BUFFER_SIZE - 1, 0);
    if (bytesReceived <= 0) return;

    buffer[bytesReceived] = '\0';
    string request(buffer);

    // Simple parsing of the request line
    stringstream ss(request);
    string method, url, version;
    ss >> method >> url >> version;

    cout << "Request: " << method << " " << url << endl;

    string response;
    string body;
    string contentType = "text/plain";
    int statusCode = 200;

    if (method == "GET") {
        if (url.find("/search?q=") == 0) {
            // Handle search API
            string query = url.substr(10);
            NLPResult parsed = processQuery(query);
            
            vector<string> suggestions;
            if (parsed.isComparison) {
                // For comparison queries, no prefix suggestions are needed 
                // Alternatively, could suggest based on the second word.
            } else {
                suggestions = trie.getSuggestions(parsed.singleWord);
            }

            // Construct JSON response manually
            body = "[";
            for (size_t i = 0; i < suggestions.size(); ++i) {
                body += "\"" + suggestions[i] + "\"";
                if (i < suggestions.size() - 1) body += ",";
            }
            body += "]";
            contentType = "application/json";
            
            response = "HTTP/1.1 200 OK\r\nAccess-Control-Allow-Origin: *\r\nCache-Control: no-cache, no-store, must-revalidate\r\nContent-Type: " + contentType + "\r\nContent-Length: " + to_string(body.length()) + "\r\n\r\n" + body;

        } else if (url.find("/define?q=") == 0) {
            // Handle Definition API
            string query = url.substr(10);
            NLPResult parsed = processQuery(query);
            
            if (parsed.isComparison) {
                string desc1 = escapeJson(trie.getDescription(parsed.mainWord1));
                string desc2 = escapeJson(trie.getDescription(parsed.mainWord2));
                
                body = "{ \"type\": \"comparison\", \"word1\": \"" + parsed.mainWord1 + "\", \"desc1\": \"" + desc1 + "\", \"word2\": \"" + parsed.mainWord2 + "\", \"desc2\": \"" + desc2 + "\" }";
            } else {
                string desc = escapeJson(trie.getDescription(parsed.singleWord));
                body = "{ \"type\": \"single\", \"word\": \"" + parsed.singleWord + "\", \"description\": \"" + desc + "\" }";
            }
            contentType = "application/json";
            
            response = "HTTP/1.1 200 OK\r\nAccess-Control-Allow-Origin: *\r\nCache-Control: no-cache, no-store, must-revalidate\r\nContent-Type: " + contentType + "\r\nContent-Length: " + to_string(body.length()) + "\r\n\r\n" + body;

        } else {
            // Handle Static Files
            string filePath = ".";
            if (url == "/") filePath += "/index.html";
            else filePath += url;

            // Remove query params if any meant for static files (unlikely here but good practice)
            size_t qPos = filePath.find('?');
            if (qPos != string::npos) filePath = filePath.substr(0, qPos);

            body = readFile(filePath);
            
            if (!body.empty()) {
                contentType = getMimeType(filePath);
                response = "HTTP/1.1 200 OK\r\nCache-Control: no-cache, no-store, must-revalidate\r\nContent-Type: " + contentType + "\r\nContent-Length: " + to_string(body.length()) + "\r\n\r\n" + body;
            } else {
                body = "404 Not Found";
                statusCode = 404;
                response = "HTTP/1.1 404 Not Found\r\nContent-Type: text/plain\r\nContent-Length: " + to_string(body.length()) + "\r\n\r\n" + body;
            }
        }
    } else {
         body = "Method Not Allowed";
         statusCode = 405;
         response = "HTTP/1.1 405 Method Not Allowed\r\nContent-Type: text/plain\r\nContent-Length: " + to_string(body.length()) + "\r\n\r\n" + body;
    }

    send(clientSocket, response.c_str(), response.length(), 0);
    closesocket(clientSocket);
}

int main() {
    loadDictionary();

#ifdef _WIN32
    WSADATA wsaData;
    if (WSAStartup(MAKEWORD(2, 2), &wsaData) != 0) {
        cerr << "WSAStartup failed" << endl;
        return 1;
    }
#endif

    SOCKET serverSocket = socket(AF_INET, SOCK_STREAM, 0);
    if (serverSocket == INVALID_SOCKET) {
        cerr << "Socket creation failed" << endl;
        WSACleanup();
        return 1;
    }

    sockaddr_in serverAddr;
    serverAddr.sin_family = AF_INET;
    serverAddr.sin_addr.s_addr = INADDR_ANY;
    serverAddr.sin_port = htons(PORT);

    if (bind(serverSocket, (sockaddr*)&serverAddr, sizeof(serverAddr)) == SOCKET_ERROR) {
        cerr << "Bind failed" << endl;
        closesocket(serverSocket);
        WSACleanup();
        return 1;
    }

    if (listen(serverSocket, SOMAXCONN) == SOCKET_ERROR) {
        cerr << "Listen failed" << endl;
        closesocket(serverSocket);
        WSACleanup();
        return 1;
    }

    cout << "Server started on http://localhost:" << PORT << endl;
    cout << "Press Ctrl+C to stop..." << endl;

    while (true) {
        SOCKET clientSocket = accept(serverSocket, nullptr, nullptr);
        if (clientSocket == INVALID_SOCKET) {
            cerr << "Accept failed" << endl;
            continue;
        }
        handleClient(clientSocket);
    }

    closesocket(serverSocket);
    WSACleanup();
    return 0;
}
