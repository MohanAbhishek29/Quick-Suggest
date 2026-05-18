import os
import shutil

btech_stack = {
    # Core Languages
    "c programming": {"desc": "A procedural programming language developed by Dennis Ritchie, known as the mother of all modern languages.", "characteristics": ["Low-level memory access", "Procedural", "Fast execution"], "types": ["ANSI C", "C99", "C11"]},
    "c++ programming": {"desc": "An extension of C that adds object-oriented programming features.", "characteristics": ["Object-Oriented", "High performance", "Memory management via pointers"], "types": ["C++98", "C++11", "C++14", "C++17"]},
    "java": {"desc": "A high-level, class-based, object-oriented programming language designed to have as few implementation dependencies as possible.", "characteristics": ["Platform Independent (JVM)", "Object-Oriented", "Robust and Secure"], "types": ["Java SE", "Java EE", "Java ME"]},
    "python": {"desc": "An interpreted, high-level, general-purpose programming language.", "characteristics": ["Easy to read and write", "Dynamically typed", "Extensive libraries"], "types": ["CPython", "Jython", "PyPy"]},
    "javascript": {"desc": "A high-level, often just-in-time compiled language that conforms to the ECMAScript standard.", "characteristics": ["Client-side scripting", "Event-driven", "Dynamic typing"], "types": ["Vanilla JS", "ES6+", "Node.js (Backend)"]},
    "typescript": {"desc": "A strict syntactical superset of JavaScript and adds optional static typing to the language.", "characteristics": ["Type safety", "Object-oriented features", "Compiles to JS"], "types": ["Interfaces", "Enums", "Generics"]},
    "golang": {"desc": "A statically typed, compiled programming language designed at Google.", "characteristics": ["Excellent Concurrency (Goroutines)", "Fast compilation", "Garbage collection"], "types": ["Backend API", "Cloud Native Tools"]},
    "rust": {"desc": "A multi-paradigm, general-purpose programming language designed for performance and safety.", "characteristics": ["Memory safety without GC", "Ownership model", "Fearless concurrency"], "types": ["Systems programming", "WebAssembly"]},

    # OOP Concepts
    "object-oriented programming": {"desc": "A programming paradigm based on the concept of 'objects', which can contain data and code.", "characteristics": ["Modularity", "Code Reusability", "Security"], "types": ["Class-based", "Prototype-based"]},
    "encapsulation": {"desc": "The bundling of data with the methods that operate on that data, restricting direct access to some of an object's components.", "characteristics": ["Data hiding", "Improved security", "Modularity"], "types": ["Public", "Private", "Protected"]},
    "inheritance": {"desc": "A mechanism wherein a new class is derived from an existing class.", "characteristics": ["Code Reusability", "Method Overriding", "Hierarchical classification"], "types": ["Single", "Multiple", "Multilevel", "Hierarchical"]},
    "polymorphism": {"desc": "The ability of different objects to respond in a unique way to the same method call.", "characteristics": ["Flexibility", "Code Reusability"], "types": ["Compile-time (Overloading)", "Run-time (Overriding)"]},
    "abstraction": {"desc": "The process of hiding complex implementation details and showing only the essential features of an object.", "characteristics": ["Reduces complexity", "Hides details", "Improves security"], "types": ["Abstract Classes", "Interfaces"]},

    # Data Structures
    "array": {"desc": "A collection of items stored at contiguous memory locations.", "characteristics": ["Fixed size (in many languages)", "Contiguous memory", "O(1) access time"], "types": ["One-dimensional", "Multi-dimensional", "Dynamic Arrays"]},
    "linked list": {"desc": "A linear collection of data elements whose order is not given by their physical placement in memory.", "characteristics": ["Dynamic size", "Ease of insertion/deletion", "No random access"], "types": ["Singly", "Doubly", "Circular"]},
    "stack": {"desc": "A linear data structure which follows a particular order in which the operations are performed (LIFO).", "characteristics": ["LIFO (Last In First Out)", "Only one end (Top) is accessible"], "types": ["Array implementation", "Linked List implementation"]},
    "queue": {"desc": "A linear structure which follows a particular order in which the operations are performed (FIFO).", "characteristics": ["FIFO (First In First Out)", "Two ends (Front and Rear)"], "types": ["Simple Queue", "Circular Queue", "Priority Queue", "Deque"]},
    "tree data structure": {"desc": "A widely used abstract data type that simulates a hierarchical tree structure.", "characteristics": ["Hierarchical", "Root node", "Child nodes"], "types": ["Binary Tree", "Binary Search Tree", "AVL Tree", "Red-Black Tree"]},
    "binary search tree": {"desc": "A node-based binary tree data structure where left child is smaller and right child is greater than parent.", "characteristics": ["O(log n) search time", "Ordered elements"], "types": ["AVL Tree", "Red-Black Tree", "Splay Tree"]},
    "graph data structure": {"desc": "A non-linear data structure consisting of nodes and edges.", "characteristics": ["Vertices and Edges", "Can be cyclic or acyclic"], "types": ["Directed", "Undirected", "Weighted", "Unweighted"]},
    "hash table": {"desc": "A data structure that implements an associative array abstract data type, a structure that can map keys to values.", "characteristics": ["Fast lookups", "Key-value pairs", "Uses hash function"], "types": ["Separate Chaining", "Open Addressing"]},
    "heap data structure": {"desc": "A specialized tree-based data structure which is essentially an almost complete tree that satisfies the heap property.", "characteristics": ["Complete binary tree", "Max or Min property"], "types": ["Min-Heap", "Max-Heap"]},

    # Algorithms
    "sorting algorithms": {"desc": "Algorithms that put elements of a list in a certain order.", "characteristics": ["Time complexity varies", "Space complexity varies", "Stability"], "types": ["Quick Sort", "Merge Sort", "Bubble Sort", "Insertion Sort"]},
    "searching algorithms": {"desc": "Algorithms designed to check for an element or retrieve an element from any data structure where it is stored.", "characteristics": ["Linear vs Logarithmic time"], "types": ["Linear Search", "Binary Search"]},
    "dynamic programming": {"desc": "A method for solving a complex problem by breaking it down into a collection of simpler subproblems.", "characteristics": ["Overlapping subproblems", "Optimal substructure"], "types": ["Memoization (Top-down)", "Tabulation (Bottom-up)"]},
    "greedy algorithms": {"desc": "Any algorithm that follows the problem-solving heuristic of making the locally optimal choice at each stage.", "characteristics": ["Local optimum", "Not always global optimum"], "types": ["Dijkstra's", "Kruskal's", "Prim's"]},
    "divide and conquer": {"desc": "An algorithm design paradigm based on multi-branched recursion.", "characteristics": ["Divide", "Conquer", "Combine"], "types": ["Merge Sort", "Quick Sort"]},
    
    # Operating Systems
    "operating system": {"desc": "System software that manages computer hardware, software resources, and provides common services for computer programs.", "characteristics": ["Resource Management", "Memory Management", "Process Management"], "types": ["Batch OS", "Time-sharing OS", "Distributed OS", "Real-time OS"]},
    "process management": {"desc": "The OS module responsible for managing the execution of processes.", "characteristics": ["Process creation/deletion", "Process scheduling", "Synchronization"], "types": ["FCFS", "SJF", "Round Robin"]},
    "thread": {"desc": "The smallest sequence of programmed instructions that can be managed independently by a scheduler.", "characteristics": ["Lightweight process", "Shares memory with peer threads"], "types": ["User-level threads", "Kernel-level threads"]},
    "deadlock": {"desc": "A state in which each member of a group is waiting for another member, including itself, to take action.", "characteristics": ["Mutual Exclusion", "Hold and Wait", "No Preemption", "Circular Wait"], "types": ["Deadlock Prevention", "Deadlock Avoidance", "Deadlock Detection"]},
    "virtual memory": {"desc": "A memory management capability of an OS that uses hardware and software to allow a computer to compensate for physical memory shortages.", "characteristics": ["Illusion of large memory", "Uses paging", "Disk swapping"], "types": ["Paging", "Segmentation"]},
    "mutex": {"desc": "A mutual exclusion object that allows multiple program threads to share the same resource, such as file access, but not simultaneously.", "characteristics": ["Locking mechanism", "Prevents race conditions", "Owned by a thread"], "types": ["Recursive Mutex", "Non-recursive Mutex"]},
    "semaphore": {"desc": "A variable or abstract data type used to control access to a common resource by multiple processes in a concurrent system.", "characteristics": ["Signaling mechanism", "Can allow multiple threads", "Wait and Signal operations"], "types": ["Binary Semaphore", "Counting Semaphore"]},

    # Computer Networks
    "osi model": {"desc": "A conceptual model that characterizes and standardizes the communication functions of a telecommunication or computing system.", "characteristics": ["7 layers", "Standardized communication", "Encapsulation"], "types": ["Physical", "Data Link", "Network", "Transport", "Session", "Presentation", "Application"]},
    "tcp/ip model": {"desc": "The conceptual model and set of communications protocols used in the Internet and similar computer networks.", "characteristics": ["4 layers", "Basis of the internet"], "types": ["Network Access", "Internet", "Transport", "Application"]},
    "ip address": {"desc": "A numerical label assigned to each device connected to a computer network that uses the Internet Protocol for communication.", "characteristics": ["Unique identifier", "Logical address"], "types": ["IPv4", "IPv6", "Public", "Private"]},
    "dns": {"desc": "The Domain Name System is a hierarchical and decentralized naming system for computers, services, or other resources.", "characteristics": ["Translates domain names to IP", "Distributed database"], "types": ["Root server", "TLD server", "Authoritative server"]},
    "http / https": {"desc": "Hypertext Transfer Protocol (Secure) is the foundation of data communication for the World Wide Web.", "characteristics": ["Client-server protocol", "Stateless", "Encrypted (in HTTPS)"], "types": ["HTTP/1.1", "HTTP/2", "HTTP/3"]},
    
    # Database Management System (DBMS)
    "dbms": {"desc": "Software that interacts with end users, applications, and the database itself to capture and analyze the data.", "characteristics": ["Data Security", "Data Integrity", "Concurrency Control"], "types": ["Relational (RDBMS)", "NoSQL", "Hierarchical", "Network"]},
    "acid properties": {"desc": "A set of properties of database transactions intended to guarantee data validity despite errors, power failures, and other mishaps.", "characteristics": ["Atomicity", "Consistency", "Isolation", "Durability"], "types": ["N/A"]},
    "normalization": {"desc": "The process of structuring a relational database in accordance with a series of so-called normal forms in order to reduce data redundancy.", "characteristics": ["Reduces redundancy", "Improves data integrity"], "types": ["1NF", "2NF", "3NF", "BCNF"]},
    "sql joins": {"desc": "A clause used to combine rows from two or more tables, based on a related column between them.", "characteristics": ["Combines data", "Uses foreign keys"], "types": ["Inner Join", "Left Join", "Right Join", "Full Outer Join"]},
    "mongodb": {"desc": "A source-available cross-platform document-oriented database program, classified as a NoSQL database.", "characteristics": ["JSON-like documents", "Schema-less", "Highly Scalable"], "types": ["Standalone", "Replica Set", "Sharded Cluster"]},
    
    # Web Development
    "html": {"desc": "The standard markup language for documents designed to be displayed in a web browser.", "characteristics": ["Structure of web pages", "Tags and Elements"], "types": ["HTML4", "HTML5"]},
    "css": {"desc": "A style sheet language used for describing the presentation of a document written in HTML.", "characteristics": ["Styling", "Layout", "Responsive design"], "types": ["CSS2", "CSS3", "Flexbox", "Grid"]},
    "react.js": {"desc": "A free and open-source front-end JavaScript library for building user interfaces based on UI components.", "characteristics": ["Virtual DOM", "Component-based", "JSX"], "types": ["Functional Components", "Class Components", "Hooks"]},
    "node.js": {"desc": "A cross-platform, open-source server environment that can run JavaScript on Windows, Linux, Unix, macOS.", "characteristics": ["Asynchronous", "Event-driven", "V8 Engine"], "types": ["Express.js", "NestJS"]},
    
    # Software Engineering & Methodologies
    "sdlc": {"desc": "Software Development Life Cycle is a process used by the software industry to design, develop and test high quality softwares.", "characteristics": ["Structured phases", "Quality assurance"], "types": ["Waterfall", "Agile", "Spiral", "V-Model"]},
    "agile methodology": {"desc": "A practice that promotes continuous iteration of development and testing throughout the software development lifecycle of the project.", "characteristics": ["Iterative", "Incremental", "Customer collaboration"], "types": ["Scrum", "Kanban", "Extreme Programming (XP)"]},
    "software testing": {"desc": "An investigation conducted to provide stakeholders with information about the quality of the software product or service.", "characteristics": ["Bug detection", "Quality assurance"], "types": ["Unit Testing", "Integration Testing", "System Testing", "Acceptance Testing"]},

    # Cybersecurity
    "cryptography": {"desc": "The practice and study of techniques for secure communication in the presence of adversarial behavior.", "characteristics": ["Confidentiality", "Integrity", "Authentication", "Non-repudiation"], "types": ["Symmetric Key", "Asymmetric Key", "Hashing"]},
    "malware": {"desc": "Software intentionally designed to cause disruption to a computer, server, client, or computer network.", "characteristics": ["Malicious intent", "Hidden execution"], "types": ["Virus", "Worm", "Trojan", "Ransomware", "Spyware"]},
    "firewall": {"desc": "A network security system that monitors and controls incoming and outgoing network traffic based on predetermined security rules.", "characteristics": ["Traffic filtering", "Security barrier"], "types": ["Packet-filtering", "Stateful inspection", "Proxy firewall"]},

    # AI & ML
    "machine learning": {"desc": "The study of computer algorithms that can improve automatically through experience and by the use of data.", "characteristics": ["Data-driven", "Pattern recognition", "Predictive capabilities"], "types": ["Supervised", "Unsupervised", "Reinforcement"]},
    "neural networks": {"desc": "Computing systems vaguely inspired by the biological neural networks that constitute animal brains.", "characteristics": ["Hidden layers", "Activation functions", "Weights and Biases"], "types": ["CNN", "RNN", "ANN"]},
    "natural language processing": {"desc": "A subfield of linguistics, computer science, and AI concerned with the interactions between computers and human language.", "characteristics": ["Text analysis", "Speech recognition", "Language translation"], "types": ["Syntax analysis", "Semantics analysis"]}
}

