import sqlite3
import uuid

DB_PATH = 'placepilot.db'

# Format: (topic, difficulty, question_text, option_a, option_b, option_c, option_d, correct_option, explanation)
sorting_questions = [
    # ==================== SORTING & SEARCHING - Easy (13) ====================
    ("Sorting & Searching", "easy", "What is the best-case time complexity of Bubble Sort when optimized with a swapped flag?", "O(N^2)", "O(N log N)", "O(N)", "O(1)", "C", "If no swaps occur in the first pass through an already sorted array, the algorithm terminates in O(N) time."),
    ("Sorting & Searching", "easy", "What is the worst-case time complexity of Selection Sort on an array of size N?", "O(N)", "O(N log N)", "O(N^2)", "O(2^N)", "C", "Selection Sort always performs N*(N-1)/2 comparisons regardless of initial array order, giving O(N^2) time."),
    ("Sorting & Searching", "easy", "What is the prerequisite for performing Binary Search on an array?", "Array must contain only positive numbers", "Array must be sorted", "Array must have distinct elements", "Array size must be a power of 2", "B", "Binary Search relies on sorted order to eliminate half of the search space at each comparison step."),
    ("Sorting & Searching", "easy", "What is the time complexity of Linear Search in an unsorted array of size N?", "O(1)", "O(log N)", "O(N)", "O(N log N)", "C", "In the worst case, linear search must examine each of the N elements sequentially, taking O(N) time."),
    ("Sorting & Searching", "easy", "Which sorting algorithm is most efficient for small arrays or nearly sorted data?", "Merge Sort", "Insertion Sort", "Heap Sort", "Quick Sort", "B", "Insertion Sort runs in O(N) time on nearly sorted data and has very low constant factors for small inputs."),
    ("Sorting & Searching", "easy", "What is the average time complexity of Merge Sort on an array of size N?", "O(N)", "O(N log N)", "O(N^2)", "O(log N)", "B", "Merge Sort divides the array into halves (log N levels) and merges in O(N) per level, taking O(N log N) in all cases."),
    ("Sorting & Searching", "easy", "Is Merge Sort a stable sorting algorithm?", "Yes, by default if ties favor left element", "No, never", "Only if array has distinct elements", "Only for integers", "A", "Standard Merge Sort preserves the relative order of duplicate elements, making it stable."),
    ("Sorting & Searching", "easy", "What does 'in-place sorting algorithm' mean?", "It does not change the array", "It uses O(1) or O(log N) auxiliary memory", "It sorts in O(N) time", "It uses parallel threads", "B", "An in-place algorithm transforms the input using minimal additional memory beyond the input array."),
    ("Sorting & Searching", "easy", "In binary search on an array of size 1024, what is the maximum number of comparisons required?", "10", "11", "512", "1024", "B", "log2(1024) = 10, plus 1 possible boundary comparison = 11 maximum iterations."),
    ("Sorting & Searching", "easy", "Which of the following sorting algorithms is NOT a comparison-based sort?", "Quick Sort", "Radix Sort", "Heap Sort", "Bubble Sort", "B", "Radix Sort distributes keys into buckets based on digits/radix, bypassing the Omega(N log N) comparison lower bound."),
    ("Sorting & Searching", "easy", "How do you avoid integer overflow when computing the middle index in binary search?", "mid = (low + high) / 2", "mid = low + (high - low) / 2", "mid = (low * high) / 2", "mid = high - low", "B", "low + (high - low) / 2 prevents overflow that can occur when low + high exceeds the maximum 32-bit integer limit."),
    ("Sorting & Searching", "easy", "Which sorting algorithm builds the final sorted array one item at a time, similar to sorting playing cards in hand?", "Selection Sort", "Insertion Sort", "Quick Sort", "Bubble Sort", "B", "Insertion sort takes each element and inserts it into its proper position in the already-sorted prefix."),
    ("Sorting & Searching", "easy", "What is the space complexity of standard recursive Merge Sort?", "O(1)", "O(log N)", "O(N)", "O(N^2)", "C", "Merge Sort requires an auxiliary array of size N to merge two sorted subarrays."),

    # ==================== SORTING & SEARCHING - Medium (14) ====================
    ("Sorting & Searching", "medium", "What is the worst-case time complexity of QuickSort?", "O(N)", "O(N log N)", "O(N^2)", "O(N!)", "C", "QuickSort degrades to O(N^2) when poor pivots are chosen (e.g. smallest or largest element on already sorted data)."),
    ("Sorting & Searching", "medium", "What is the time complexity of Heap Sort on an array of size N in the worst case?", "O(N^2)", "O(N log N)", "O(N)", "O(N * sqrt(N))", "B", "Building the heap takes O(N), and extracting the root N times takes N * O(log N), giving O(N log N) in all cases."),
    ("Sorting & Searching", "medium", "What is the space complexity of Heap Sort?", "O(N)", "O(N log N)", "O(1)", "O(log N)", "C", "Heap Sort is an in-place comparison sort requiring only O(1) auxiliary space."),
    ("Sorting & Searching", "medium", "What is the lower bound for the worst-case time complexity of any comparison-based sorting algorithm?", "Omega(N)", "Omega(N log N)", "Omega(N^2)", "Omega(log N)", "B", "The decision tree for sorting N elements has N! leaves and minimum depth ceil(log2(N!)) = Omega(N log N)."),
    ("Sorting & Searching", "medium", "What is the time complexity of Counting Sort for N elements with keys in range [0, K]?", "O(N * K)", "O(N + K)", "O(N log K)", "O(K log N)", "B", "Counting Sort counts key frequencies in O(N) and reconstructs output using prefix sums in O(K), giving O(N + K)."),
    ("Sorting & Searching", "medium", "When is Counting Sort preferred over QuickSort or Merge Sort?", "When range K is much smaller than N", "When elements are floating point numbers", "When memory is strictly limited to O(1)", "When strings of variable length are sorted", "A", "When K = O(N), Counting Sort runs in linear O(N) time, beating comparison-based sorts."),
    ("Sorting & Searching", "medium", "What is the time complexity of finding an element in a row-wise and column-wise sorted 2D matrix of size M x N?", "O(M * N)", "O(M + N)", "O(log(M * N))", "O(M log N)", "B", "Starting from the top-right corner and moving left or down eliminates one row or column at each step in O(M + N) time."),
    ("Sorting & Searching", "medium", "Which pivot selection strategy ensures QuickSort avoids O(N^2) performance on already sorted arrays?", "Always choose first element", "Median-of-three or randomized pivot", "Always choose last element", "Always choose index 0", "B", "Randomized pivot selection or median-of-three (first, middle, last) prevents consistent worst-case partitions."),
    ("Sorting & Searching", "medium", "What is the time complexity of finding the peak element in an array where arr[i] != arr[i+1]?", "O(N)", "O(log N)", "O(N log N)", "O(1)", "B", "Binary search comparing arr[mid] with arr[mid+1] guarantees finding a local peak in O(log N) time."),
    ("Sorting & Searching", "medium", "What is the time complexity of Radix Sort for N integers with maximum d digits in base b?", "O(d * (N + b))", "O(N * log N)", "O(d * N * b)", "O(N^2)", "A", "Radix sort applies stable counting sort d times, each taking O(N + b) time."),
    ("Sorting & Searching", "medium", "In an infinite sorted array of positive integers, how can an element X be located in O(log P) time where P is the position of X?", "Exponential Search followed by Binary Search", "Linear Search", "Ternary Search", "Interpolation Search", "A", "Exponential search finds the search bound [2^k, 2^(k+1)] in O(log P) steps, followed by binary search in O(log P)."),
    ("Sorting & Searching", "medium", "What is the average-case time complexity of Interpolation Search on uniformly distributed sorted data?", "O(N)", "O(log N)", "O(log(log N))", "O(1)", "C", "Interpolation search estimates target position by linear interpolation, taking O(log log N) expected time on uniform data."),
    ("Sorting & Searching", "medium", "What is the hybrid sorting algorithm used in Python's list.sort() and Java's Arrays.sort() for objects?", "Introsort", "Timsort", "Smoothsort", "Tournament Sort", "B", "Timsort is a hybrid of Merge Sort and Insertion Sort designed to exploit existing runs in real-world data."),
    ("Sorting & Searching", "medium", "What is Introsort?", "A hybrid of QuickSort, HeapSort, and InsertionSort", "A parallelized version of MergeSort", "An external memory sorting algorithm", "A quantum sorting algorithm", "A", "Introsort begins with QuickSort, switches to HeapSort if recursion depth exceeds 2 * log N, and uses InsertionSort for small arrays.")
]

