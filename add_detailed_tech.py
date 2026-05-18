import os
import shutil

tech_data = {
    "docker": {
        "desc": "An open-source platform that automates the deployment, scaling, and management of applications using containerization.",
        "characteristics": ["Lightweight and isolated", "OS-level virtualization", "Highly portable across environments"],
        "types": ["Docker Engine", "Docker Compose", "Docker Swarm"]
    },
    "kubernetes": {
        "desc": "An open-source container orchestration system for automating software deployment, scaling, and management.",
        "characteristics": ["Self-healing capabilities", "Automated rollouts and rollbacks", "Horizontal scaling"],
        "types": ["Minikube", "EKS (Amazon)", "AKS (Azure)", "GKE (Google)"]
    },
    "aws": {
        "desc": "Amazon Web Services is a comprehensive, evolving cloud computing platform provided by Amazon.",
        "characteristics": ["Pay-as-you-go pricing", "Massive global infrastructure", "Highly scalable and secure"],
        "types": ["Compute (EC2)", "Storage (S3)", "Database (RDS)", "Networking (VPC)"]
    },
    "azure": {
        "desc": "Microsoft Azure is a cloud computing service operated by Microsoft for application management via Microsoft-managed data centers.",
        "characteristics": ["Seamless integration with Microsoft products", "Enterprise-grade security", "Hybrid cloud capabilities"],
        "types": ["Azure Virtual Machines", "Azure App Service", "Azure SQL Database", "Azure Functions"]
    },
    "devops": {
        "desc": "A set of practices that combines software development (Dev) and IT operations (Ops) to shorten the systems development life cycle.",
        "characteristics": ["Continuous Integration (CI)", "Continuous Delivery (CD)", "Infrastructure as Code (IaC)", "Monitoring and Logging"],
        "types": ["Version Control (Git)", "CI/CD Pipeline tools", "Configuration Management"]
    },
    "ci/cd": {
        "desc": "Continuous Integration and Continuous Deployment is a method to frequently deliver apps to customers by introducing automation into the stages of app development.",
        "characteristics": ["Automated testing", "Faster release cycles", "Reduced manual errors"],
        "types": ["Jenkins", "GitHub Actions", "GitLab CI", "CircleCI"]
    },
    "microservices": {
        "desc": "An architectural style that structures an application as a collection of loosely coupled, independently deployable services.",
        "characteristics": ["Highly maintainable and testable", "Independently deployable", "Organized around business capabilities"],
        "types": ["API Gateways", "Service Meshes", "Event-driven microservices"]
    },
    "machine learning": {
        "desc": "A branch of artificial intelligence (AI) and computer science which focuses on the use of data and algorithms to imitate the way that humans learn.",
        "characteristics": ["Pattern recognition", "Predictive modeling", "Improves through experience"],
        "types": ["Supervised Learning", "Unsupervised Learning", "Reinforcement Learning"]
    },
    "neural networks": {
        "desc": "A series of algorithms that endeavors to recognize underlying relationships in a set of data through a process that mimics the way the human brain operates.",
        "characteristics": ["Interconnected nodes (neurons)", "Weighted connections", "Activation functions"],
        "types": ["Convolutional Neural Networks (CNN)", "Recurrent Neural Networks (RNN)", "Feedforward Neural Networks"]
    },
    "load balancer": {
        "desc": "A device or software that acts as a reverse proxy and distributes network or application traffic across a number of servers.",
        "characteristics": ["Increases concurrent user capacity", "Ensures high availability", "Prevents single point of failure"],
        "types": ["Hardware Load Balancer", "Software Load Balancer (e.g., Nginx)", "DNS Load Balancing"]
    },
    "nginx": {
        "desc": "A web server that can also be used as a reverse proxy, load balancer, mail proxy and HTTP cache.",
        "characteristics": ["High performance and stability", "Low resource consumption", "Event-driven architecture"],
        "types": ["Reverse Proxy", "Load Balancer", "Static Content Server"]
    },
    "rest api": {
        "desc": "An application programming interface that conforms to the constraints of REST architectural style and allows for interaction with RESTful web services.",
        "characteristics": ["Stateless operations", "Client-server architecture", "Cacheability", "Uniform interface"],
        "types": ["GET (Retrieve)", "POST (Create)", "PUT (Update)", "DELETE (Remove)"]
    },
    "graphql": {
        "desc": "A query language for APIs and a runtime for fulfilling those queries with your existing data.",
        "characteristics": ["Asks for exactly what is needed", "Get many resources in a single request", "Strongly typed system"],
        "types": ["Queries (Fetch data)", "Mutations (Modify data)", "Subscriptions (Real-time updates)"]
    },
    "dynamic programming": {
        "desc": "An algorithmic technique for solving an optimization problem by breaking it down into simpler subproblems and utilizing the fact that the optimal solution to the overall problem depends upon the optimal solution to its subproblems.",
        "characteristics": ["Overlapping subproblems", "Optimal substructure", "Memoization or Tabulation"],
        "types": ["Top-down (Memoization)", "Bottom-up (Tabulation)"]
    },
    "graph algorithms": {
        "desc": "Algorithms designed to solve problems related to graph theory, which is the study of graphs and relationships between nodes.",
        "characteristics": ["Traverses nodes and edges", "Finds shortest paths", "Detects cycles"],
        "types": ["Breadth-First Search (BFS)", "Depth-First Search (DFS)", "Dijkstra's Algorithm", "A* Search"]
    },
    "git": {
        "desc": "A distributed version control system that tracks changes in any set of computer files.",
        "characteristics": ["Distributed architecture", "Branching and merging", "Cryptographic authentication of history"],
        "types": ["Local Repository", "Remote Repository", "Bare Repository"]
    },
    "react": {
        "desc": "A free and open-source front-end JavaScript library for building user interfaces based on UI components.",
        "characteristics": ["Virtual DOM", "Component-based architecture", "Unidirectional data flow"],
        "types": ["Functional Components", "Class Components", "React Hooks"]
    },
    "node.js": {
        "desc": "A cross-platform, open-source server environment that can run JavaScript on Windows, Linux, Unix, macOS, and more.",
        "characteristics": ["Asynchronous and Event Driven", "Single Threaded but Highly Scalable", "Very Fast (V8 Engine)"],
        "types": ["Web Servers", "RESTful APIs", "Real-time Web Applications"]
    },
    "nosql": {
        "desc": "A broad class of database management systems that differ from the classic model of the relational database management system (RDBMS) in some significant ways.",
        "characteristics": ["Schema-less data models", "High scalability", "Distributed architecture"],
        "types": ["Document Databases (MongoDB)", "Key-Value Stores (Redis)", "Wide-Column Stores (Cassandra)", "Graph Databases (Neo4j)"]
    },
    "sql": {
        "desc": "Structured Query Language is a domain-specific language used in programming and designed for managing data held in a relational database management system.",
        "characteristics": ["Schema-based", "ACID properties", "Table-based data structure"],
        "types": ["MySQL", "PostgreSQL", "Oracle Database", "Microsoft SQL Server"]
    }
}

