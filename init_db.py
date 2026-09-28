"""
Seed script for the PSIT College of Higher Education, Kanpur — BCA 2nd Year
Interactive Quiz Portal.

Covers every core subject of CSJMU's BCA 2nd Year (Semester III & IV) syllabus,
with a Basic level quiz and an Advanced level quiz for each subject.
"""

from app import app, db, User, Quiz, Question
from werkzeug.security import generate_password_hash

# Each tuple: (question, option_a, option_b, option_c, option_d, correct_answer)
# correct_answer is one of "option_a" / "option_b" / "option_c" / "option_d"

def q(text, a, b, c, d, correct_letter):
    letter_map = {"a": "option_a", "b": "option_b", "c": "option_c", "d": "option_d"}
    return (text, a, b, c, d, letter_map[correct_letter])


SUBJECTS = [
    {
        "subject": "Python Programming",
        "basic": [
            q("Which keyword is used to define a function in Python?", "func", "define", "def", "function", "c"),
            q("Which symbol is used to start a single-line comment in Python?", "//", "#", "/*", "--", "b"),
            q("Which data type stores an ordered, mutable collection of items?", "Tuple", "List", "Set", "Frozenset", "b"),
            q("Which built-in function converts a string into an integer?", "str()", "int()", "float()", "chr()", "b"),
            q("Which operator is used for exponentiation in Python?", "^", "**", "%%", "exp()", "b"),
            q("Which keyword is used to create a class in Python?", "struct", "object", "class", "define", "c"),
            q("Which method adds an item to the end of a list?", "insert()", "append()", "add()", "push()", "b"),
            q("Which data type stores data as unordered key-value pairs?", "List", "Tuple", "Dictionary", "Set", "c"),
        ],
        "advanced": [
            q("What is the average time complexity of appending an item to a Python list?", "O(n)", "O(log n)", "O(1) amortized", "O(n^2)", "c"),
            q("Which built-in module provides support for regular expressions?", "regex", "re", "pyregex", "string", "b"),
            q("What does the 'self' parameter represent inside an instance method?", "The class itself", "The current instance of the class", "A static variable", "The parent class", "b"),
            q("Which construct is used to handle runtime errors gracefully in Python?", "if-else", "try-except", "for-in", "switch-case", "b"),
            q("A Python function that uses 'yield' instead of 'return' is called a:", "Decorator", "Generator", "Iterator class", "Lambda", "b"),
            q("Which built-in function returns pairs of index and value while looping over a list?", "zip()", "map()", "enumerate()", "range()", "c"),
            q("What is the primary purpose of the '__init__' method in a Python class?", "To destroy an object", "To initialize a new object's attributes", "To import modules", "To define static methods", "b"),
            q("Which third-party library is most widely used for numerical/array computing in Python?", "Pandas", "NumPy", "Flask", "Matplotlib", "b"),
        ],
    },
    {
        "subject": "Operating System",
        "basic": [
            q("An Operating System primarily acts as an interface between:", "Two users", "User and hardware", "Two networks", "Compiler and linker", "b"),
            q("Which of the following is an example of an Operating System?", "MySQL", "Linux", "HTML", "Python", "b"),
            q("A program in execution is called a:", "File", "Process", "Compiler", "Thread only", "b"),
            q("Which type of memory is volatile?", "ROM", "RAM", "Hard Disk", "SSD", "b"),
            q("CPU stands for:", "Central Process Utility", "Central Processing Unit", "Computer Personal Unit", "Central Processor Unit-let", "b"),
            q("Which scheduling algorithm uses a fixed time quantum for each process?", "FCFS", "Round Robin", "SJF", "Priority Scheduling", "b"),
            q("A deadlock occurs when processes:", "Finish execution early", "Wait indefinitely for resources held by each other", "Run in parallel successfully", "Share memory freely", "b"),
            q("Which OS component is responsible for organizing and managing files?", "Scheduler", "File System", "Loader", "Compiler", "b"),
        ],
        "advanced": [
            q("Which page replacement algorithm can suffer from Belady's Anomaly?", "LRU", "Optimal", "FIFO", "LFU", "c"),
            q("Which of these is NOT one of the four necessary conditions for deadlock?", "Mutual Exclusion", "Hold and Wait", "Preemption", "Circular Wait", "c"),
            q("Which scheduling algorithm can lead to starvation of long processes?", "Round Robin", "FCFS", "Shortest Job First", "None of these", "c"),
            q("Excessive paging that severely degrades CPU utilization is called:", "Fragmentation", "Thrashing", "Spooling", "Swapping fault", "b"),
            q("Which of these is a common synchronization primitive used to control access to shared resources?", "Semaphore", "Compiler", "Scheduler queue", "Interrupt vector", "a"),
            q("Which memory management technique divides physical memory into fixed-size blocks?", "Segmentation", "Paging", "Overlaying", "Caching", "b"),
            q("Which algorithm is used by an OS to avoid deadlock by carefully allocating resources?", "Round Robin", "Banker's Algorithm", "FIFO", "LRU", "b"),
            q("A 'critical section' in OS refers to:", "The OS kernel boot code", "A code segment that accesses shared resources and must not run concurrently", "The fastest CPU register", "A type of disk partition", "b"),
        ],
    },
    {
        "subject": "Introduction to Emerging Technologies",
        "basic": [
            q("AI stands for:", "Automated Interface", "Artificial Intelligence", "Applied Informatics", "Analytical Insight", "b"),
            q("IoT stands for:", "Internet of Technology", "Internet of Things", "Integration of Things", "Interface of Tools", "b"),
            q("Which of the following is a cloud computing service model?", "SaaS", "LAN", "USB", "BIOS", "a"),
            q("Blockchain technology is primarily known for maintaining a:", "Centralized database", "Distributed, tamper-resistant ledger", "Local file system", "Single point of control", "b"),
            q("Which technology enables systems to learn patterns from data without explicit programming?", "Machine Learning", "Compilation", "Virtualization", "Firmware update", "a"),
            q("AR stands for:", "Automated Reality", "Augmented Reality", "Applied Robotics", "Analog Recording", "b"),
            q("Which of the following is one of the classic '3 Vs' used to describe Big Data?", "Volume", "Version", "Vendor", "Virus", "a"),
            q("5G primarily refers to:", "The fifth version of Windows", "The fifth generation of mobile network technology", "A programming language", "A type of hard drive", "b"),
        ],
        "advanced": [
            q("Which consensus mechanism is originally used by Bitcoin to validate transactions?", "Proof of Stake", "Proof of Work", "Proof of Authority", "Proof of Capacity", "b"),
            q("Which cloud service model provides virtual machines/infrastructure without managing the OS for the customer?", "SaaS", "PaaS", "IaaS", "FaaS", "c"),
            q("Which technique is commonly used to reduce the number of features/dimensions in a dataset?", "Encryption", "Principal Component Analysis (PCA)", "Load balancing", "Tokenization", "b"),
            q("Edge computing primarily aims to:", "Centralize all data processing in the cloud", "Process data closer to its source to reduce latency", "Replace all local storage with tape drives", "Increase network hops for security", "b"),
            q("A 'Digital Twin' refers to:", "A backup hard disk", "A virtual replica of a physical system used for simulation/analysis", "A second user account", "A duplicate website domain", "b"),
            q("In blockchain, a 'smart contract' is best described as:", "A legal paper contract scanned into PDF", "Self-executing code that runs automatically when contract conditions are met", "A type of cryptocurrency wallet", "An encrypted email", "b"),
            q("Which of the following is a widely used deep learning framework?", "TensorFlow", "MySQL", "Apache HTTP", "WordPress", "a"),
            q("The term 'Industry 4.0' mainly refers to:", "The fourth industrial revolution driven by IoT, AI, and automation", "The 4th version of an operating system", "A car manufacturing brand", "The 4th generation of the internet", "a"),
        ],
    },
    {
        "subject": "Internet & Web Technology",
        "basic": [
            q("HTML stands for:", "HyperText Markup Language", "HighText Machine Language", "HyperTransfer Markup Language", "HyperText Modern Language", "a"),
            q("CSS is mainly used for:", "Structuring web page content", "Styling and layout of web pages", "Server-side database access", "Sending emails", "b"),
            q("Which protocol is commonly used for transferring web pages?", "FTP", "HTTP", "SMTP", "SNMP", "b"),
            q("Which HTML tag is used to create a hyperlink?", "<link>", "<a>", "<href>", "<h1>", "b"),
            q("Which language is primarily used to add client-side interactivity to a web page?", "JavaScript", "SQL", "C", "XML", "a"),
            q("URL stands for:", "Universal Resource Locator", "Uniform Resource Locator", "Unified Read Link", "Universal Reference Link", "b"),
            q("Which protocol is the secure version of HTTP?", "HTTPS", "FTP", "SSH", "SMTP", "a"),
            q("Which HTML tag defines the largest/most important heading?", "<h6>", "<head>", "<h1>", "<header>", "c"),
        ],
        "advanced": [
            q("Which HTTP method is idempotent and used to simply retrieve a resource?", "POST", "GET", "DELETE", "PUT", "b"),
            q("DOM stands for:", "Data Object Model", "Document Object Model", "Dynamic Output Module", "Document Order Map", "b"),
            q("Which CSS layout module arranges items along a main axis and a cross axis?", "Grid only", "Flexbox", "Float layout", "Table layout", "b"),
            q("AJAX is primarily used to:", "Style HTML with animations", "Exchange data with a server asynchronously without reloading the page", "Compile server-side code", "Encrypt cookies", "b"),
            q("Which HTTP status code indicates that a requested resource was not found?", "200", "301", "404", "500", "c"),
            q("A browser cookie is mainly used to:", "Speed up the CPU", "Store small pieces of data on the client to maintain state", "Compile JavaScript", "Render CSS faster", "b"),
            q("Which protocol is used to transfer files securely over SSH?", "HTTP", "SFTP", "SMTP", "DNS", "b"),
            q("REST stands for:", "Remote Execution State Transfer", "Representational State Transfer", "Reliable State Transmission", "Recursive State Template", "b"),
        ],
    },
    {
        "subject": "Software Engineering",
        "basic": [
            q("SDLC stands for:", "Software Design Life Cycle", "Software Development Life Cycle", "System Design Logic Chart", "Software Debug Life Cycle", "b"),
            q("Which model executes phases strictly one after another without overlap?", "Spiral Model", "Waterfall Model", "Agile Model", "V-Model with iteration", "b"),
            q("Which document specifies what a software system should do?", "Test Plan", "SRS (Software Requirements Specification)", "Source Code", "Change Log", "b"),
            q("Testing performed by a developer on an individual module is called:", "System Testing", "Unit Testing", "Acceptance Testing", "Regression Testing", "b"),
            q("UML is primarily used for:", "Compiling programs", "Modeling and visualizing software design", "Managing databases", "Network routing", "b"),
            q("Which model is iterative and incremental, emphasizing risk analysis in each cycle?", "Waterfall Model", "Spiral Model", "Big Bang Model", "V-Model", "b"),
            q("The phase of fixing bugs and updating software after release is called:", "Requirement Analysis", "Maintenance", "Design", "Feasibility Study", "b"),
            q("Which of these is a primary goal of software testing?", "Increase code size", "Find and fix defects before release", "Slow down the release cycle", "Remove documentation", "b"),
        ],
        "advanced": [
            q("Which metric measures a program's complexity based on the number of independent paths through its control flow?", "Cohesion Index", "Cyclomatic Complexity", "Fan-out Ratio", "Halstead Volume only", "b"),
            q("In Agile methodology, a 'Sprint' refers to:", "A final release candidate", "A fixed, time-boxed iteration in which a set of work is completed", "A type of bug", "A code review meeting only", "b"),
            q("Which UML diagram shows how objects interact with each other over time?", "Class Diagram", "Sequence Diagram", "Use Case Diagram", "Deployment Diagram", "b"),
            q("Regression testing is primarily performed to:", "Test the software for the very first time", "Ensure that new changes have not broken existing functionality", "Estimate project cost", "Design the user interface", "b"),
            q("Which design principle states that a class should have only one reason to change?", "Open/Closed Principle", "Single Responsibility Principle", "Liskov Substitution Principle", "Interface Segregation", "b"),
            q("CASE (as in CASE tools) stands for:", "Computer-Aided Software Engineering", "Central Application Software Engine", "Controlled Assembly of Software Elements", "Compiled Application Source Editor", "a"),
            q("Testing a system without any knowledge of its internal code structure is called:", "White-box Testing", "Black-box Testing", "Unit Testing only", "Static Analysis", "b"),
            q("'Technical debt' in software engineering refers to:", "Money owed to a software vendor", "The implied cost of future rework caused by choosing a quick, easy solution now", "A bug tracking tool", "A licensing fee", "b"),
        ],
    },
    {
        "subject": "Database Management System",
        "basic": [
            q("Which SQL command is used to retrieve data from a table?", "INSERT", "SELECT", "UPDATE", "DELETE", "b"),
            q("Which key uniquely identifies each row in a table?", "Foreign Key", "Primary Key", "Candidate Value", "Index Only", "b"),
            q("Which SQL command is used to add a new row to a table?", "INSERT", "ALTER", "DROP", "SELECT", "a"),
            q("Which normal form primarily deals with removing repeating groups?", "1NF", "2NF", "3NF", "BCNF", "a"),
            q("Which SQL command is used to modify existing rows in a table?", "UPDATE", "CREATE", "SELECT", "GRANT", "a"),
            q("DBMS stands for:", "Data Backup Management System", "Database Management System", "Digital Base Management Software", "Data Block Management Service", "b"),
            q("A key in one table that refers to the primary key of another table is called a:", "Primary Key", "Foreign Key", "Composite Key", "Super Key", "b"),
            q("Which SQL command permanently removes an entire table?", "DELETE", "DROP", "TRUNCATE ROW", "REMOVE", "b"),
        ],
        "advanced": [
            q("Which normal form removes transitive dependency on the primary key?", "1NF", "2NF", "3NF", "0NF", "c"),
            q("ACID properties of a transaction stand for:", "Access, Control, Isolation, Data", "Atomicity, Consistency, Isolation, Durability", "Availability, Concurrency, Integrity, Durability", "Atomicity, Concurrency, Index, Data", "b"),
            q("Which SQL clause is used to group rows that share a common value?", "ORDER BY", "GROUP BY", "HAVING only", "WHERE", "b"),
            q("A deadlock in DBMS occurs when:", "A single transaction commits successfully", "Two or more transactions wait indefinitely for locks held by each other", "A table has no primary key", "An index is rebuilt", "b"),
            q("Which type of JOIN returns all rows from both tables, matched or unmatched?", "INNER JOIN", "LEFT JOIN", "FULL OUTER JOIN", "CROSS JOIN", "c"),
            q("The main purpose of normalization is to:", "Increase data redundancy", "Reduce data redundancy and improve data integrity", "Slow down queries intentionally", "Remove all keys from a table", "b"),
            q("Which data structure is commonly used internally by database indexes for fast lookup?", "Linked List", "B-Tree", "Stack", "Queue", "b"),
            q("'Referential integrity' in a relational database ensures that:", "All tables have the same number of columns", "Foreign key values always match an existing primary key or are null", "Every column is indexed", "Queries execute in constant time", "b"),
        ],
    },
    {
        "subject": "Computer Networks",
        "basic": [
            q("Which protocol is commonly used for transferring web pages?", "FTP", "HTTP", "SMTP", "SNMP", "b"),
            q("IP stands for:", "Internal Process", "Internet Protocol", "Internet Program", "Input Protocol", "b"),
            q("Which device is primarily used to forward data packets between different networks?", "Switch", "Router", "Hub", "Repeater", "b"),
            q("DNS is mainly responsible for:", "Encrypting emails", "Translating domain names into IP addresses", "Compressing files", "Managing printers", "b"),
            q("How many layers does the OSI reference model have?", "5", "6", "7", "8", "c"),
            q("LAN stands for:", "Large Area Network", "Local Area Network", "Long Access Network", "Linked Area Node", "b"),
            q("Which network topology connects all devices to a single central hub or switch?", "Bus Topology", "Ring Topology", "Star Topology", "Mesh Topology", "c"),
            q("Which protocol is primarily used for sending email?", "SMTP", "HTTP", "FTP", "DNS", "a"),
        ],
        "advanced": [
            q("Which layer of the OSI model is primarily responsible for routing packets between networks?", "Data Link Layer", "Network Layer", "Session Layer", "Presentation Layer", "b"),
            q("Subnetting is primarily used to:", "Increase the speed of the CPU", "Divide a larger network into smaller, manageable sub-networks", "Encrypt all packet data", "Merge two different protocols", "b"),
            q("Which transport layer protocol provides reliable, connection-oriented communication?", "UDP", "TCP", "IP", "ICMP", "b"),
            q("CSMA/CD, used mainly in traditional Ethernet, stands for:", "Carrier Sense Multiple Access with Collision Detection", "Central System Multiple Access with Circuit Delivery", "Client Server Multiple Access Controller Device", "Channel Sensing Multiple Access with Collision Denial", "a"),
            q("Which addressing scheme uses 128-bit addresses?", "IPv4", "IPv6", "MAC addressing", "Subnet masking", "b"),
            q("NAT (Network Address Translation) is primarily used to:", "Translate private IP addresses to a public IP address", "Encrypt DNS queries", "Compress video streams", "Assign MAC addresses randomly", "a"),
            q("Which port number does HTTPS use by default?", "80", "21", "443", "25", "c"),
            q("A firewall's primary function is to:", "Speed up internet browsing", "Filter incoming and outgoing network traffic based on security rules", "Store website content permanently", "Assign IP addresses automatically", "b"),
        ],
    },
    {
        "subject": "Computer Graphics & Computer Vision",
        "basic": [
            q("The smallest addressable element of a digital image/display is called a:", "Byte", "Pixel", "Vector", "Node", "b"),
            q("RGB, a common color model, stands for:", "Red Green Blue", "Raster Graphic Byte", "Random Gradient Block", "Rendered Grid Buffer", "a"),
            q("Filling the interior of a closed 2D shape with color is generally called:", "Clipping", "Area/Flood filling", "Rasterization only", "Panning", "b"),
            q("Which classic algorithm is used to draw a straight line efficiently on a raster display?", "Bresenham's Algorithm", "Dijkstra's Algorithm", "Bubble Sort", "Newton-Raphson Method", "a"),
            q("2D transformations like translation, scaling and rotation are typically represented using a:", "Linked list", "Transformation matrix", "Hash table", "Binary tree", "b"),
            q("Converting a continuous image into a grid of discrete pixel values is called:", "Encryption", "Scan conversion / Digitization", "Compilation", "Masking", "b"),
            q("Which color model is typically used for printing rather than screen display?", "RGB", "HSV", "CMYK", "YUV", "c"),
            q("DPI stands for:", "Data Per Instruction", "Dots Per Inch", "Display Pixel Index", "Digital Print Interface", "b"),
        ],
        "advanced": [
            q("Which 2D transformation is used to change the size of an object?", "Translation", "Scaling", "Shearing only", "Reflection only", "b"),
            q("Anti-aliasing techniques are primarily used to reduce:", "File size", "Jagged/stair-step edges in rendered images", "Color depth", "Rendering time to zero", "b"),
            q("In computer vision, edge detection is primarily used to:", "Compress an image losslessly", "Identify boundaries and discontinuities within an image", "Increase image resolution", "Encrypt image data", "b"),
            q("Which algorithm is a widely used classical technique for edge detection?", "Canny Edge Detector", "Bresenham's Algorithm", "Dijkstra's Algorithm", "Quick Sort", "a"),
            q("Convolutional Neural Networks (CNNs) are especially effective in computer vision because they:", "Store images as plain text", "Automatically learn and extract spatial features from images", "Only work on 1D audio data", "Require no training data", "b"),
            q("'Clipping' in computer graphics refers to:", "Increasing image brightness", "Removing portions of an image/scene that lie outside a defined viewing window", "Compressing a video file", "Adding a watermark", "b"),
            q("Which representation is commonly used for 3D rotations to avoid the gimbal lock problem?", "Euler angles only", "Quaternions", "Bitmaps", "Hash values", "b"),
            q("Image segmentation is primarily used to:", "Encrypt an image", "Partition an image into meaningful regions or objects", "Convert an image to grayscale only", "Reduce file size to zero", "b"),
        ],
    },
    {
        "subject": "Numerical & Statistical Techniques",
        "basic": [
            q("The 'mean' of a data set is also commonly known as the:", "Median", "Average", "Mode", "Range", "b"),
            q("Which measure represents the middle value of an ordered data set?", "Mean", "Median", "Mode", "Variance", "b"),
            q("Standard deviation is a measure of a data set's:", "Central tendency", "Dispersion / spread", "Symmetry only", "Sample size", "b"),
            q("Which iterative numerical method is commonly used to find the roots of an equation?", "Gauss Elimination", "Newton-Raphson Method", "Simpson's Rule", "Trapezoidal Rule", "b"),
            q("Interpolation is a technique primarily used to:", "Delete outliers from data", "Estimate unknown values that fall between known data points", "Encrypt statistical data", "Sort a data set", "b"),
            q("The 'mode' of a data set refers to:", "The average value", "The middle value", "The most frequently occurring value", "The total sum of values", "c"),
            q("Which numerical method solves a system of linear equations using systematic elimination?", "Newton-Raphson Method", "Gauss Elimination Method", "Simpson's Rule", "Bisection Method", "b"),
            q("Correlation is a statistical measure of the:", "Absolute size of a data set", "Strength and direction of the relationship between two variables", "Number of outliers", "Standard deviation squared", "b"),
        ],
        "advanced": [
            q("Which numerical method for solving ODEs generally gives better accuracy than Euler's method by using weighted slopes?", "Runge-Kutta Method", "Bisection Method", "Regula-Falsi Method", "Gauss-Jordan Method", "a"),
            q("The Trapezoidal Rule is primarily used for:", "Solving differential equations", "Numerical integration (approximating the area under a curve)", "Finding matrix inverses", "Hypothesis testing", "b"),
            q("Regression analysis is primarily used to estimate the:", "Mode of a data set", "Relationship between a dependent variable and one or more independent variables", "Standard deviation only", "Number of samples needed", "b"),
            q("An error that arises from approximating numbers during computation (e.g., due to limited decimal places) is called:", "Truncation error", "Round-off error", "Syntax error", "Sampling error", "b"),
            q("Applying the Newton-Raphson method to find a root requires knowledge of the function's:", "Integral", "Derivative", "Mean", "Standard deviation", "b"),
            q("Which statistical test is commonly used to compare the means of two small samples?", "Chi-square test", "t-test", "F-test only", "Z-test always", "b"),
            q("Simpson's Rule for numerical integration requires the number of sub-intervals to be:", "Odd", "Even", "Prime", "A multiple of 5", "b"),
            q("The least squares method used in regression aims to:", "Maximize the sum of residuals", "Minimize the sum of squared errors between observed and predicted values", "Maximize the standard deviation", "Randomize the data points", "b"),
        ],
    },
    {
        "subject": "Soft Computing",
        "basic": [
            q("Soft computing primarily deals with problems involving:", "Absolute precision only", "Uncertainty, imprecision, and approximation", "Only integer arithmetic", "Fixed deterministic rules only", "b"),
            q("Which technique is inspired by the structure and function of biological neural networks?", "Genetic Algorithm", "Artificial Neural Network (ANN)", "Fuzzy Logic", "Simulated Annealing", "b"),
            q("Fuzzy logic primarily deals with:", "Strictly binary true/false values", "Degrees of truth between completely true and completely false", "Only whole numbers", "Random number generation only", "b"),
            q("Which optimization technique is inspired by the process of natural selection?", "Fuzzy Logic", "Genetic Algorithm", "Neural Network training", "Gradient Descent only", "b"),
            q("ANN stands for:", "Automated Network Node", "Artificial Neural Network", "Analog Numeric Notation", "Applied Network Node", "b"),
            q("Which of the following is a commonly used activation function in neural networks?", "Sigmoid", "Median", "Determinant", "Checksum", "a"),
            q("In fuzzy logic, membership values typically range between:", "-1 and 1", "0 and 1", "0 and 100", "1 and 10", "b"),
            q("Which soft computing technique is inspired by the collective/swarm behavior of birds or insects?", "Genetic Algorithm", "Particle Swarm Optimization", "Fuzzy Inference", "Backpropagation", "b"),
        ],
        "advanced": [
            q("In a neural network, the layer(s) between the input and output layers are called:", "Output layers", "Hidden layers", "Bias layers", "Root layers", "b"),
            q("The backpropagation algorithm is primarily used to:", "Initialize random weights", "Adjust network weights by propagating the error backward from output to input", "Compress the training dataset", "Encrypt neural network outputs", "b"),
            q("In a Genetic Algorithm, the operation that combines two parent solutions to create offspring is called:", "Mutation", "Crossover", "Selection pressure", "Fitness evaluation", "b"),
            q("The fuzzy logic component that converts a crisp (exact) input into a fuzzy set is called:", "Defuzzification", "Fuzzification", "Rule base compilation", "Aggregation", "b"),
            q("'Overfitting' in a trained model refers to a situation where the model:", "Performs poorly on both training and unseen data", "Performs very well on training data but poorly on unseen/test data", "Trains in zero time", "Has no parameters at all", "b"),
            q("Which optimization technique is most commonly used to minimize the loss function of a neural network?", "Gradient Descent", "Bubble Sort", "Binary Search", "Depth-First Search", "a"),
            q("Mutation in a Genetic Algorithm is primarily used to:", "Guarantee immediate convergence", "Maintain diversity in the population and help avoid local optima", "Remove the fitness function", "Stop the algorithm early", "b"),
            q("Which neural network architecture is best suited for sequential or time-series data?", "Convolutional Neural Network (CNN)", "Recurrent Neural Network (RNN)", "Perceptron only", "Decision Tree", "b"),
        ],
    },
]

