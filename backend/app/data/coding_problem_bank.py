"""
Initial Coding Problem Bank for PlacePilot
Contains curated DSA problems across Easy, Medium, and Hard difficulty with
clean starter templates in Python, C++, and Java, constraints, examples,
and both public sample test cases and hidden judging test cases.
(Note: Solutions are intentionally NOT included in starter codes so the student
writes the algorithm themselves).
"""

INITIAL_PROBLEMS = [
    {
        "title": "Two Sum",
        "slug": "two-sum",
        "difficulty": "easy",
        "topic": "Arrays & Hashing",
        "description": "Given an array of integers `nums` and an integer `target`, return the indices of the two numbers such that they add up to `target`.\n\nYou may assume that each input would have exactly one solution, and you may not use the same element twice. You can return the answer with the indices in non-decreasing order.",
        "constraints": "- 2 <= nums.length <= 10^4\n- -10^9 <= nums[i] <= 10^9\n- -10^9 <= target <= 10^9\n- Only one valid answer exists.",
        "input_format": "The first line contains an integer N (the size of the array) and an integer target, separated by space.\nThe second line contains N space-separated integers representing the array.",
        "output_format": "Print the two 0-based indices separated by a space.",
        "sample_input": "4 9\n2 7 11 15",
        "sample_output": "0 1",
        "hints": [
            "A brute force approach checks every pair, taking O(N^2) time.",
            "Can you use a Hash Map to find the complement (target - nums[i]) in O(1) time?"
        ],
        "starter_code": {
            "python": """import sys

def two_sum(nums, target):
    # TODO: Write your code here
    # Return a list of two indices [i, j] such that nums[i] + nums[j] == target
    return []

if __name__ == '__main__':
    lines = sys.stdin.read().strip().split()
    if lines:
        n = int(lines[0])
        target = int(lines[1])
        nums = [int(x) for x in lines[2:2+n]]
        res = two_sum(nums, target)
        if res and len(res) == 2:
            print(f"{res[0]} {res[1]}")
""",
            "cpp": """#include <iostream>
#include <vector>
using namespace std;

vector<int> twoSum(const vector<int>& nums, int target) {
    // TODO: Write your code here
    // Return a vector of two indices {i, j} such that nums[i] + nums[j] == target
    return {};
}

int main() {
    int n, target;
    if (cin >> n >> target) {
        vector<int> nums(n);
        for (int i = 0; i < n; i++) cin >> nums[i];
        vector<int> res = twoSum(nums, target);
        if (res.size() == 2) {
            cout << res[0] << " " << res[1] << endl;
        }
    }
    return 0;
}
""",
            "java": """import java.util.*;

public class Main {
    public static int[] twoSum(int[] nums, int target) {
        // TODO: Write your code here
        // Return an array of two indices [i, j] such that nums[i] + nums[j] == target
        return new int[]{};
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        if (sc.hasNextInt()) {
            int n = sc.nextInt();
            int target = sc.nextInt();
            int[] nums = new int[n];
            for (int i = 0; i < n; i++) {
                nums[i] = sc.nextInt();
            }
            int[] res = twoSum(nums, target);
            if (res != null && res.length == 2) {
                System.out.println(res[0] + " " + res[1]);
            }
        }
    }
}
"""
        },
        "test_cases": [
            {"input": "4 9\n2 7 11 15", "expected_output": "0 1", "is_hidden": False, "explanation": "nums[0] + nums[1] = 2 + 7 = 9"},
            {"input": "3 6\n3 2 4", "expected_output": "1 2", "is_hidden": False, "explanation": "nums[1] + nums[2] = 2 + 4 = 6"},
            {"input": "2 6\n3 3", "expected_output": "0 1", "is_hidden": True, "explanation": "Duplicate values allowed"},
            {"input": "5 10\n1 5 3 7 9", "expected_output": "2 3", "is_hidden": True, "explanation": "3 + 7 = 10, indices 2 and 3"},
            {"input": "6 0\n-3 4 3 90 2 -1", "expected_output": "0 2", "is_hidden": True, "explanation": "Negative numbers: -3 + 3 = 0"}
        ]
    },
    {
        "title": "Valid Parentheses",
        "slug": "valid-parentheses",
        "difficulty": "easy",
        "topic": "Stacks",
        "description": "Given a string `s` containing just the characters `'('`, `')'`, `'{'`, `'}'`, `'['` and `']'`, determine if the input string is valid.\n\nAn input string is valid if:\n1. Open brackets must be closed by the same type of brackets.\n2. Open brackets must be closed in the correct order.\n3. Every close bracket has a corresponding open bracket of the same type.",
        "constraints": "- 1 <= s.length <= 10^4\n- `s` consists of parentheses only `'()[]{}'`.",
        "input_format": "A single line containing the string `s`.",
        "output_format": "Print `true` if valid, otherwise `false`.",
        "sample_input": "()[]{}",
        "sample_output": "true",
        "hints": [
            "Use a Last-In-First-Out (LIFO) stack to match the most recent opening bracket with incoming closing brackets."
        ],
        "starter_code": {
            "python": """import sys

def is_valid(s: str) -> bool:
    # TODO: Write your code here
    # Return True if the bracket string is valid, False otherwise
    return False

if __name__ == '__main__':
    raw = sys.stdin.read().strip()
    if raw:
        print("true" if is_valid(raw) else "false")
""",
            "cpp": """#include <iostream>
#include <string>
using namespace std;

bool isValid(const string& s) {
    // TODO: Write your code here
    // Return true if the bracket string is valid, false otherwise
    return false;
}

int main() {
    string s;
    if (cin >> s) {
        cout << (isValid(s) ? "true" : "false") << endl;
    }
    return 0;
}
""",
            "java": """import java.util.*;

public class Main {
    public static boolean isValid(String s) {
        // TODO: Write your code here
        // Return true if the bracket string is valid, false otherwise
        return false;
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        if (sc.hasNext()) {
            String s = sc.next();
            System.out.println(isValid(s) ? "true" : "false");
        }
    }
}
"""
        },
        "test_cases": [
            {"input": "()[]{}", "expected_output": "true", "is_hidden": False, "explanation": "All matched properly"},
            {"input": "(]", "expected_output": "false", "is_hidden": False, "explanation": "Mismatched closing bracket"},
            {"input": "([)]", "expected_output": "false", "is_hidden": True, "explanation": "Interleaved brackets are invalid"},
            {"input": "{[]}", "expected_output": "true", "is_hidden": True, "explanation": "Proper nested brackets"},
            {"input": "((((", "expected_output": "false", "is_hidden": True, "explanation": "Unclosed brackets"}
        ]
    },
    {
        "title": "Maximum Subarray",
        "slug": "maximum-subarray",
        "difficulty": "medium",
        "topic": "Dynamic Programming",
        "description": "Given an integer array `nums`, find the subarray with the largest sum, and return its sum.\n\nA subarray is a contiguous non-empty sequence of elements within an array.",
        "constraints": "- 1 <= nums.length <= 10^5\n- -10^4 <= nums[i] <= 10^4",
        "input_format": "The first line contains integer N (size of array).\nThe second line contains N space-separated integers.",
        "sample_input": "9\n-2 1 -3 4 -1 2 1 -5 4",
        "sample_output": "6",
        "hints": [
            "Use Kadane's algorithm: maintain the current running sum and reset it to zero if it becomes negative.",
            "Keep track of the maximum sum observed so far."
        ],
        "starter_code": {
            "python": """import sys

def max_sub_array(nums):
    # TODO: Write your code here
    # Return the maximum contiguous subarray sum
    return 0

if __name__ == '__main__':
    raw = sys.stdin.read().strip().split()
    if raw:
        n = int(raw[0])
        nums = [int(x) for x in raw[1:1+n]]
        print(max_sub_array(nums))
""",
            "cpp": """#include <iostream>
#include <vector>
using namespace std;

int maxSubArray(const vector<int>& nums) {
    // TODO: Write your code here
    // Return the maximum contiguous subarray sum
    return 0;
}

int main() {
    int n;
    if (cin >> n) {
        vector<int> nums(n);
        for (int i = 0; i < n; i++) cin >> nums[i];
        cout << maxSubArray(nums) << endl;
    }
    return 0;
}
""",
            "java": """import java.util.*;

public class Main {
    public static int maxSubArray(int[] nums) {
        // TODO: Write your code here
        // Return the maximum contiguous subarray sum
        return 0;
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        if (sc.hasNextInt()) {
            int n = sc.nextInt();
            int[] nums = new int[n];
            for (int i = 0; i < n; i++) nums[i] = sc.nextInt();
            System.out.println(maxSubArray(nums));
        }
    }
}
"""
        },
        "test_cases": [
            {"input": "9\n-2 1 -3 4 -1 2 1 -5 4", "expected_output": "6", "is_hidden": False, "explanation": "[4,-1,2,1] has the largest sum = 6"},
            {"input": "1\n1", "expected_output": "1", "is_hidden": False, "explanation": "Single element array"},
            {"input": "5\n5 4 -1 7 8", "expected_output": "23", "is_hidden": True, "explanation": "[5,4,-1,7,8] has largest sum 23"},
            {"input": "3\n-3 -2 -1", "expected_output": "-1", "is_hidden": True, "explanation": "All negative numbers: maximum is -1"}
        ]
    },
    {
        "title": "Binary Search",
        "slug": "binary-search",
        "difficulty": "easy",
        "topic": "Binary Search",
        "description": "Given an array of integers `nums` which is sorted in ascending order, and an integer `target`, write a function to search `target` in `nums`. If `target` exists, then return its 0-based index. Otherwise, return -1.\n\nYou must write an algorithm with `O(log n)` runtime complexity.",
        "constraints": "- 1 <= nums.length <= 10^4\n- -10^4 < nums[i], target < 10^4\n- All integers in `nums` are unique and sorted in ascending order.",
        "input_format": "The first line contains N (size) and target separated by space.\nThe second line contains N sorted integers.",
        "sample_input": "6 9\n-1 0 3 5 9 12",
        "sample_output": "4",
        "hints": [
            "Use two pointers, `left` and `right`. Check the middle element and halve the search interval each step."
        ],
        "starter_code": {
            "python": """import sys

def search(nums, target):
    # TODO: Write your code here
    # Return 0-based index if target exists in sorted nums, else return -1
    return -1

if __name__ == '__main__':
    raw = sys.stdin.read().strip().split()
    if raw:
        n = int(raw[0])
        target = int(raw[1])
        nums = [int(x) for x in raw[2:2+n]]
        print(search(nums, target))
""",
            "cpp": """#include <iostream>
#include <vector>
using namespace std;

int search(const vector<int>& nums, int target) {
    // TODO: Write your code here
    // Return 0-based index if target exists in sorted nums, else return -1
    return -1;
}

int main() {
    int n, target;
    if (cin >> n >> target) {
        vector<int> nums(n);
        for (int i = 0; i < n; i++) cin >> nums[i];
        cout << search(nums, target) << endl;
    }
    return 0;
}
""",
            "java": """import java.util.*;

public class Main {
    public static int search(int[] nums, int target) {
        // TODO: Write your code here
        // Return 0-based index if target exists in sorted nums, else return -1
        return -1;
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        if (sc.hasNextInt()) {
            int n = sc.nextInt();
            int target = sc.nextInt();
            int[] nums = new int[n];
            for (int i = 0; i < n; i++) nums[i] = sc.nextInt();
            System.out.println(search(nums, target));
        }
    }
}
"""
        },
        "test_cases": [
            {"input": "6 9\n-1 0 3 5 9 12", "expected_output": "4", "is_hidden": False, "explanation": "9 exists in nums and its index is 4"},
            {"input": "6 2\n-1 0 3 5 9 12", "expected_output": "-1", "is_hidden": False, "explanation": "2 does not exist in nums so return -1"},
            {"input": "1 5\n5", "expected_output": "0", "is_hidden": True, "explanation": "Single item match"},
            {"input": "5 100\n1 2 3 4 5", "expected_output": "-1", "is_hidden": True, "explanation": "Target exceeds max value"}
        ]
    },
    {
        "title": "Longest Substring Without Repeating Characters",
        "slug": "longest-substring-without-repeating-characters",
        "difficulty": "medium",
        "topic": "Sliding Window",
        "description": "Given a string `s`, find the length of the longest substring without duplicate characters.\n\nA substring is a contiguous sequence of characters within a string.",
        "constraints": "- 0 <= s.length <= 5 * 10^4\n- `s` consists of English letters, digits, symbols and spaces.",
        "input_format": "A single line containing the string `s`.",
        "sample_input": "abcabcbb",
        "sample_output": "3",
        "hints": [
            "Use the sliding window technique with two pointers `left` and `right`.",
            "Keep a hash set or dictionary of the most recent index of each character to expand or shrink the window."
        ],
        "starter_code": {
            "python": """import sys

def length_of_longest_substring(s: str) -> int:
    # TODO: Write your code here
    # Return the length of the longest substring without duplicate characters
    return 0

if __name__ == '__main__':
    s = sys.stdin.readline().rstrip('\\r\\n')
    print(length_of_longest_substring(s))
""",
            "cpp": """#include <iostream>
#include <string>
using namespace std;

int lengthOfLongestSubstring(const string& s) {
    // TODO: Write your code here
    // Return the length of the longest substring without duplicate characters
    return 0;
}

int main() {
    string s;
    if (getline(cin, s)) {
        cout << lengthOfLongestSubstring(s) << endl;
    }
    return 0;
}
""",
            "java": """import java.util.*;

public class Main {
    public static int lengthOfLongestSubstring(String s) {
        // TODO: Write your code here
        // Return the length of the longest substring without duplicate characters
        return 0;
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        String s = sc.hasNextLine() ? sc.nextLine() : "";
        System.out.println(lengthOfLongestSubstring(s));
    }
}
"""
        },
        "test_cases": [
            {"input": "abcabcbb", "expected_output": "3", "is_hidden": False, "explanation": "The answer is 'abc', with the length of 3."},
            {"input": "bbbbb", "expected_output": "1", "is_hidden": False, "explanation": "The answer is 'b', with the length of 1."},
            {"input": "pwwkew", "expected_output": "3", "is_hidden": True, "explanation": "The answer is 'wke', with the length of 3."},
            {"input": "dvdf", "expected_output": "3", "is_hidden": True, "explanation": "'vdf' has length 3"}
        ]
    },
    {
        "title": "Trapping Rain Water",
        "slug": "trapping-rain-water",
        "difficulty": "hard",
        "topic": "Two Pointers",
        "description": "Given `n` non-negative integers representing an elevation map where the width of each bar is 1, compute how much water it can trap after raining.",
        "constraints": "- n == height.length\n- 1 <= n <= 2 * 10^4\n- 0 <= height[i] <= 10^5",
        "input_format": "The first line contains integer N.\nThe second line contains N space-separated integers representing the bar heights.",
        "sample_input": "12\n0 1 0 2 1 0 1 3 2 1 2 1",
        "sample_output": "6",
        "hints": [
            "Use two pointers from left and right towards the center, keeping track of `max_left` and `max_right`.",
            "Water trapped at index i is determined by min(max_left, max_right) - height[i]."
        ],
        "starter_code": {
            "python": """import sys

def trap(height):
    # TODO: Write your code here
    # Return the total units of trapped rain water
    return 0

if __name__ == '__main__':
    raw = sys.stdin.read().strip().split()
    if raw:
        n = int(raw[0])
        height = [int(x) for x in raw[1:1+n]]
        print(trap(height))
""",
            "cpp": """#include <iostream>
#include <vector>
using namespace std;

int trap(const vector<int>& height) {
    // TODO: Write your code here
    // Return the total units of trapped rain water
    return 0;
}

int main() {
    int n;
    if (cin >> n) {
        vector<int> height(n);
        for (int i = 0; i < n; i++) cin >> height[i];
        cout << trap(height) << endl;
    }
    return 0;
}
""",
            "java": """import java.util.*;

public class Main {
    public static int trap(int[] height) {
        // TODO: Write your code here
        // Return the total units of trapped rain water
        return 0;
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        if (sc.hasNextInt()) {
            int n = sc.nextInt();
            int[] height = new int[n];
            for (int i = 0; i < n; i++) height[i] = sc.nextInt();
            System.out.println(trap(height));
        }
    }
}
"""
        },
        "test_cases": [
            {"input": "12\n0 1 0 2 1 0 1 3 2 1 2 1", "expected_output": "6", "is_hidden": False, "explanation": "6 units of rain water are trapped"},
            {"input": "6\n4 2 0 3 2 5", "expected_output": "9", "is_hidden": False, "explanation": "9 units trapped between 4 and 5"},
            {"input": "3\n1 2 3", "expected_output": "0", "is_hidden": True, "explanation": "Monotonically increasing elevation traps 0 water"},
            {"input": "4\n3 0 0 3", "expected_output": "6", "is_hidden": True, "explanation": "Wide trough traps 3*2 = 6"}
        ]
    }
]