# Let's also dynamically add AWS services individually so they show up
aws_services = {
    "aws ec2": "Amazon Elastic Compute Cloud provides scalable computing capacity in the Amazon Web Services cloud.",
    "aws s3": "Amazon Simple Storage Service is an object storage service that offers industry-leading scalability, data availability, security, and performance.",
    "aws rds": "Amazon Relational Database Service makes it easy to set up, operate, and scale a relational database in the cloud.",
    "aws lambda": "A serverless, event-driven compute service that lets you run code for virtually any type of application or backend service without provisioning or managing servers."
}

for svc, desc in aws_services.items():
    tech_data[svc] = {
        "desc": desc,
        "characteristics": ["Fully managed by AWS", "Highly scalable", "Pay-as-you-go pricing"],
        "types": ["Serverless", "Managed Compute", "Managed Storage"]
    }

# Same for some Azure services
azure_services = {
    "azure vm": "Azure Virtual Machines gives you the flexibility of virtualization for a wide range of computing solutions.",
    "azure functions": "A serverless solution that allows you to write less code, maintain less infrastructure, and save on costs."
}

for svc, desc in azure_services.items():
    tech_data[svc] = {
        "desc": desc,
        "characteristics": ["Fully managed by Microsoft Azure", "Enterprise security", "Scalable on demand"],
        "types": ["Serverless Compute", "IaaS (Infrastructure as a Service)"]
    }

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

with open('dataset.txt', 'a', encoding='utf-8') as f:
    for word, data in tech_data.items():
        f.write(format_entry(word, data))

# Copy to dist
if os.path.exists('dist'):
    shutil.copy('dataset.txt', 'dist/dataset.txt')
    print("Copied to dist/dataset.txt")

print(f"Successfully added {len(tech_data)} ultra-detailed tech entries!")