TIMER_BASIC = 8
TIMER_ADVANCED = 10

with app.app_context():
    db.create_all()

    # Rebuild only this application's own quiz seed data.
    Question.query.delete()
    Quiz.query.delete()
    User.query.filter_by(username="bca_teacher").delete()
    db.session.commit()

    teacher = User(
        username="bca_teacher",
        password=generate_password_hash("bca123"),
        user_type="teacher"
    )
    db.session.add(teacher)
    db.session.commit()

    quiz_count = 0
    question_count = 0

    for entry in SUBJECTS:
        subject = entry["subject"]
        for level, timer in (("Basic", TIMER_BASIC), ("Advanced", TIMER_ADVANCED)):
            questions = entry["basic"] if level == "Basic" else entry["advanced"]
            quiz = Quiz(
                title=f"{subject} - {level}",
                teacher_id=teacher.id,
                timer=timer,
                subject=subject,
                level=level,
            )
            db.session.add(quiz)
            db.session.flush()
            quiz_count += 1

            for text, a, b, c, d, correct in questions:
                db.session.add(Question(
                    quiz_id=quiz.id,
                    question_text=text,
                    option_a=a,
                    option_b=b,
                    option_c=c,
                    option_d=d,
                    correct_answer=correct,
                ))
                question_count += 1

    db.session.commit()

print("PSIT BCA 2nd Year quiz database initialized successfully.")
print(f"Subjects: {len(SUBJECTS)} | Quizzes: {quiz_count} | Questions: {question_count}")
print("Teacher username: bca_teacher")
print("Teacher password: bca123")
