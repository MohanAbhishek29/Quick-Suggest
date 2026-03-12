/**
 * Quick-Suggest Static Engine
 * Ports the C++ Trie and NLP logic to JavaScript for Netlify static hosting.
 */

class TrieNode {
    constructor() {
        this.children = {};
        this.isEndOfWord = false;
        this.description = "";
    }
}

class Trie {
    constructor() {
        this.root = new TrieNode();
    }

    insert(word, description) {
        let current = this.root;
        for (let char of word.toLowerCase()) {
            if (char < 'a' || char > 'z') continue;
            if (!current.children[char]) {
                current.children[char] = new TrieNode();
            }
            current = current.children[char];
        }
        current.isEndOfWord = true;
        current.description = description;
    }

    getSuggestions(prefix, limit = 10) {
        let results = [];
        let current = this.root;
        let cleanPrefix = "";

        for (let char of prefix.toLowerCase()) {
            if (char < 'a' || char > 'z') continue;
            if (!current.children[char]) return [];
            current = current.children[char];
            cleanPrefix += char;
        }

        this._findWords(current, cleanPrefix, results, limit);
        return results;
    }

    _findWords(node, prefix, results, limit) {
        if (results.length >= limit) return;
        if (node.isEndOfWord) {
            results.push(prefix);
        }

        for (let char of "abcdefghijklmnopqrstuvwxyz") {
            if (node.children[char]) {
                this._findWords(node.children[char], prefix + char, results, limit);
                if (results.length >= limit) return;
            }
        }
    }

    getDescription(word) {
        let current = this.root;
        for (let char of word.toLowerCase()) {
            if (char < 'a' || char > 'z') continue;
            if (!current.children[char]) return "Definition not found.";
            current = current.children[char];
        }
        return current.isEndOfWord ? current.description : "Definition not found.";
    }
}

// NLP & Query Processor
const trieEngine = {
    trie: new Trie(),
    isLoaded: false,

    async init() {
        if (this.isLoaded) return;
        try {
            const response = await fetch('dataset.txt');
            const data = await response.text();
            const lines = data.split('\n');
            let count = 0;
            for (let line of lines) {
                const parts = line.split('|');
                if (parts.length >= 2) {
                    this.trie.insert(parts[0].trim(), parts[1].trim());
                    count++;
                }
            }
            console.log(`Static Engine: Loaded ${count} definitions.`);
            this.isLoaded = true;
        } catch (e) {
            console.error("Static Engine: Failed to load dataset.", e);
        }
    },

    processQuery(query) {
        let decoded = decodeURIComponent(query).toLowerCase();
        let res = {
            isComparison: false,
            mainWord1: "",
            mainWord2: "",
            singleWord: ""
        };

        const vsPos = decoded.indexOf(" vs ");
        const diffPos = decoded.indexOf("difference");
        const andPos = decoded.indexOf(" and ");

        if (vsPos !== -1) {
            res.isComparison = true;
            res.mainWord1 = decoded.substring(0, vsPos).trim();
            res.mainWord2 = decoded.substring(vsPos + 4).trim();
        } else if (diffPos !== -1 && andPos !== -1 && andPos > diffPos) {
            res.isComparison = true;
            const betweenPos = decoded.indexOf("between ");
            const startWord1 = (betweenPos !== -1) ? betweenPos + 8 : diffPos + 10;
            if (andPos > startWord1) {
                res.mainWord1 = decoded.substring(startWord1, andPos).trim();
                res.mainWord2 = decoded.substring(andPos + 5).trim();
            }
        }

        const cleanWord = (w) => {
            const prefixes = [
                "what is a ", "what is an ", "what is the ", "what is ",
                "what are ", "explain ", "define ", "meaning of ", "who is ", "the "
            ];
            for (let p of prefixes) {
                if (w.startsWith(p)) {
                    w = w.substring(p.length);
                    break;
                }
            }
            return w.replace(/[?]/g, '').trim();
        };

        if (res.isComparison) {
            res.mainWord1 = cleanWord(res.mainWord1);
            res.mainWord2 = cleanWord(res.mainWord2);
        } else {
            res.singleWord = cleanWord(decoded);
        }
        return res;
    },

    getResults(query) {
        const parsed = this.processQuery(query);
        if (parsed.isComparison) {
            return {
                type: "comparison",
                word1: parsed.mainWord1,
                desc1: this.trie.getDescription(parsed.mainWord1),
                word2: parsed.mainWord2,
                desc2: this.trie.getDescription(parsed.mainWord2)
            };
        } else {
            return {
                type: "single",
                word: parsed.singleWord,
                description: this.trie.getDescription(parsed.singleWord)
            };
        }
    }
};
