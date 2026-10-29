import sqlite3
import uuid

DB_PATH = 'placepilot.db'

# Questions to add for Coding
# Format: (topic, difficulty, question_text, option_a, option_b, option_c, option_d, correct_option, explanation)
coding_questions = [
    # ==================== ARRAYS (Need: 13 Easy, 12 Medium, 13 Hard) ====================
    # Easy (13)
    ("Arrays", "easy", "Which of the following operations on an array has O(1) time complexity?", "Inserting at the beginning", "Accessing an element by index", "Deleting from the middle", "Searching an unsorted array", "B", "Direct index access into a contiguous array requires only pointer arithmetic, taking O(1) time."),
    ("Arrays", "easy", "In a zero-indexed array of size N, what is the index of the last element?", "N", "N - 1", "N + 1", "0", "B", "Because indexing starts at 0, the elements run from 0 to N-1."),
    ("Arrays", "easy", "What is the space complexity of allocating an array of N integers?", "O(1)", "O(log N)", "O(N)", "O(N^2)", "C", "An array storing N elements requires memory proportional to N, hence O(N)."),
    ("Arrays", "easy", "What is the worst-case time complexity of inserting an element at index 0 of an array of size N?", "O(1)", "O(log N)", "O(N)", "O(N log N)", "C", "All N existing elements must be shifted right by one position, requiring O(N) operations."),
    ("Arrays", "easy", "How do you find the length of an array 'arr' in Python?", "arr.size()", "arr.length", "len(arr)", "length(arr)", "C", "The built-in len() function returns the number of items in a list/array."),
    ("Arrays", "easy", "What is the time complexity to find the minimum element in an unsorted array of size N?", "O(1)", "O(log N)", "O(N)", "O(N^2)", "C", "Every element must be checked at least once in an unsorted array, giving O(N) time."),
    ("Arrays", "easy", "What will be the result of accessing index 5 in an array of size 5?", "Null", "0", "IndexOutOfBounds error", "Last element", "C", "An array of size 5 has valid indices 0 through 4. Accessing 5 throws an index out of bounds error."),
    ("Arrays", "easy", "Which condition indicates that an array is completely sorted in non-decreasing order?", "arr[i] > arr[i+1] for all i", "arr[i] <= arr[i+1] for all valid i", "arr[0] <= arr[N-1]", "arr[i] == arr[i+1] for all i", "B", "Every element must be less than or equal to its succeeding element."),
    ("Arrays", "easy", "What is a 2D array typically stored as in computer memory?", "A linked list of arrays", "A single contiguous block in row-major or column-major order", "A binary search tree", "A hash set of elements", "B", "Modern systems store multidimensional arrays as contiguous linear memory blocks."),
    ("Arrays", "easy", "What is the result of reversing an array [1, 2, 3, 4] in-place?", "Space complexity is O(N)", "Space complexity is O(1)", "Time complexity is O(N^2)", "Time complexity is O(log N)", "B", "In-place reversal swaps elements from both ends using two pointers without extra space, achieving O(1) auxiliary space."),
    ("Arrays", "easy", "Which data structure has fixed size upon declaration in C/C++?", "std::vector", "Static Array", "std::list", "std::deque", "B", "Static arrays are allocated with a fixed size known at compile or creation time."),
    ("Arrays", "easy", "What is the prefix sum array P of arr = [2, 3, 5] where P[i] = sum(arr[0..i])?", "[2, 5, 10]", "[5, 8, 10]", "[2, 3, 5]", "[10, 8, 5]", "A", "P[0]=2, P[1]=2+3=5, P[2]=2+3+5=10."),
    ("Arrays", "easy", "What does checking 'if (arr.length == 0)' test for in an array?", "Null pointer", "Empty array", "Array contains only zeros", "Array is sorted", "B", "Length equal to zero means the array contains no elements."),

    # Medium (12)
    ("Arrays", "medium", "What is the optimal time complexity to find the majority element (appears > N/2 times) in an array?", "O(N^2)", "O(N log N)", "O(N)", "O(log N)", "C", "Boyer-Moore Voting Algorithm finds the majority element in O(N) time and O(1) space."),
    ("Arrays", "medium", "Given an array of positive integers, what is the best technique to find the smallest subarray with sum >= K?", "Dynamic Programming", "Sliding Window", "Binary Search Tree", "Breadth First Search", "B", "A variable-size sliding window (two pointers) can expand and shrink in O(N) total time."),
    ("Arrays", "medium", "What is the optimal time complexity to rotate an array of size N by K steps to the right using O(1) extra space?", "O(N * K)", "O(N)", "O(N log N)", "O(K)", "B", "Reversing the entire array, then the first K elements, then the remaining N-K elements takes O(N) time and O(1) space."),
    ("Arrays", "medium", "Which algorithm finds the duplicate number in an array of size N+1 containing integers between 1 and N in O(1) space?", "Kadane's Algorithm", "Floyd's Tortoise and Hare (Cycle Detection)", "Dijkstra's Algorithm", "Kruskal's Algorithm", "B", "Treating array values as next pointers creates a linked list with a cycle, solved by Floyd's cycle detection."),
    ("Arrays", "medium", "What is the time complexity of the Dutch National Flag algorithm used to sort an array of 0s, 1s, and 2s?", "O(N log N)", "O(N)", "O(N^2)", "O(1)", "B", "Dijkstra's Dutch National Flag algorithm partitions 0s, 1s, and 2s in a single pass with O(N) time and O(1) space."),
    ("Arrays", "medium", "In a sorted array with one element occurring once and all others twice, what is the optimal search complexity?", "O(N)", "O(log N)", "O(N log N)", "O(1)", "B", "Binary search on index parity finds the single non-duplicate element in O(log N) time."),
    ("Arrays", "medium", "What is the space complexity of the Next Greater Element problem using a Monotonic Stack?", "O(1)", "O(log N)", "O(N)", "O(N^2)", "C", "A monotonic stack stores at most N elements during execution, requiring O(N) auxiliary space."),
    ("Arrays", "medium", "Which data structure allows range sum queries in O(log N) time with point updates in O(log N)?", "Prefix Sum Array", "Fenwick Tree (Binary Indexed Tree)", "Hash Table", "Doubly Linked List", "B", "A Fenwick Tree (or Segment Tree) handles point updates and range prefix queries in O(log N)."),
    ("Arrays", "medium", "Given intervals [[1,3],[2,6],[8,10]], what is the first step in merging overlapping intervals?", "Sort intervals by start time", "Sort intervals by duration", "Build an interval tree", "Apply binary search", "A", "Sorting by start time ensures that overlapping intervals appear consecutively, allowing a single O(N) merge pass."),
    ("Arrays", "medium", "What is the optimal time complexity of the Product of Array Except Self problem without using the division operator?", "O(N^2)", "O(N log N)", "O(N)", "O(log N)", "C", "Using prefix and suffix product passes achieves O(N) time with O(1) extra space (excluding output array)."),
    ("Arrays", "medium", "What does Kadane's algorithm return if all numbers in an array are negative [-5, -2, -8, -1]?", "-16", "-1", "0", "-8", "B", "Kadane's algorithm properly initialized returns the maximum single element (-1) when all numbers are negative."),
    ("Arrays", "medium", "Given an array of size N, what is the maximum number of peaks (elements strictly greater than neighbors) possible?", "N", "floor(N/2)", "ceil(N/2)", "N - 1", "C", "Peaks cannot be adjacent, so the maximum count is ceil(N/2) (e.g. for N=5: indices 0, 2, 4)."),

    # Hard (13)
    ("Arrays", "hard", "What is the optimal time complexity to solve the 'Largest Rectangle in Histogram' problem?", "O(N^2)", "O(N log N)", "O(N)", "O(N^3)", "C", "A monotonic increasing stack finds the nearest smaller elements for each bar in O(N) time."),
    ("Arrays", "hard", "What is the time complexity to find the median of two sorted arrays of sizes M and N?", "O(M + N)", "O(log(min(M, N)))", "O((M + N) log(M + N))", "O(M * N)", "B", "Binary search on partition points of the smaller array finds the median in O(log(min(M, N))) time."),
    ("Arrays", "hard", "In the 'First Missing Positive' integer problem, what is the optimal time and auxiliary space complexity?", "O(N log N) time, O(1) space", "O(N) time, O(N) space", "O(N) time, O(1) space", "O(N^2) time, O(1) space", "C", "Using index-as-hash-key placing each positive integer x at index x-1 achieves O(N) time and O(1) auxiliary space."),
    ("Arrays", "hard", "What is the optimal time complexity of Mo's algorithm for offline range queries on an array of size N with Q queries?", "O(Q * N)", "O((N + Q) * sqrt(N))", "O(N * log N + Q)", "O(Q * log N)", "B", "By sorting queries into blocks of size sqrt(N), Mo's algorithm processes all queries in O((N + Q) * sqrt(N)) time."),
    ("Arrays", "hard", "What is the worst-case time complexity of finding the K-th smallest element in an unsorted array using Quickselect with median-of-medians pivot?", "O(N^2)", "O(N log N)", "O(N)", "O(log N)", "C", "Median-of-medians guarantees a balanced partition, achieving strictly worst-case O(N) time."),
    ("Arrays", "hard", "What is the time complexity to construct a Segment Tree over an array of size N?", "O(N)", "O(N log N)", "O(log N)", "O(N^2)", "A", "Building a Segment Tree recursively visits each of the 2N - 1 tree nodes once, taking O(N) time."),
    ("Arrays", "hard", "In the 'Sliding Window Maximum' problem of array size N and window size K, what is the optimal time complexity?", "O(N * K)", "O(N log K)", "O(N)", "O(K log N)", "C", "Using a monotonic double-ended queue (deque) processes each element at most twice (push and pop), giving O(N) total time."),
    ("Arrays", "hard", "What is the maximum number of inversions in an array of size N?", "N", "N * (N - 1) / 2", "N * log N", "2^N", "B", "A reverse sorted array has every pair out of order, yielding N*(N-1)/2 inversions."),
    ("Arrays", "hard", "What is the space complexity of a Sparse Table built for Range Minimum Query (RMQ) on an array of size N?", "O(N)", "O(N log N)", "O(N^2)", "O(log N)", "B", "A Sparse Table stores 2^j range answers for each index, requiring table dimensions N x (floor(log2 N) + 1), which is O(N log N)."),
    ("Arrays", "hard", "How can Range Minimum Query (RMQ) be answered in O(1) query time after O(N log N) preprocessing?", "Binary Indexed Tree", "Sparse Table", "Segment Tree", "AVL Tree", "B", "A Sparse Table computes min(ST[L][k], ST[R - 2^k + 1][k]) in O(1) time using overlapping intervals of length 2^k."),
    ("Arrays", "hard", "In Kadane's algorithm for 2D arrays (Maximum Sum Submatrix of size R x C), what is the optimal time complexity?", "O(R^2 * C^2)", "O(R^2 * C)", "O(R * C * log(R * C))", "O(R + C)", "B", "Fixing the top and bottom rows takes O(R^2), and running 1D Kadane across columns takes O(C), yielding O(R^2 * C)."),
    ("Arrays", "hard", "In an array of N integers, how many non-empty subarrays exist?", "N", "N * (N + 1) / 2", "2^N", "N^2", "B", "Choosing a start index i and end index j with i <= j yields N*(N+1)/2 possible contiguous subarrays."),
    ("Arrays", "hard", "What is the query time complexity for finding the sum of elements in a range [L, R] using a standard Segment Tree?", "O(1)", "O(log N)", "O(sqrt(N))", "O(N)", "B", "Range queries traverse at most 4 nodes per level in a balanced Segment Tree of height log N, taking O(log N) time.")
]

conn = sqlite3.connect(DB_PATH)
c = conn.cursor()

inserted = 0
for topic, diff, qtext, oa, ob, oc, od, ans, exp in coding_questions:
    # check existing
    c.execute("SELECT id FROM assessment_questions WHERE assessment_type='coding' AND question_text=?", (qtext,))
    if c.fetchone() is None:
        c.execute("""
            INSERT INTO assessment_questions (id, assessment_type, topic, difficulty, question_text, option_a, option_b, option_c, option_d, correct_option, explanation, is_active)
            VALUES (?, 'coding', ?, ?, ?, ?, ?, ?, ?, ?, ?, 1)
        """, (str(uuid.uuid4()), topic, diff, qtext, oa, ob, oc, od, ans, exp))
        inserted += 1

conn.commit()
conn.close()
print(f"Inserted {inserted} Array questions for Coding.")
