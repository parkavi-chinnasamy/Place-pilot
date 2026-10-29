import sqlite3
import uuid

DB_PATH = 'placepilot.db'

# Format: (topic, difficulty, question_text, option_a, option_b, option_c, option_d, correct_option, explanation)
strings_questions = [
    # ==================== STRINGS - Easy (15) ====================
    ("Strings", "easy", "What is the time complexity to determine the length of a string of size N in C (using strlen)?", "O(1)", "O(log N)", "O(N)", "O(N^2)", "C", "In C, strings are null-terminated, so strlen must traverse each character until '\\0', taking O(N) time."),
    ("Strings", "easy", "Which of the following is true regarding Strings in Java?", "Strings are mutable", "Strings are immutable", "Strings cannot contain spaces", "Strings have fixed size of 256 bytes", "B", "In Java, String objects are immutable; any modification creates a new String instance in the string pool or heap."),
    ("Strings", "easy", "What is the time complexity to concatenate two strings of lengths M and N in Java/Python?", "O(1)", "O(log(M+N))", "O(M + N)", "O(M * N)", "C", "Because strings are immutable, creating a new concatenated string requires copying all M + N characters."),
    ("Strings", "easy", "Which method in Python checks if all characters in a string are alphanumeric?", "isalnum()", "isalpha()", "isnum()", "isvalid()", "A", "The isalnum() method returns True if all characters are letters or digits and the string is non-empty."),
    ("Strings", "easy", "How do you check if two strings s1 and s2 are identical in Python?", "s1 == s2", "s1.equals(s2)", "s1.compare(s2)", "s1 === s2", "A", "In Python, the equality operator == compares the values of two strings."),
    ("Strings", "easy", "What does the function trim() or strip() do on a string?", "Converts string to lowercase", "Removes leading and trailing whitespace", "Reverses the string", "Splits the string into words", "B", "strip() in Python and trim() in Java/JS remove whitespace from both beginning and end."),
    ("Strings", "easy", "What is an Anagram of a string?", "A substring starting at index 0", "A string with identical characters rearranged", "A string read backwards", "A string with only vowels", "B", "Two strings are anagrams if they contain the same characters with the same frequencies, in different orders."),
    ("Strings", "easy", "What is a Palindrome?", "A string with unique characters", "A string that reads the same forwards and backwards", "A string of odd length", "A string containing only digits", "B", "A palindrome reads identically in forward and reverse directions (e.g., 'radar')."),
    ("Strings", "easy", "What is the result of 'hello'[1:4] in Python string slicing?", "'hell'", "'ell'", "'ello'", "'hel'", "B", "Slice [1:4] takes indices 1, 2, and 3, which are characters 'e', 'l', 'l'."),
    ("Strings", "easy", "What is the time complexity of reversing a string of length N in-place in C++?", "O(1)", "O(log N)", "O(N)", "O(N^2)", "C", "Reversing a string involves swapping characters from both ends taking N/2 swaps, which is O(N) time."),
    ("Strings", "easy", "Which character represents the string termination character in C?", "'\\n'", "'\\0'", "'\\t'", "' '", "B", "C strings are terminated by the null character '\\0' with ASCII value 0."),
    ("Strings", "easy", "What data structure is recommended in Java for performing frequent string concatenations in a loop?", "String", "StringBuilder", "char[]", "Vector", "B", "StringBuilder provides mutable character sequences with amortized O(1) appends, avoiding repeated memory reallocations."),
    ("Strings", "easy", "What is the ASCII value of the uppercase letter 'A'?", "48", "65", "97", "128", "B", "In ASCII, 'A' is 65, 'a' is 97, and '0' is 48."),
    ("Strings", "easy", "What will 'racecar'.replace('a', 'o') return in Python?", "'rocecar'", "'rocecor'", "'racecar'", "'oacecao'", "B", "Python's replace('a', 'o') replaces all occurrences of 'a' with 'o', giving 'rocecor'."),
    ("Strings", "easy", "What is the time complexity to access a character at index i in a string of length N?", "O(1)", "O(log N)", "O(N)", "O(i)", "A", "Characters in standard strings/arrays are stored contiguously, allowing direct O(1) indexing."),

    # ==================== STRINGS - Medium (15) ====================
    ("Strings", "medium", "What is the optimal time complexity to find the length of the Longest Substring Without Repeating Characters?", "O(N^2)", "O(N log N)", "O(N)", "O(2^N)", "C", "Using a sliding window with a hash map / character index array achieves O(N) time."),
    ("Strings", "medium", "Which string matching algorithm preprocesses the pattern to avoid re-examining matched characters (LPS array)?", "Rabin-Karp", "Knuth-Morris-Pratt (KMP)", "Boyer-Moore", "Z-Algorithm", "B", "KMP builds the Longest Proper Prefix which is also Suffix (LPS) array to achieve O(N + M) pattern matching."),
    ("Strings", "medium", "What is the average time complexity of the Rabin-Karp algorithm for pattern matching?", "O(N * M)", "O(N + M)", "O(log(N * M))", "O(N^2)", "B", "Rabin-Karp uses rolling hash to achieve O(N + M) average time complexity, where N is text length and M is pattern length."),
    ("Strings", "medium", "What is the optimal time complexity to check if two strings of length N are anagrams of each other?", "O(N log N)", "O(N)", "O(N^2)", "O(1)", "B", "Counting character frequencies using a fixed-size frequency array of 26 (or 256) takes O(N) time and O(1) space."),
    ("Strings", "medium", "What is the time complexity of finding all anagram occurrences in a string of length N using a sliding window?", "O(N * M)", "O(N)", "O(N log N)", "O(M log M)", "B", "A fixed sliding window with frequency match counts processes each character in O(1) time, yielding O(N)."),
    ("Strings", "medium", "Which data structure is most suitable for prefix search, autocomplete, and dictionary lookups?", "Binary Heap", "Trie (Prefix Tree)", "Hash Table", "Red-Black Tree", "B", "A Trie stores common prefixes efficiently and allows lookups proportional to the query word length O(L)."),
    ("Strings", "medium", "What is the time complexity of searching a word of length L in a Trie containing N words?", "O(N)", "O(L)", "O(log N)", "O(L * log N)", "B", "Each step in a Trie descends one edge matching one character of the word, taking O(L) time regardless of N."),
    ("Strings", "medium", "What is the minimum number of edits (insert, delete, replace) required to convert 'kitten' to 'sitting'?", "2", "3", "4", "5", "B", "Levenshtein distance: kitten -> sitten (replace k with s) -> sittin (replace e with i) -> sitting (insert g) = 3 edits."),
    ("Strings", "medium", "What does the Z-algorithm compute for a string S of length N?", "Length of the longest palindromic substring", "Z-array where Z[i] is length of longest prefix match starting at i", "The minimum rotation of string S", "All unique anagrams of string S", "B", "The Z-algorithm computes in O(N) time an array Z where Z[i] is the length of the longest substring starting from S[i] that is also a prefix of S."),
    ("Strings", "medium", "What is the optimal time complexity to count the number of palindromic substrings in a string of length N using center expansion?", "O(N)", "O(N^2)", "O(N^3)", "O(N log N)", "B", "Expanding around all 2N - 1 possible centers takes O(N) per center, resulting in O(N^2) time with O(1) auxiliary space."),
    ("Strings", "medium", "What is the time complexity of the Manacher's Algorithm for finding the Longest Palindromic Substring?", "O(N^2)", "O(N log N)", "O(N)", "O(2^N)", "C", "Manacher's Algorithm finds the longest palindromic substring in linear O(N) time by reusing previously computed palindrome radii."),
    ("Strings", "medium", "Given a string encoded as '3[a2[c]]', what technique is best to decode it to 'accaccacc'?", "Greedy Search", "Two Stacks (one for counts, one for strings)", "Priority Queue", "Binary Search", "B", "Nested bracket decoding is solved naturally using stacks to preserve outer context while expanding inner brackets."),
    ("Strings", "medium", "What is the time complexity of generating all permutations of a string of length N with unique characters?", "O(N^2)", "O(N!)", "O(2^N)", "O(N^N)", "B", "There are N! distinct permutations, and generating each of length N takes O(N * N!) time."),
    ("Strings", "medium", "How do you detect if a string S can be rotated to form another string T of the same length?", "Sort both strings", "Check if T is a substring of S + S", "Compute XOR of all characters", "Reverse S and compare with T", "B", "Concatenating S with itself (S + S) contains all possible cyclic rotations of S. Checking if T is a substring takes linear time."),
    ("Strings", "medium", "What is the space complexity of a Suffix Automaton for a string of length N?", "O(N^2)", "O(N)", "O(N log N)", "O(2^N)", "B", "A Suffix Automaton has at most 2N - 1 states and 3N - 4 transitions, requiring strictly O(N) space.")
]