# Cloud & DevOps
cloud_devops = {
    "docker": {"desc": "A platform for developers and sysadmins to build, run, and share applications with containers.", "characteristics": ["Containerization", "Portable", "Lightweight"], "types": ["Images", "Containers", "Volumes"]},
    "kubernetes": {"desc": "An open-source system for automating deployment, scaling, and management of containerized applications.", "characteristics": ["Orchestration", "Auto-scaling", "Self-healing"], "types": ["Pods", "Nodes", "Clusters"]},
    "aws ec2": {"desc": "Amazon Elastic Compute Cloud provides scalable computing capacity in the AWS cloud.", "characteristics": ["Virtual Servers", "Scalable", "Pay-as-you-go"], "types": ["On-Demand", "Reserved", "Spot Instances"]},
    "aws s3": {"desc": "Amazon Simple Storage Service is an object storage service.", "characteristics": ["Highly durable", "Infinite scaling", "Object storage"], "types": ["Standard", "Glacier", "Intelligent-Tiering"]},
    "aws lambda": {"desc": "A serverless compute service that runs your code in response to events and automatically manages the underlying compute resources.", "characteristics": ["Serverless", "Event-driven", "Pay per trigger"], "types": ["Synchronous invokes", "Asynchronous invokes"]},
    "azure virtual machines": {"desc": "On-demand, scalable computing resources offered by Microsoft Azure.", "characteristics": ["IaaS", "Supports Windows/Linux", "High availability"], "types": ["General Purpose", "Compute Optimized", "Memory Optimized"]},
    "git": {"desc": "A free and open source distributed version control system designed to handle everything from small to very large projects with speed and efficiency.", "characteristics": ["Distributed", "Branching", "History tracking"], "types": ["Local", "Remote"]},
    "ci/cd": {"desc": "Continuous Integration and Continuous Deployment.", "characteristics": ["Automation", "Faster delivery", "Code testing"], "types": ["Jenkins", "GitHub Actions", "GitLab CI"]},
    "jenkins": {"desc": "An open source automation server which enables developers around the world to reliably build, test, and deploy their software.", "characteristics": ["Extensible with plugins", "Pipeline as code", "Open-source"], "types": ["Freestyle Project", "Pipeline", "Multibranch Pipeline"]},
    "terraform": {"desc": "An open-source infrastructure as code software tool that provides a consistent CLI workflow to manage hundreds of cloud services.", "characteristics": ["Infrastructure as Code (IaC)", "Declarative", "Multi-cloud support"], "types": ["Providers", "Modules", "State files"]},
}