sorting_hard_questions = [
    # ==================== SORTING & SEARCHING - Hard (14) ====================
    ("Sorting & Searching", "hard", "What is the time complexity to find the K-th element of two sorted arrays of sizes M and N without merging them?", "O(M + N)", "O(log(min(M, N)))", "O(log(M) + log(N))", "O(1)", "B", "Binary searching on partitions of the smaller array finds the K-th element in O(log(min(M, N))) time."),
    ("Sorting & Searching", "hard", "What is the time complexity of External Merge Sort for sorting N elements using M memory blocks and B block size?", "O(N / B * log_(M/B)(N / B))", "O(N * log N)", "O(N^2 / M)", "O(M * B)", "A", "External sorting reads/writes blocks in passes, requiring O((N/B) * log_{M/B}(N/B)) I/O transfers."),
    ("Sorting & Searching", "hard", "What is the worst-case number of comparisons performed by Merge Sort on an array of size N?", "N * log2(N) - N + 1", "N * log2(N)", "N^2 / 2", "2^N", "A", "The exact upper bound on comparisons in 2-way Merge Sort is N * ceil(log2 N) - 2^(ceil(log2 N)) + 1 <= N log2 N - N + 1."),
    ("Sorting & Searching", "hard", "What is the time complexity to count inversions in an array of size N using a modified Merge Sort?", "O(N^2)", "O(N log N)", "O(N)", "O(log N)", "B", "During the merge step, when an element from the right subarray is smaller than one in the left subarray, all remaining left elements form inversions, computed in O(N log N)."),
    ("Sorting & Searching", "hard", "How many comparisons does the Ford-Johnson algorithm (Merge-Insertion Sort) optimize?", "Minimizes comparisons to near information-theoretic lower bound", "Maximizes cache locality", "Eliminates all branch mispredictions", "Allows in-place O(1) external sorting", "A", "The Ford-Johnson algorithm minimizes the total number of comparisons required to sort N items."),
    ("Sorting & Searching", "hard", "What is the optimal time complexity to find the minimum capacity to ship all packages within D days?", "O(N * D)", "O(N * log(Sum - Max))", "O(N^2)", "O(D * log N)", "B", "Binary search on answer space [max_weight, sum_weights] tests each midpoint capacity greedily in O(N) time."),
    ("Sorting & Searching", "hard", "In a rotated sorted array with DUPLICATE elements, what is the worst-case time complexity of searching for target X?", "O(1)", "O(log N)", "O(N)", "O(N log N)", "C", "When arr[low] == arr[mid] == arr[high], it is impossible to determine which half is sorted without incrementing low / decrementing high, degrading to O(N)."),
    ("Sorting & Searching", "hard", "What is the time complexity to find the K-th smallest pair distance among N numbers?", "O(N^2)", "O(N log N + N log(Max - Min))", "O(N^2 log N)", "O(K log N)", "B", "Sorting takes O(N log N), and binary search on distance range [0, Max - Min] with a two-pointer count takes O(N log(Max - Min))."),
    ("Sorting & Searching", "hard", "What is the time complexity of Median-of-Medians pivot selection algorithm on N elements?", "O(N^2)", "O(N log N)", "O(N)", "O(log N)", "C", "Dividing into groups of 5 and recursively finding the median of medians T(N) = T(N/5) + T(7N/10) + O(N) solves to O(N)."),
    ("Sorting & Searching", "hard", "What is the time complexity to find the K-th smallest element in an N x N multiplication table?", "O(N^2)", "O(N log(N^2))", "O(N * K)", "O(log(N))", "B", "Binary search on range [1, N^2] counts elements <= mid in each row in O(1) using min(N, mid//i), taking O(N log(N^2)) total time."),
    ("Sorting & Searching", "hard", "Which data structure can maintain a dynamic set of numbers and answer 'order statistic' queries (K-th smallest) in O(log N)?", "Order Statistic Tree (Augmented Balanced BST)", "Standard Hash Map", "Min-Heap", "Disjoint Set Union", "A", "Augmenting each node of a Red-Black tree with the size of its subtree allows finding the K-th element in O(log N) time."),
    ("Sorting & Searching", "hard", "What is the time complexity to search for a value in a sorted 2D matrix where each row and column is sorted, using Young Tableau properties?", "O(M * N)", "O(M + N)", "O(log(M + N))", "O(M log N)", "B", "A Young Tableau can be searched in O(M + N) time by stepping left or down from the upper right corner."),
    ("Sorting & Searching", "hard", "What is the worst-case time complexity of Quickselect when using random pivot selection?", "O(N)", "O(N log N)", "O(N^2)", "O(log N)", "C", "Although average time is O(N), randomized Quickselect can take O(N^2) in the worst case if every chosen pivot is an extreme element."),
    ("Sorting & Searching", "hard", "What is the time complexity of finding the K closest elements to target X in a sorted array of size N?", "O(N)", "O(log(N - K) + K)", "O(N log K)", "O(K * log N)", "B", "Binary searching for the optimal starting window index in range [0, N - K] takes O(log(N - K)), and returning the slice takes O(K).")
]

conn = sqlite3.connect(DB_PATH)
c = conn.cursor()

inserted = 0
for topic, diff, qtext, oa, ob, oc, od, ans, exp in sorting_questions + sorting_hard_questions:
    c.execute("SELECT id FROM assessment_questions WHERE assessment_type='coding' AND question_text=?", (qtext,))
    if c.fetchone() is None:
        c.execute("""
            INSERT INTO assessment_questions (id, assessment_type, topic, difficulty, question_text, option_a, option_b, option_c, option_d, correct_option, explanation, is_active)
            VALUES (?, 'coding', ?, ?, ?, ?, ?, ?, ?, ?, ?, 1)
        """, (str(uuid.uuid4()), topic, diff, qtext, oa, ob, oc, od, ans, exp))
        inserted += 1

conn.commit()
conn.close()
print(f"Inserted {inserted} Sorting & Searching questions for Coding.")