strings_hard_questions = [
    # ==================== STRINGS - Hard (15) ====================
    ("Strings", "hard", "What is the time complexity to construct a Suffix Array for a string of length N using the SA-IS (Suffix Array Induced Sorting) algorithm?", "O(N^2)", "O(N log N)", "O(N)", "O(N log^2 N)", "C", "The SA-IS algorithm constructs the suffix array of a string in strictly linear O(N) time."),
    ("Strings", "hard", "What is the optimal time complexity of the Aho-Corasick automaton for searching a set of keywords of total length M in a text of length N with K matches?", "O(N * M)", "O(N + M + K)", "O((N + M) log M)", "O(N * log M)", "B", "Aho-Corasick builds a trie with failure links in O(M) and searches text in O(N + K) time, giving O(N + M + K) total."),
    ("Strings", "hard", "What is the time complexity of Ukkonen's algorithm for online construction of a Suffix Tree?", "O(N^2)", "O(N log N)", "O(N)", "O(N^3)", "C", "Ukkonen's algorithm constructs the suffix tree of a string of length N in linear O(N) time with O(N) space."),
    ("Strings", "hard", "In Booth's algorithm, what is computed in O(N) time for a string of length N?", "Longest common subsequence", "Lexicographically smallest string rotation", "Number of distinct palindromes", "Shortest unique substring", "B", "Booth's algorithm uses a modified KMP failure function to find the lexicographically minimal rotation of a string in O(N) time."),
    ("Strings", "hard", "What is the Kasai algorithm used for in string processing?", "Computing LCP array from suffix array in O(N) time", "Constructing suffix tree in O(N) time", "Finding all occurrences of a regex", "Minimizing a deterministic finite automaton", "A", "Kasai's algorithm computes the Longest Common Prefix (LCP) array in linear O(N) time given the suffix array."),
    ("Strings", "hard", "How many distinct substrings can a string of length N with all distinct characters have?", "N", "N * (N + 1) / 2", "2^N", "N!", "B", "Every pair of start and end indices gives a unique substring, so the count is N * (N + 1) / 2."),
    ("Strings", "hard", "What is the optimal time complexity to solve the 'Shortest Common Supersequence' of two strings of lengths M and N?", "O(M + N)", "O(M * N)", "O(2^(M+N))", "O(M! * N!)", "B", "Shortest Common Supersequence is computed via Longest Common Subsequence (LCS) using DP in O(M * N) time."),
    ("Strings", "hard", "In regular expression matching supporting '.' and '*', what is the time complexity using 2D Dynamic Programming for text length T and pattern length P?", "O(T + P)", "O(T * P)", "O(2^(T+P))", "O(T! * P)", "B", "A 2D DP table of dimensions (T+1) x (P+1) fills each state in O(1) time, yielding O(T * P)."),
    ("Strings", "hard", "What is the Burrows-Wheeler Transform (BWT) primarily used for in computer science?", "Lossy audio compression", "Reversible text transformation for lossless data compression and fast FM-index search", "Cryptographic public-key exchange", "Grammar parsing in compilers", "B", "BWT permutes characters into runs of similar characters, widely used in bzip2 and bioinformatics (FM-index / bowtie)."),
    ("Strings", "hard", "What is the time complexity of the KMP algorithm preprocessing phase on a pattern of length M?", "O(M)", "O(M log M)", "O(M^2)", "O(1)", "A", "Building the prefix function (pi table / LPS) takes linear O(M) time."),
    ("Strings", "hard", "What is the time complexity to find the longest substring that appears at least K times in a string of length N using Suffix Array and LCP array?", "O(N^2)", "O(N log N)", "O(N)", "O(K * N)", "B", "Using Suffix Array and LCP with sliding window or binary search on answer takes O(N log N) or O(N) with SA-IS."),
    ("Strings", "hard", "In the 'Word Break II' problem (find all possible sentence combinations), what is the worst-case time complexity?", "O(N^2)", "O(N^3)", "O(2^N)", "O(N!)", "C", "A string like 'aaaaa' with dictionary {'a', 'aa'} has 2^(N-1) possible segmentations, giving exponential worst-case time O(2^N)."),
    ("Strings", "hard", "What is the time complexity to find the Longest Common Substring of two strings of lengths M and N using a Generalized Suffix Tree?", "O(M * N)", "O(M + N)", "O((M + N) log(M + N))", "O(M^2 + N^2)", "B", "Building a generalized suffix tree takes O(M + N) time, and finding the deepest internal node with leaves from both strings takes O(M + N) via DFS."),
    ("Strings", "hard", "What does the Lyndon factorization of a string represent?", "Decomposition into lexicographically non-increasing simple (Lyndon) words", "Decomposition into minimal palindromes", "Factorization into prime length substrings", "Decomposition into anagram clusters", "A", "Chen-Fox-Lyndon theorem states every string can be uniquely factored into a sequence of Lyndon words w1 w2 ... wk such that w1 >= w2 >= ... >= wk."),
    ("Strings", "hard", "Duval's algorithm computes the Lyndon factorization of a string of length N in what time and auxiliary space complexity?", "O(N log N) time, O(N) space", "O(N) time, O(1) space", "O(N^2) time, O(1) space", "O(N) time, O(N) space", "B", "Duval's algorithm finds the Lyndon factorization in strictly linear O(N) time using O(1) auxiliary space.")
]

conn = sqlite3.connect(DB_PATH)
c = conn.cursor()

inserted = 0
for topic, diff, qtext, oa, ob, oc, od, ans, exp in strings_questions + strings_hard_questions:
    c.execute("SELECT id FROM assessment_questions WHERE assessment_type='coding' AND question_text=?", (qtext,))
    if c.fetchone() is None:
        c.execute("""
            INSERT INTO assessment_questions (id, assessment_type, topic, difficulty, question_text, option_a, option_b, option_c, option_d, correct_option, explanation, is_active)
            VALUES (?, 'coding', ?, ?, ?, ?, ?, ?, ?, ?, ?, 1)
        """, (str(uuid.uuid4()), topic, diff, qtext, oa, ob, oc, od, ans, exp))
        inserted += 1

conn.commit()
conn.close()
print(f"Inserted {inserted} String questions for Coding.")