btech_stack.update(cloud_devops)

def format_entry(word, data):
    html = f"<strong>{word.upper()}</strong><br><br>"
    html += f"<span style='color: var(--text-main);'><strong>Definition:</strong></span> {data['desc']}<br><br>"
    
    html += f"<span style='color: var(--primary);'><strong>Key Characteristics:</strong></span>"
    html += "<ul>"
    for char in data['characteristics']:
        html += f"<li>{char}</li>"
    html += "</ul><br>"
    
    html += f"<span style='color: var(--accent);'><strong>Types / Examples:</strong></span>"
    html += "<ul>"
    for t in data['types']:
        html += f"<li>{t}</li>"
    html += "</ul>"
    
    return f"{word.lower()}|{html}\n"

count = 0
# Read existing lines to prevent duplicates
existing_words = set()
if os.path.exists('dataset.txt'):
    with open('dataset.txt', 'r', encoding='utf-8') as f:
        for line in f:
            if '|' in line:
                existing_words.add(line.split('|')[0].lower())

with open('dataset.txt', 'a', encoding='utf-8') as f:
    for word, data in btech_stack.items():
        if word.lower() not in existing_words:
            f.write(format_entry(word, data))
            count += 1

if os.path.exists('dist'):
    shutil.copy('dataset.txt', 'dist/dataset.txt')
    print("Copied to dist/dataset.txt")

print(f"Successfully added {count} new mega-detailed B.Tech tech entries!")
