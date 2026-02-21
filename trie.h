#ifndef TRIE_H
#define TRIE_H

#include <iostream>
#include <vector>
#include <string>
#include <algorithm>
#include <unordered_map>

using namespace std;

// Trie Node Structure
class TrieNode {
public:
    unordered_map<char, TrieNode*> children;
    bool isEndOfWord;
    string description;

    TrieNode() {
        isEndOfWord = false;
        description = "";
    }
};

// Trie Class
class Trie {
private:
    TrieNode* root;

    // Helper function for DFS to find words
    void findWords(TrieNode* node, string prefix, vector<string>& results, int limit) {
        if (results.size() >= limit) return;
        
        if (node->isEndOfWord) {
            results.push_back(prefix);
        }
        
        for (char c = 'a'; c <= 'z'; c++) {
            if (node->children.find(c) != node->children.end()) {
                findWords(node->children[c], prefix + c, results, limit);
                if (results.size() >= limit) return;
            }
        }
    }

public:
    Trie() {
        root = new TrieNode();
    }

    // Insert a word into the Trie with a description
    void insert(string word, string description = "") {
        TrieNode* current = root;
        for (char c : word) {
            // Convert to lowercase to be case-insensitive
            c = tolower(c);
            if (c < 'a' || c > 'z') continue; // Skip non-alphabetic characters
            
            if (current->children.find(c) == current->children.end()) {
                current->children[c] = new TrieNode();
            }
            current = current->children[c];
        }
        current->isEndOfWord = true;
        current->description = description;
    }

    // Get suggestions based on a prefix
    vector<string> getSuggestions(string prefix, int limit = 10) {
        vector<string> results;
        TrieNode* current = root;
        string cleanPrefix = "";

        // Navigate to the end of the prefix
        for (char c : prefix) {
            c = tolower(c);
             if (c < 'a' || c > 'z') continue;
            
            if (current->children.find(c) == current->children.end()) {
                return results; // Prefix not found
            }
            current = current->children[c];
            cleanPrefix += c;
        }

        // Perform DFS from current node to find all words
        findWords(current, cleanPrefix, results, limit);
        return results;
    }

    // Get description for a specific word
    string getDescription(string word) {
        TrieNode* current = root;
        for (char c : word) {
            c = tolower(c);
            if (c < 'a' || c > 'z') continue;
            if (current->children.find(c) == current->children.end()) {
                return "Definition not found.";
            }
            current = current->children[c];
        }
        if (current->isEndOfWord) {
            return current->description;
        }
        return "Definition not found.";
    }
};

#endif
