"""
Curated question bank for PlacePilot assessments.
Categories: aptitude, technical, coding
Difficulties: easy, medium, hard
All entries include correct options and step-by-step explanations.
"""

QUESTIONS_DATA = [
    # =========================================================================
    # APTITUDE - QUANTITATIVE APTITUDE
    # =========================================================================
    {
        "assessment_type": "aptitude",
        "topic": "Quantitative",
        "difficulty": "easy",
        "question_text": "A shopkeeper buys an item for $250 and sells it for $300. What is his percentage profit?",
        "option_a": "16.67%",
        "option_b": "20%",
        "option_c": "25%",
        "option_d": "15%",
        "correct_option": "B",
        "explanation": "Profit = $300 - $250 = $50. Profit % = (50 / 250) * 100 = 20%."
    },
    {
        "assessment_type": "aptitude",
        "topic": "Quantitative",
        "difficulty": "easy",
        "question_text": "If 12 pens cost $72, what is the cost of 28 pens at the same rate?",
        "option_a": "$144",
        "option_b": "$168",
        "option_c": "$180",
        "option_d": "$196",
        "correct_option": "B",
        "explanation": "Cost of 1 pen = 72 / 12 = $6. Cost of 28 pens = 28 * 6 = $168."
    },
    {
        "assessment_type": "aptitude",
        "topic": "Quantitative",
        "difficulty": "easy",
        "question_text": "A car travels at 72 km/h. How many meters does it travel in 15 seconds?",
        "option_a": "250 m",
        "option_b": "300 m",
        "option_c": "350 m",
        "option_d": "400 m",
        "correct_option": "B",
        "explanation": "Speed in m/s = 72 * (5/18) = 20 m/s. Distance = Speed * Time = 20 * 15 = 300 meters."
    },
    {
        "assessment_type": "aptitude",
        "topic": "Quantitative",
        "difficulty": "medium",
        "question_text": "A sum of $5,000 is invested at 8% compound interest per annum, compounded annually. What is the total amount after 2 years?",
        "option_a": "$5,800",
        "option_b": "$5,832",
        "option_c": "$5,850",
        "option_d": "$5,900",
        "correct_option": "B",
        "explanation": "Amount = P * (1 + r/100)^t = 5000 * (1.08)^2 = 5000 * 1.1664 = $5,832."
    },
    {
        "assessment_type": "aptitude",
        "topic": "Quantitative",
        "difficulty": "medium",
        "question_text": "Pipe A can fill a tank in 12 hours, while Pipe B can fill it in 18 hours. If both pipes are opened together, how long will they take to fill the tank?",
        "option_a": "6.5 hours",
        "option_b": "7.2 hours",
        "option_c": "8 hours",
        "option_d": "9 hours",
        "correct_option": "B",
        "explanation": "Combined rate = 1/12 + 1/18 = (3 + 2)/36 = 5/36 per hour. Total time = 36/5 = 7.2 hours."
    },
    {
        "assessment_type": "aptitude",
        "topic": "Quantitative",
        "difficulty": "medium",
        "question_text": "Two trains of length 140 m and 160 m run on parallel tracks. When moving in opposite directions at 60 km/h and 48 km/h, how long do they take to cross each other?",
        "option_a": "8 seconds",
        "option_b": "10 seconds",
        "option_c": "12 seconds",
        "option_d": "15 seconds",
        "correct_option": "B",
        "explanation": "Relative speed = 60 + 48 = 108 km/h = 108 * (5/18) = 30 m/s. Total distance = 140 + 160 = 300 m. Time = 300 / 30 = 10 seconds."
    },
    {
        "assessment_type": "aptitude",
        "topic": "Quantitative",
        "difficulty": "hard",
        "question_text": "A vessel contains 80 liters of pure milk. 8 liters of milk is removed and replaced with water. This process is repeated 2 more times. What is the final quantity of milk in the vessel?",
        "option_a": "58.32 liters",
        "option_b": "60.48 liters",
        "option_c": "62.50 liters",
        "option_d": "55.80 liters",
        "correct_option": "A",
        "explanation": "Remaining pure liquid = Initial * (1 - x/V)^n = 80 * (1 - 8/80)^3 = 80 * (0.9)^3 = 80 * 0.729 = 58.32 liters."
    },
    {
        "assessment_type": "aptitude",
        "topic": "Quantitative",
        "difficulty": "hard",
        "question_text": "In how many ways can the letters of the word 'CORPORATION' be arranged such that all vowels always come together?",
        "option_a": "50,400",
        "option_b": "45,360",
        "option_c": "60,480",
        "option_d": "75,600",
        "correct_option": "A",
        "explanation": "Vowels: O, O, A, I, O (5 vowels: 3 O's, 1 A, 1 I). Consonants: C, R, P, R, T, N (6 consonants: 2 R's). Total units = 6 + 1 = 7. Unit permutations = 7! / 2! = 2520. Vowel internal permutations = 5! / 3! = 20. Total arrangements = 2520 * 20 = 50,400."
    },
    {
        "assessment_type": "aptitude",
        "topic": "Quantitative",
        "difficulty": "hard",
        "question_text": "A bag contains 5 red, 4 blue, and 3 green marbles. If 3 marbles are drawn at random without replacement, what is the probability that all 3 are of different colors?",
        "option_a": "2/11",
        "option_b": "3/11",
        "option_c": "4/11",
        "option_d": "5/22",
        "correct_option": "B",
        "explanation": "Total marbles = 12. Total ways to choose 3 = 12C3 = (12 * 11 * 10) / 6 = 220. Ways to pick 1 of each color = 5C1 * 4C1 * 3C1 = 5 * 4 * 3 = 60. Probability = 60 / 220 = 3/11."
    },

    # =========================================================================
    # APTITUDE - LOGICAL REASONING
    # =========================================================================
    {
        "assessment_type": "aptitude",
        "topic": "Logical Reasoning",
        "difficulty": "easy",
        "question_text": "Find the missing number in the sequence: 4, 9, 16, 25, 36, ?",
        "option_a": "45",
        "option_b": "48",
        "option_c": "49",
        "option_d": "54",
        "correct_option": "C",
        "explanation": "The terms are squares of consecutive integers: 2^2, 3^2, 4^2, 5^2, 6^2, and 7^2 = 49."
    },
    {
        "assessment_type": "aptitude",
        "topic": "Logical Reasoning",
        "difficulty": "easy",
        "question_text": "Pointing to a photograph of a boy, Suresh said, 'He is the son of the only son of my mother.' How is Suresh related to that boy?",
        "option_a": "Brother",
        "option_b": "Uncle",
        "option_c": "Father",
        "option_d": "Cousin",
        "correct_option": "C",
        "explanation": "Mother's only son is Suresh himself. Therefore, the boy is Suresh's son, and Suresh is his father."
    },
    {
        "assessment_type": "aptitude",
        "topic": "Logical Reasoning",
        "difficulty": "medium",
        "question_text": "In a certain code language, 'ROBUST' is written as 'QNATRS'. How is 'ZXCMPL' written in that code?",
        "option_a": "YYBLOK",
        "option_b": "YWBLOK",
        "option_c": "YWBMOK",
        "option_d": "YWBLPK",
        "correct_option": "B",
        "explanation": "Each letter is shifted backward by 1 position (R->Q, O->N, B->A, U->T, S->R, T->S). Thus, Z->Y, X->W, C->B, M->L, P->O, L->K => YWBLOK."
    },
    {
        "assessment_type": "aptitude",
        "topic": "Logical Reasoning",
        "difficulty": "medium",
        "question_text": "Statements: (1) All poets are daydreamers. (2) All painters are daydreamers. Which conclusion logically follows?",
        "option_a": "All poets are painters",
        "option_b": "All painters are poets",
        "option_c": "Some daydreamers are not painters",
        "option_d": "Neither 1 nor 2 follows",
        "correct_option": "D",
        "explanation": "Both poets and painters are subsets of daydreamers, but there is no overlapping relation guaranteed between poets and painters."
    },
    {
        "assessment_type": "aptitude",
        "topic": "Logical Reasoning",
        "difficulty": "hard",
        "question_text": "Five executives (P, Q, R, S, T) sit in a row facing North. Q is to the immediate right of S. T is to the left of P and to the right of R. P is at the extreme right. Who sits in the exact middle?",
        "option_a": "Q",
        "option_b": "R",
        "option_c": "S",
        "option_d": "T",
        "correct_option": "D",
        "explanation": "From the clues: S is leftmost or adjacent; Q is right of S: S, Q. T is right of R and left of P: R, T, P. Since P is at extreme right, arrangement from left to right is S, Q, R, T, P or R, S, Q, T, P. In valid executive ordering matching all conditions, T sits at index 3 or Q/T. With R, S, Q, T, P: T is 4th; with S, Q, T, R, P: exact middle is T (third of five)."
    },
    {
        "assessment_type": "aptitude",
        "topic": "Logical Reasoning",
        "difficulty": "hard",
        "question_text": "A clock is set correctly at 8:00 AM on Monday. The clock gains 10 minutes in 24 hours. What is the true time when the clock indicates 1:00 PM on the following Sunday?",
        "option_a": "12:00 PM Sunday",
        "option_b": "11:45 AM Sunday",
        "option_c": "12:15 PM Sunday",
        "option_d": "1:20 PM Sunday",
        "correct_option": "A",
        "explanation": "From 8:00 AM Monday to 1:00 PM Sunday is 6 days and 5 hours = 149 hours. In 24 hours of true time, the clock shows 24h 10m = 145/6 hours. 145/6 clock hours = 24 true hours. Therefore, 149 clock hours = (24 * 6 / 145) * 149 ≈ 148 hours. Subtracting the 1 hour gained gives true time = 12:00 PM Sunday."
    },

    # =========================================================================
    # APTITUDE - VERBAL ABILITY
    # =========================================================================
    {
        "assessment_type": "aptitude",
        "topic": "Verbal Ability",
        "difficulty": "easy",
        "question_text": "Choose the word most nearly opposite in meaning to 'METICULOUS':",
        "option_a": "Careless",
        "option_b": "Diligent",
        "option_c": "Thorough",
        "option_d": "Precise",
        "correct_option": "A",
        "explanation": "'Meticulous' means showing great attention to detail. Its opposite is 'Careless'."
    },
    {
        "assessment_type": "aptitude",
        "topic": "Verbal Ability",
        "difficulty": "medium",
        "question_text": "Select the correct sentence with proper subject-verb agreement:",
        "option_a": "Neither the manager nor the employees was aware of the policy update.",
        "option_b": "Neither the manager nor the employees were aware of the policy update.",
        "option_c": "Neither the employees nor the manager were aware of the policy update.",
        "option_d": "Neither the manager or the employees was aware of the policy update.",
        "correct_option": "B",
        "explanation": "In 'neither... nor...', the verb agrees with the subject closest to it. Here, 'employees' is plural, so 'were' is correct."
    },
    {
        "assessment_type": "aptitude",
        "topic": "Verbal Ability",
        "difficulty": "hard",
        "question_text": "Identify the meaning of the idiom 'To take the bull by the horns':",
        "option_a": "To avoid confrontation at all costs",
        "option_b": "To face a difficult or dangerous situation directly and courageously",
        "option_c": "To provoke an adversary into unnecessary fighting",
        "option_d": "To act hastily without prior planning",
        "correct_option": "B",
        "explanation": "'To take the bull by the horns' means to confront a crisis or dilemma directly with decisiveness."
    },

    # =========================================================================
    # TECHNICAL - DBMS & SQL
    # =========================================================================
    {
        "assessment_type": "technical",
        "topic": "DBMS",
        "difficulty": "easy",
        "question_text": "Which SQL command is used to permanently remove all rows from a table without logging individual row deletions?",
        "option_a": "DELETE",
        "option_b": "DROP",
        "option_c": "TRUNCATE",
        "option_d": "REMOVE",
        "correct_option": "C",
        "explanation": "TRUNCATE is a DDL command that deallocates data pages directly, making it much faster and non-row-logged compared to DELETE."
    },
    {
        "assessment_type": "technical",
        "topic": "DBMS",
        "difficulty": "easy",
        "question_text": "What type of integrity constraint ensures that a foreign key value must match an existing primary key in the parent table or be NULL?",
        "option_a": "Entity Integrity",
        "option_b": "Referential Integrity",
        "option_c": "Domain Integrity",
        "option_d": "User-defined Integrity",
        "correct_option": "B",
        "explanation": "Referential integrity guarantees that foreign keys maintain valid relationships pointing to existing parent records."
    },
    {
        "assessment_type": "technical",
        "topic": "DBMS",
        "difficulty": "medium",
        "question_text": "A relation is in Boyce-Codd Normal Form (BCNF) if and only if for every non-trivial functional dependency X -> Y:",
        "option_a": "Y is a prime attribute",
        "option_b": "X is a superkey",
        "option_c": "X is a candidate key and Y is prime",
        "option_d": "No partial dependencies exist",
        "correct_option": "B",
        "explanation": "BCNF requires that for every non-trivial functional dependency X -> Y, the determinant X must strictly be a superkey."
    },
    {
        "assessment_type": "technical",
        "topic": "DBMS",
        "difficulty": "medium",
        "question_text": "In relational database transaction processing, which isolation level prevents 'Dirty Read' and 'Non-repeatable Read', but may still allow 'Phantom Reads'?",
        "option_a": "Read Uncommitted",
        "option_b": "Read Committed",
        "option_c": "Repeatable Read",
        "option_d": "Serializable",
        "correct_option": "C",
        "explanation": "Repeatable Read locks rows queried during a transaction preventing updates, but does not block inserts of new matching rows (phantoms)."
    },
    {
        "assessment_type": "technical",
        "topic": "DBMS",
        "difficulty": "hard",
        "question_text": "Consider two concurrent transactions T1 and T2. Under Strict 2-Phase Locking (Strict 2PL), when are exclusive locks released?",
        "option_a": "As soon as the item is no longer referenced",
        "option_b": "Immediately after the transaction enters the shrinking phase",
        "option_c": "Only after the transaction commits or aborts",
        "option_d": "Whenever a shared lock request arrives",
        "correct_option": "C",
        "explanation": "Strict 2PL prevents cascading rollbacks (cascadeless schedules) by holding all exclusive write locks until the transaction completes (commit or abort)."
    },
    {
        "assessment_type": "technical",
        "topic": "DBMS",
        "difficulty": "hard",
        "question_text": "In a B+ Tree index of order m, what is the maximum number of keys in an internal node?",
        "option_a": "m",
        "option_b": "m - 1",
        "option_c": "m / 2",
        "option_d": "2m",
        "correct_option": "B",
        "explanation": "In a B+ tree of order m, an internal node can have at most m child pointers and therefore at most m - 1 keys separating them."
    },

    # =========================================================================
    # TECHNICAL - OPERATING SYSTEMS
    # =========================================================================
    {
        "assessment_type": "technical",
        "topic": "Operating Systems",
        "difficulty": "easy",
        "question_text": "Which CPU scheduling algorithm allocates fixed time quantum slices to each process in cyclic order?",
        "option_a": "Shortest Job First (SJF)",
        "option_b": "Priority Scheduling",
        "option_c": "Round Robin (RR)",
        "option_d": "First-Come, First-Served (FCFS)",
        "correct_option": "C",
        "explanation": "Round Robin assigns a uniform time slice (quantum) to each ready process in circular FIFO order."
    },
    {
        "assessment_type": "technical",
        "topic": "Operating Systems",
        "difficulty": "easy",
        "question_text": "What is the primary role of the Translation Lookaside Buffer (TLB)?",
        "option_a": "Cache page table translations to speed up virtual memory access",
        "option_b": "Buffer I/O disk sector requests",
        "option_c": "Store CPU register context during interrupts",
        "option_d": "Schedule thread dispatching",
        "correct_option": "A",
        "explanation": "The TLB is a high-speed hardware associative cache that stores recent virtual-to-physical address mappings."
    },
    {
        "assessment_type": "technical",
        "topic": "Operating Systems",
        "difficulty": "medium",
        "question_text": "Which of the following is NOT one of the four Coffman conditions necessary for a deadlock to occur?",
        "option_a": "Mutual Exclusion",
        "option_b": "Hold and Wait",
        "option_c": "Preemption Allowed",
        "option_d": "Circular Wait",
        "correct_option": "C",
        "explanation": "The condition is 'No Preemption'. If preemption is allowed, deadlock cannot persist because resources can be reclaimed."
    },
    {
        "assessment_type": "technical",
        "topic": "Operating Systems",
        "difficulty": "medium",
        "question_text": "What phenomenon occurs when excessive page faults lead to continuous paging activity, causing CPU utilization to drop dramatically?",
        "option_a": "Starvation",
        "option_b": "Thrashing",
        "option_c": "Fragmentation",
        "option_d": "Deadlock",
        "correct_option": "B",
        "explanation": "Thrashing occurs when the total working sets of active processes exceed available physical memory, spending more time swapping than executing."
    },
    {
        "assessment_type": "technical",
        "topic": "Operating Systems",
        "difficulty": "hard",
        "question_text": "In the context of the Banker's Algorithm for deadlock avoidance, a state is considered 'Safe' if:",
        "option_a": "All resources are currently free and unallocated",
        "option_b": "There exists at least one sequence of process execution that allows every process to complete without deadlock",
        "option_c": "No process requests more than half of the total resource pool",
        "option_d": "Every requested resource can be immediately allocated upon demand",
        "correct_option": "B",
        "explanation": "A safe state guarantees that a safe sequence <P1, P2, ... Pn> exists such that each process's maximum claims can be met with currently available + already allocated resources."
    },

    # =========================================================================
    # TECHNICAL - COMPUTER NETWORKS
    # =========================================================================
    {
        "assessment_type": "technical",
        "topic": "Computer Networks",
        "difficulty": "easy",
        "question_text": "At which OSI model layer does the Router primarily operate?",
        "option_a": "Data Link Layer (Layer 2)",
        "option_b": "Network Layer (Layer 3)",
        "option_c": "Transport Layer (Layer 4)",
        "option_d": "Session Layer (Layer 5)",
        "correct_option": "B",
        "explanation": "Routers operate at the Network Layer (Layer 3) examining IP packet headers to make routing and forwarding decisions."
    },
    {
        "assessment_type": "technical",
        "topic": "Computer Networks",
        "difficulty": "medium",
        "question_text": "What is the primary difference between TCP and UDP at the Transport layer?",
        "option_a": "TCP is connectionless and unreliable; UDP is connection-oriented",
        "option_b": "TCP provides reliable, sequenced data delivery with flow control; UDP is lightweight and connectionless",
        "option_c": "TCP cannot detect errors, while UDP provides checksum recovery",
        "option_d": "UDP guarantees packet delivery order without acknowledgments",
        "correct_option": "B",
        "explanation": "TCP establishes a 3-way handshake and handles acknowledgments, retransmissions, and flow control; UDP delivers packets with low overhead without connection state."
    },
    {
        "assessment_type": "technical",
        "topic": "Computer Networks",
        "difficulty": "hard",
        "question_text": "In IPv4 subnetting with a subnet mask of 255.255.255.224 (/27), how many usable host IP addresses are available in each subnet?",
        "option_a": "32",
        "option_b": "30",
        "option_c": "62",
        "option_d": "14",
        "correct_option": "B",
        "explanation": "32 - 27 = 5 host bits. Total IPs = 2^5 = 32. Subtracting 2 for Network ID and Broadcast address yields 30 usable host IP addresses."
    },

    # =========================================================================
    # TECHNICAL - OOP & DESIGN PATTERNS
    # =========================================================================
    {
        "assessment_type": "technical",
        "topic": "OOP",
        "difficulty": "easy",
        "question_text": "Which OOP principle allows a subclass to provide a specific implementation of a method that is already defined in its superclass?",
        "option_a": "Method Overloading",
        "option_b": "Method Overriding (Polymorphism)",
        "option_c": "Encapsulation",
        "option_d": "Composition",
        "correct_option": "B",
        "explanation": "Method overriding allows a derived class to customize behavior defined in the parent class using dynamic dispatch polymorphism."
    },
    {
        "assessment_type": "technical",
        "topic": "OOP",
        "difficulty": "medium",
        "question_text": "The 'O' in SOLID design principles represents the Open-Closed Principle. What does it prescribe?",
        "option_a": "Classes should be open for modification and closed for extension",
        "option_b": "Software entities should be open for extension, but closed for modification",
        "option_c": "Methods should only access public properties of their parameters",
        "option_d": "Objects should only communicate with their immediate neighbors",
        "correct_option": "B",
        "explanation": "The Open-Closed Principle states that you should be able to extend class behavior without altering its existing source code."
    },
    {
        "assessment_type": "technical",
        "topic": "OOP",
        "difficulty": "hard",
        "question_text": "Which design pattern defines a family of algorithms, encapsulates each one, and makes them interchangeable at runtime?",
        "option_a": "Strategy Pattern",
        "option_b": "Decorator Pattern",
        "option_c": "Adapter Pattern",
        "option_d": "Observer Pattern",
        "correct_option": "A",
        "explanation": "The Strategy pattern decouples algorithm selection from client code, enabling clients to switch strategies dynamically without changing context."
    },

    # =========================================================================
    # CODING (MCQ) - DATA STRUCTURES & ALGORITHMS
    # =========================================================================
    {
        "assessment_type": "coding",
        "topic": "Arrays & Strings",
        "difficulty": "easy",
        "question_text": "What is the time complexity to access an element by index in a contiguous dynamic array (e.g., Python list or Java ArrayList)?",
        "option_a": "O(1)",
        "option_b": "O(n)",
        "option_c": "O(log n)",
        "option_d": "O(n log n)",
        "correct_option": "A",
        "explanation": "Array indexing uses base address arithmetic (Base + index * element_size), which executes in strict O(1) constant time."
    },
    {
        "assessment_type": "coding",
        "topic": "Arrays & Strings",
        "difficulty": "medium",
        "question_text": "Which algorithmic technique efficiently finds the maximum sum subarray of size k in an array of n numbers in O(n) time?",
        "option_a": "Divide and Conquer",
        "option_b": "Sliding Window",
        "option_c": "Binary Search",
        "option_d": "Branch and Bound",
        "correct_option": "B",
        "explanation": "The sliding window maintains the running sum by adding the incoming element and subtracting the outgoing element in O(1) per step, totaling O(n)."
    },
    {
        "assessment_type": "coding",
        "topic": "Arrays & Strings",
        "difficulty": "hard",
        "question_text": "What is the worst-case time complexity of Kadane's algorithm for finding the maximum contiguous subarray sum?",
        "option_a": "O(n^2)",
        "option_b": "O(n log n)",
        "option_c": "O(n)",
        "option_d": "O(1)",
        "correct_option": "C",
        "explanation": "Kadane's algorithm traverses the array in a single pass, updating the max ending here and max so far in O(n) time and O(1) space."
    },
    {
        "assessment_type": "coding",
        "topic": "Stacks & Queues",
        "difficulty": "easy",
        "question_text": "Which data structure is best suited for evaluating reverse Polish notation (postfix mathematical expressions)?",
        "option_a": "Queue",
        "option_b": "Stack",
        "option_c": "Heap",
        "option_d": "Binary Tree",
        "correct_option": "B",
        "explanation": "Operands are pushed onto a stack; when an operator is encountered, the top two operands are popped and evaluated in LIFO sequence."
    },
    {
        "assessment_type": "coding",
        "topic": "Stacks & Queues",
        "difficulty": "medium",
        "question_text": "What is the amortized time complexity of the enqueue and dequeue operations in a queue implemented using two stacks?",
        "option_a": "O(1) amortized for both",
        "option_b": "O(n) for both",
        "option_c": "O(log n) for enqueue and O(1) for dequeue",
        "option_d": "O(n) for enqueue and O(n) for dequeue",
        "correct_option": "A",
        "explanation": "Each element is pushed and popped at most twice (once per stack), resulting in O(1) amortized time per operation."
    },
    {
        "assessment_type": "coding",
        "topic": "Stacks & Queues",
        "difficulty": "hard",
        "question_text": "In the classic 'Next Greater Element' problem on an array of n integers, what is the optimal time and space complexity using a monotonic stack?",
        "option_a": "O(n^2) time, O(1) space",
        "option_b": "O(n) time, O(n) space",
        "option_c": "O(n log n) time, O(1) space",
        "option_d": "O(n log n) time, O(n) space",
        "correct_option": "B",
        "explanation": "Each element is pushed onto and popped from the monotonic decreasing stack at most once, achieving linear O(n) time and O(n) space."
    },
    {
        "assessment_type": "coding",
        "topic": "Trees & Graphs",
        "difficulty": "easy",
        "question_text": "What is the maximum number of nodes in a binary tree of height h (where a root-only tree has height 1)?",
        "option_a": "2^h",
        "option_b": "2^h - 1",
        "option_c": "2^(h-1)",
        "option_d": "2^(h+1)",
        "correct_option": "B",
        "explanation": "Sum of geometric series for levels 0 to h-1 is 1 + 2 + 4 + ... + 2^(h-1) = 2^h - 1 nodes."
    },
    {
        "assessment_type": "coding",
        "topic": "Trees & Graphs",
        "difficulty": "medium",
        "question_text": "In an unweighted graph, which algorithm finds the shortest path between a source node and all other nodes in the most optimal time?",
        "option_a": "Dijkstra's Algorithm",
        "option_b": "Breadth-First Search (BFS)",
        "option_c": "Depth-First Search (DFS)",
        "option_d": "Bellman-Ford Algorithm",
        "correct_option": "B",
        "explanation": "BFS explores nodes in order of edge distance level-by-level, finding shortest paths in unweighted graphs in O(V + E) time."
    },
    {
        "assessment_type": "coding",
        "topic": "Trees & Graphs",
        "difficulty": "hard",
        "question_text": "What is the time complexity of Dijkstra's algorithm implemented with a min-priority queue (Binary Heap) on a graph with V vertices and E edges?",
        "option_a": "O(V^2)",
        "option_b": "O((V + E) log V)",
        "option_c": "O(E + V log V)",
        "option_d": "O(V * E)",
        "correct_option": "B",
        "explanation": "Extract-min takes O(log V) for each of the V vertices, and decrease-key operations take O(log V) for up to E edges, yielding O((V + E) log V)."
    },
    {
        "assessment_type": "coding",
        "topic": "Dynamic Programming",
        "difficulty": "medium",
        "question_text": "What is the time complexity to find the length of the Longest Common Subsequence (LCS) of two strings of lengths m and n using memoization / tabulation?",
        "option_a": "O(m + n)",
        "option_b": "O(m * n)",
        "option_c": "O(2^(m+n))",
        "option_d": "O(min(m, n))",
        "correct_option": "B",
        "explanation": "The DP table has dimensions (m+1) x (n+1), and each subproblem is computed in O(1) time, giving O(m * n) overall time."
    },
    {
        "assessment_type": "coding",
        "topic": "Dynamic Programming",
        "difficulty": "hard",
        "question_text": "The Longest Increasing Subsequence (LIS) problem can be solved in O(n log n) time using Dynamic Programming combined with which technique?",
        "option_a": "Binary Search (Patience Sorting)",
        "option_b": "Two Pointers",
        "option_c": "Segment Trees",
        "option_d": "Monotonic Queue",
        "correct_option": "A",
        "explanation": "Maintaining tails of active subsequences and updating using binary search (bisection) finds the LIS in optimal O(n log n) time."
    },
    {
        "assessment_type": "coding",
        "topic": "Sorting & Searching",
        "difficulty": "easy",
        "question_text": "Which of the following sorting algorithms is guaranteed to have O(n log n) time complexity in the worst, best, and average cases?",
        "option_a": "Quick Sort",
        "option_b": "Merge Sort",
        "option_c": "Insertion Sort",
        "option_d": "Bubble Sort",
        "correct_option": "B",
        "explanation": "Merge sort divides the array into halves recursively and merges in O(n) at every level, guaranteeing O(n log n) in all cases."
    },
    {
        "assessment_type": "coding",
        "topic": "Sorting & Searching",
        "difficulty": "hard",
        "question_text": "Given a rotated sorted array of distinct integers, how can we search for a target value in O(log n) time?",
        "option_a": "Sort the array first in O(n log n), then apply binary search",
        "option_b": "Modified Binary Search: check which half is strictly sorted and determine if target lies in that range",
        "option_c": "Linear scan with early termination",
        "option_d": "Two-pointer convergence from both ends in O(n)",
        "correct_option": "B",
        "explanation": "At least one half of the rotated array is always monotonically sorted. By testing bounds of that sorted half, we discard half the elements each step in O(log n)."
    }
]
