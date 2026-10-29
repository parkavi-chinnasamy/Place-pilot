"""
Additional high-yield questions for PlacePilot assessment bank.
"""

EXTRA_QUESTIONS = [
    # Hard Aptitude
    {
        "assessment_type": "aptitude",
        "topic": "Quantitative",
        "difficulty": "hard",
        "question_text": "A man can row 9 km/h in still water. It takes him twice as long to row up as to row down the river for the same distance. Find the speed of the stream.",
        "option_a": "2 km/h",
        "option_b": "3 km/h",
        "option_c": "4 km/h",
        "option_d": "4.5 km/h",
        "correct_option": "B",
        "explanation": "Let speed of stream = s. Downstream speed = 9 + s, upstream speed = 9 - s. Given: (9 + s) = 2 * (9 - s) => 9 + s = 18 - 2s => 3s = 9 => s = 3 km/h."
    },
    {
        "assessment_type": "aptitude",
        "topic": "Quantitative",
        "difficulty": "hard",
        "question_text": "A and B can complete a project together in 20 days. They work together for 15 days, and then B leaves. A finishes the remaining work alone in 10 days. In how many days can A finish the entire work alone?",
        "option_a": "35 days",
        "option_b": "40 days",
        "option_c": "45 days",
        "option_d": "50 days",
        "correct_option": "B",
        "explanation": "Work done in 15 days = 15/20 = 3/4. Remaining work = 1/4. A does 1/4 of work in 10 days => A can finish the whole work in 10 / (1/4) = 40 days."
    },
    {
        "assessment_type": "aptitude",
        "topic": "Logical Reasoning",
        "difficulty": "hard",
        "question_text": "In a family of seven (A, B, C, D, E, F, G), there are two married couples. B is the brother of D and father of G. C is the mother of D. E is the wife of B. A is the father of C. How is G related to C?",
        "option_a": "Daughter",
        "option_b": "Grandson or Granddaughter",
        "option_c": "Sister",
        "option_d": "Niece",
        "correct_option": "B",
        "explanation": "B is the son of C. G is the child of B. Therefore, G is the grandchild (grandson or granddaughter) of C."
    },
    {
        "assessment_type": "aptitude",
        "topic": "Verbal Ability",
        "difficulty": "hard",
        "question_text": "Choose the most appropriate word to complete the sentence: 'The CEO's _______ remarks during the press conference only served to exacerbate tensions with the union.'",
        "option_a": "conciliatory",
        "option_b": "inflammatory",
        "option_c": "placating",
        "option_d": "sycophantic",
        "correct_option": "B",
        "explanation": "'Inflammatory' means tending to arouse anger or hostility, which aligns with 'exacerbating tensions'."
    },

    # Hard Technical
    {
        "assessment_type": "technical",
        "topic": "DBMS",
        "difficulty": "hard",
        "question_text": "In write-ahead logging (WAL), when can a transaction T write a modified dirty page to disk?",
        "option_a": "Any time, without restriction",
        "option_b": "Only after the log record describing the update is flushed to non-volatile storage",
        "option_c": "Only after all transactions in the system commit",
        "option_d": "Only when the checkpoint background daemon triggers",
        "correct_option": "B",
        "explanation": "The fundamental invariant of WAL states that the log record detailing an update must reach persistent disk before the corresponding modified data page is written to disk."
    },
    {
        "assessment_type": "technical",
        "topic": "Operating Systems",
        "difficulty": "hard",
        "question_text": "Consider a system using Peterson's algorithm for mutual exclusion between two processes P0 and P1. Which shared variables are used?",
        "option_a": "A binary semaphore and a counting semaphore",
        "option_b": "An integer turn variable and a boolean flag array flag[2]",
        "option_c": "A mutex lock and a condition variable",
        "option_d": "A compare-and-swap hardware instruction register",
        "correct_option": "B",
        "explanation": "Peterson's algorithm relies on 'int turn' and 'bool flag[2]' to ensure mutual exclusion, progress, and bounded waiting in software."
    },
    {
        "assessment_type": "technical",
        "topic": "Computer Networks",
        "difficulty": "hard",
        "question_text": "In the TCP Congestion Control mechanism, what triggers TCP to drop its congestion window (cwnd) immediately down to 1 Maximum Segment Size (MSS) in TCP Tahoe?",
        "option_a": "Receipt of a duplicate ACK",
        "option_b": "A retransmission timeout (RTO)",
        "option_c": "Receipt of a selective ACK (SACK)",
        "option_d": "Completion of the 3-way handshake",
        "correct_option": "B",
        "explanation": "A timeout indicates severe network congestion, prompting TCP to reset cwnd to 1 MSS and re-enter slow start."
    },
    {
        "assessment_type": "technical",
        "topic": "OOP",
        "difficulty": "hard",
        "question_text": "Which design pattern is used to attach additional responsibilities to an object dynamically without modifying the original class hierarchy?",
        "option_a": "Decorator Pattern",
        "option_b": "Composite Pattern",
        "option_c": "Flyweight Pattern",
        "option_d": "Singleton Pattern",
        "correct_option": "A",
        "explanation": "The Decorator pattern wraps an object to dynamically extend its functionality at runtime as an alternative to subclassing."
    },

    # Hard Coding
    {
        "assessment_type": "coding",
        "topic": "Trees & Graphs",
        "difficulty": "hard",
        "question_text": "What is the time complexity to find strongly connected components (SCCs) in a directed graph using Tarjan's algorithm?",
        "option_a": "O(V * E)",
        "option_b": "O(V + E)",
        "option_c": "O(V^2)",
        "option_d": "O((V + E) log V)",
        "correct_option": "B",
        "explanation": "Tarjan's algorithm performs a single DFS traversal maintaining low-link values and a stack, visiting each vertex and edge once in O(V + E) linear time."
    },
    {
        "assessment_type": "coding",
        "topic": "Dynamic Programming",
        "difficulty": "hard",
        "question_text": "What is the recurrence relation for the Coin Change problem (minimum coins to make amount A given coins c1, c2, ... ck)?",
        "option_a": "dp[a] = sum(dp[a - c])",
        "option_b": "dp[a] = 1 + min(dp[a - c]) for all c <= a",
        "option_c": "dp[a] = max(dp[a - c])",
        "option_d": "dp[a] = dp[a - 1] + dp[a - 2]",
        "correct_option": "B",
        "explanation": "For any amount a, taking a valid coin c uses 1 coin plus the optimal subproblem cost dp[a - c]. We take the minimum across all coin choices."
    },
    {
        "assessment_type": "coding",
        "topic": "Arrays & Strings",
        "difficulty": "hard",
        "question_text": "In the 'Trapping Rain Water' problem with elevation map heights of size n, what is the optimal two-pointer solution complexity?",
        "option_a": "O(n) time and O(n) space",
        "option_b": "O(n) time and O(1) space",
        "option_c": "O(n log n) time and O(1) space",
        "option_d": "O(n^2) time and O(1) space",
        "correct_option": "B",
        "explanation": "Using left and right pointers moving towards the center while tracking left_max and right_max calculates trapped water in O(n) time and O(1) extra space."
    },
    {
        "assessment_type": "coding",
        "topic": "Trees & Graphs",
        "difficulty": "hard",
        "question_text": "Which algorithm is optimal for finding the Lowest Common Ancestor (LCA) in a tree for multiple queries (Q queries) in O((N + Q) log N) time?",
        "option_a": "Binary Lifting (Ancestry jumping by powers of 2)",
        "option_b": "Brute-force path tracing",
        "option_c": "Breadth-first search per query",
        "option_d": "Dijkstra's search",
        "correct_option": "A",
        "explanation": "Binary lifting precomputes 2^k ancestors in O(N log N) time and answers each LCA query in O(log N) time, totaling O((N + Q) log N)."
    }
]
