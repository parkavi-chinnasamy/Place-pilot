-- ============================================================
-- PlacePilot Seed Data
-- NOTE: All student data below is DEMO/SYNTHETIC data
--       used only for prototype demonstration.
-- ============================================================

-- ============================================================
-- JOB ROLES
-- ============================================================

INSERT INTO job_roles (id, name, description) VALUES
('a1000000-0000-0000-0000-000000000001', 'Software Developer',    'General software development role requiring DSA, OOP, and programming fundamentals'),
('a1000000-0000-0000-0000-000000000002', 'Full Stack Developer',  'End-to-end web development with frontend and backend skills'),
('a1000000-0000-0000-0000-000000000003', 'Backend Developer',     'Server-side development with databases and APIs'),
('a1000000-0000-0000-0000-000000000004', 'Frontend Developer',    'UI/UX focused development with modern JavaScript frameworks'),
('a1000000-0000-0000-0000-000000000005', 'Data Analyst',          'Data processing, SQL, statistics, and visualization'),
('a1000000-0000-0000-0000-000000000006', 'AI/ML Engineer',        'Machine learning, deep learning, and AI model development'),
('a1000000-0000-0000-0000-000000000007', 'QA Engineer',           'Quality assurance, testing methodologies, and automation');

-- ============================================================
-- ROLE REQUIREMENTS
-- ============================================================

-- Software Developer
INSERT INTO role_requirements (job_role_id, skill_name, required_score, weight) VALUES
('a1000000-0000-0000-0000-000000000001', 'dsa',           80, 1.5),
('a1000000-0000-0000-0000-000000000001', 'programming',   75, 1.3),
('a1000000-0000-0000-0000-000000000001', 'dbms',          70, 1.0),
('a1000000-0000-0000-0000-000000000001', 'oop',           70, 1.2),
('a1000000-0000-0000-0000-000000000001', 'aptitude',      65, 0.8),
('a1000000-0000-0000-0000-000000000001', 'interview',     70, 1.0),
('a1000000-0000-0000-0000-000000000001', 'resume',        65, 0.7),
('a1000000-0000-0000-0000-000000000001', 'leetcode',      60, 0.8);

-- Full Stack Developer
INSERT INTO role_requirements (job_role_id, skill_name, required_score, weight) VALUES
('a1000000-0000-0000-0000-000000000002', 'web_dev',       85, 1.5),
('a1000000-0000-0000-0000-000000000002', 'programming',   80, 1.3),
('a1000000-0000-0000-0000-000000000002', 'dbms',          75, 1.2),
('a1000000-0000-0000-0000-000000000002', 'dsa',           65, 0.8),
('a1000000-0000-0000-0000-000000000002', 'interview',     70, 1.0),
('a1000000-0000-0000-0000-000000000002', 'resume',        70, 0.8),
('a1000000-0000-0000-0000-000000000002', 'aptitude',      60, 0.7);

-- Backend Developer
INSERT INTO role_requirements (job_role_id, skill_name, required_score, weight) VALUES
('a1000000-0000-0000-0000-000000000003', 'programming',   80, 1.5),
('a1000000-0000-0000-0000-000000000003', 'dbms',          80, 1.5),
('a1000000-0000-0000-0000-000000000003', 'dsa',           75, 1.2),
('a1000000-0000-0000-0000-000000000003', 'oop',           75, 1.2),
('a1000000-0000-0000-0000-000000000003', 'aptitude',      65, 0.8),
('a1000000-0000-0000-0000-000000000003', 'interview',     70, 1.0),
('a1000000-0000-0000-0000-000000000003', 'resume',        65, 0.7);

-- Data Analyst
INSERT INTO role_requirements (job_role_id, skill_name, required_score, weight) VALUES
('a1000000-0000-0000-0000-000000000005', 'dbms',          85, 1.5),
('a1000000-0000-0000-0000-000000000005', 'aptitude',      80, 1.3),
('a1000000-0000-0000-0000-000000000005', 'aiml',          70, 1.2),
('a1000000-0000-0000-0000-000000000005', 'programming',   70, 1.0),
('a1000000-0000-0000-0000-000000000005', 'interview',     65, 0.8),
('a1000000-0000-0000-0000-000000000005', 'resume',        65, 0.7);

-- AI/ML Engineer
INSERT INTO role_requirements (job_role_id, skill_name, required_score, weight) VALUES
('a1000000-0000-0000-0000-000000000006', 'aiml',          85, 1.5),
('a1000000-0000-0000-0000-000000000006', 'programming',   80, 1.3),
('a1000000-0000-0000-0000-000000000006', 'dsa',           75, 1.0),
('a1000000-0000-0000-0000-000000000006', 'aptitude',      75, 1.0),
('a1000000-0000-0000-0000-000000000006', 'dbms',          65, 0.8),
('a1000000-0000-0000-0000-000000000006', 'interview',     70, 1.0),
('a1000000-0000-0000-0000-000000000006', 'leetcode',      65, 0.9);

-- QA Engineer
INSERT INTO role_requirements (job_role_id, skill_name, required_score, weight) VALUES
('a1000000-0000-0000-0000-000000000007', 'programming',   70, 1.2),
('a1000000-0000-0000-0000-000000000007', 'aptitude',      75, 1.3),
('a1000000-0000-0000-0000-000000000007', 'dbms',          65, 0.9),
('a1000000-0000-0000-0000-000000000007', 'communication', 80, 1.2),
('a1000000-0000-0000-0000-000000000007', 'interview',     70, 1.0),
('a1000000-0000-0000-0000-000000000007', 'resume',        65, 0.7);

-- ============================================================
-- APTITUDE QUESTIONS (20 questions)
-- ============================================================

INSERT INTO assessment_questions (assessment_type, topic, question_text, option_a, option_b, option_c, option_d, correct_option, explanation, difficulty) VALUES
('aptitude','Quantitative','A train travels 360 km in 4 hours. What is its speed in m/s?','20 m/s','25 m/s','30 m/s','22.5 m/s','B','Speed = 360/4 = 90 km/h = 90 × 5/18 = 25 m/s','easy'),
('aptitude','Quantitative','If 8 workers can complete a task in 12 days, how many days will 6 workers take?','14','16','18','20','B','Workers × Days = Constant: 8×12 = 96; 96/6 = 16 days','easy'),
('aptitude','Quantitative','What is 15% of 480?','66','72','76','78','B','15/100 × 480 = 72','easy'),
('aptitude','Quantitative','A shopkeeper marks up a product by 40% and then gives a 20% discount. What is the net profit percentage?','10%','12%','14%','8%','B','Net = 1.4 × 0.8 = 1.12 → 12% profit','medium'),
('aptitude','Quantitative','Two pipes fill a tank in 12 and 15 minutes respectively. How long will they take together?','6.67 min','6 min','7 min','5.5 min','A','1/12 + 1/15 = 9/60 = 3/20; Time = 20/3 ≈ 6.67 min','medium'),
('aptitude','Logical','Find the next number: 2, 6, 12, 20, 30, ?','40','42','44','46','B','Differences: 4,6,8,10,12 → 30+12=42','easy'),
('aptitude','Logical','If all Bloops are Razzles, and all Razzles are Lazzles, then all Bloops are definitely:','not Lazzles','Lazzles','not Razzles','none of the above','B','Transitive relation: Bloops→Razzles→Lazzles','easy'),
('aptitude','Logical','A clock shows 3:15. What is the angle between the hour and minute hands?','7.5°','8°','6°','5°','A','Hour hand at 97.5°, minute at 90°; difference = 7.5°','medium'),
('aptitude','Verbal','Choose the word most opposite in meaning to ENIGMATIC:','Mysterious','Clear','Cryptic','Puzzling','B','Enigmatic means mysterious; opposite is clear/obvious','easy'),
('aptitude','Verbal','Select the correctly spelled word:','Accomodate','Accommodate','Acommodate','Accommoddate','B','Correct spelling is Accommodate','easy'),
('aptitude','Data Interpretation','In a class of 60, 40% passed in Math, 50% passed in Science, and 30% passed in both. How many failed in both?','18','24','12','15','A','Passed in at least one = 40+50-30 = 60%. Failed in both = 40% of 60 = 24. Wait: 40% failed both = 0.4×60=24. Check: passed only math=10%, only sci=20%, both=30%, total passed=60%, failed=40%=24','medium'),
('aptitude','Quantitative','The ratio of ages of A and B is 3:5. After 10 years, the ratio will be 5:7. Find A''s current age.','15','20','25','10','A','3x+10/5x+10=5/7 → 21x+70=25x+50 → 4x=20 → x=5; A=15','medium'),
('aptitude','Logical','Complete the series: ACE, BDF, CEG, ?','DFH','DEF','EFG','DGH','A','Each letter increments by 1 in each position','easy'),
('aptitude','Quantitative','Simple interest on Rs. 8000 at 5% per annum for 3 years is:','Rs. 1200','Rs. 1000','Rs. 1400','Rs. 1600','A','SI = 8000×5×3/100 = 1200','easy'),
('aptitude','Quantitative','A man walks at 5 km/h and runs at 10 km/h. He covers 50 km in 7 hours. How far did he run?','30 km','20 km','25 km','35 km','A','Let walking distance = x; x/5 + (50-x)/10 = 7 → 2x+50-x=70 → x=20. Running = 30 km','medium'),
('aptitude','Logical','If CLOUD is coded as DMPVE, how is FLAME coded?','GMBOF','GNDOF','GMBNF','GNBOF','A','Each letter shifts by +1: F→G, L→M, A→B, M→N, E→F → GMBNE. Actually: C+1=D,L+1=M,O+1=P,U+1=V,D+1=E=DMPVE ✓; F+1=G,L+1=M,A+1=B,M+1=N,E+1=F=GMBNF','medium'),
('aptitude','Quantitative','The compound interest on Rs. 10000 at 10% per annum for 2 years is:','Rs. 2000','Rs. 2100','Rs. 2200','Rs. 1900','B','CI = 10000(1.1)²-10000 = 12100-10000 = 2100','medium'),
('aptitude','Verbal','Find the odd one out: Laptop, Keyboard, Monitor, Mouse, Hard disk','Laptop','Keyboard','Monitor','Mouse','A','Laptop is a complete system; others are peripherals/components','easy'),
('aptitude','Logical','A is taller than B. C is shorter than A. D is taller than C but shorter than B. Who is the shortest?','A','B','C','D','C','A>B>D>C → C is shortest','medium'),
('aptitude','Quantitative','Find the value of √(0.0256)','0.16','0.016','1.6','0.6','A','√(256/10000) = 16/100 = 0.16','easy');

-- ============================================================
-- TECHNICAL / DBMS QUESTIONS (20 questions)
-- ============================================================

INSERT INTO assessment_questions (assessment_type, topic, question_text, option_a, option_b, option_c, option_d, correct_option, explanation, difficulty) VALUES
('technical','DBMS','Which normal form eliminates partial dependencies?','1NF','2NF','3NF','BCNF','B','2NF removes partial dependencies on composite primary keys','easy'),
('technical','DBMS','What does ACID stand for in database transactions?','Atomicity, Consistency, Isolation, Durability','Availability, Consistency, Isolation, Durability','Atomicity, Concurrency, Isolation, Durability','Atomicity, Consistency, Integration, Durability','A','ACID properties ensure reliable database transactions','easy'),
('technical','DBMS','Which JOIN returns all rows from both tables, including unmatched rows?','INNER JOIN','LEFT JOIN','RIGHT JOIN','FULL OUTER JOIN','D','FULL OUTER JOIN returns all rows from both tables','easy'),
('technical','DBMS','What is the purpose of the GROUP BY clause?','Sort rows','Filter rows','Group rows for aggregate functions','Join tables','C','GROUP BY groups rows sharing same values for aggregate operations','easy'),
('technical','DBMS','Which index type is best for equality searches on high-cardinality columns?','B-Tree','Hash','Bitmap','GIN','B','Hash indexes are optimized for equality comparisons','medium'),
('technical','DBMS','What is a deadlock in DBMS?','Two transactions waiting for each other''s resources','A transaction that never completes','A corrupt database state','A broken foreign key','A','Deadlock: circular dependency where transactions block each other','medium'),
('technical','OOP','Which OOP principle hides internal implementation details?','Inheritance','Polymorphism','Encapsulation','Abstraction','C','Encapsulation bundles data and methods, hiding internal state','easy'),
('technical','OOP','What is method overloading?','Redefining a parent method in child class','Multiple methods with same name but different parameters','A method calling itself','None of the above','B','Overloading: same method name, different signatures (compile-time polymorphism)','easy'),
('technical','OOP','Which design pattern ensures only one instance of a class exists?','Factory','Observer','Singleton','Strategy','C','Singleton pattern restricts instantiation to a single object','medium'),
('technical','OOP','What is the Liskov Substitution Principle?','Classes should have single responsibility','Subtypes must be substitutable for their base types','Depend on abstractions not concretions','Open for extension closed for modification','B','LSP: objects of a superclass shall be replaceable with objects of subclasses','medium'),
('technical','Networking','What does HTTP status code 404 mean?','Internal Server Error','Unauthorized','Not Found','Bad Request','C','404 means the requested resource was not found on the server','easy'),
('technical','Networking','Which layer of the OSI model handles routing?','Data Link','Network','Transport','Session','B','Layer 3 (Network) is responsible for routing packets between networks','easy'),
('technical','OS','What is a semaphore used for in operating systems?','Memory management','Process synchronization','File handling','CPU scheduling','B','Semaphores control access to shared resources and enable synchronization','medium'),
('technical','OS','Which scheduling algorithm can cause starvation?','Round Robin','FCFS','Priority Scheduling','SJF','C','Priority Scheduling can starve low-priority processes','medium'),
('technical','DBMS','What does the HAVING clause do in SQL?','Filter rows before grouping','Filter groups after GROUP BY','Join tables','Sort results','B','HAVING filters groups based on aggregate conditions (used with GROUP BY)','medium'),
('technical','DBMS','Which SQL command is used to remove all rows from a table without logging individual deletions?','DELETE','DROP','TRUNCATE','REMOVE','C','TRUNCATE removes all rows faster than DELETE, without transaction log per row','easy'),
('technical','OOP','What is the difference between an interface and an abstract class?','No difference','Interface has method bodies, abstract class does not','Abstract class can have method bodies; interface traditionally cannot','Interface supports multiple inheritance, abstract class does not','D','Key distinction: classes can implement multiple interfaces but extend only one abstract class','medium'),
('technical','DBMS','What is a foreign key?','Primary key in same table','A key that references the primary key of another table','A composite key','A unique constraint','B','Foreign key enforces referential integrity between tables','easy'),
('technical','Networking','What is the purpose of DNS?','Encrypt data','Translate domain names to IP addresses','Assign IP addresses','Route packets','B','DNS (Domain Name System) translates human-readable names to IP addresses','easy'),
('technical','OS','What is virtual memory?','Physical RAM','Extra storage on disk used as RAM extension','Cache memory','GPU memory','B','Virtual memory uses disk space to extend available memory, enabling larger programs to run','medium');

-- ============================================================
-- CODING QUESTIONS (20 questions)
-- ============================================================

INSERT INTO assessment_questions (assessment_type, topic, question_text, option_a, option_b, option_c, option_d, correct_option, explanation, difficulty) VALUES
('coding','Arrays','What is the time complexity of binary search?','O(n)','O(log n)','O(n log n)','O(1)','B','Binary search halves the search space each step → O(log n)','easy'),
('coding','Sorting','Which sorting algorithm has best average-case complexity?','Bubble Sort','Selection Sort','Merge Sort','Insertion Sort','C','Merge Sort guarantees O(n log n) in all cases','easy'),
('coding','Data Structures','Which data structure uses LIFO order?','Queue','Stack','Heap','Tree','B','Stack follows Last-In, First-Out order','easy'),
('coding','Graphs','BFS uses which data structure?','Stack','Priority Queue','Queue','Array','C','BFS uses a Queue to visit nodes level by level','easy'),
('coding','Dynamic Programming','What is the time complexity of the standard Fibonacci DP solution?','O(2^n)','O(n)','O(n log n)','O(n²)','B','Bottom-up DP computes each Fibonacci number once → O(n)','medium'),
('coding','Trees','What is the height of a balanced BST with n nodes?','O(n)','O(log n)','O(n²)','O(1)','B','A balanced BST has height O(log n)','easy'),
('coding','Strings','What is the time complexity of the KMP string matching algorithm?','O(nm)','O(n+m)','O(n log m)','O(m²)','B','KMP runs in O(n+m) where n is text length and m is pattern length','hard'),
('coding','Arrays','Given array [3,1,4,1,5,9], what does two-pointer technique help solve efficiently?','Finding max element','Finding pair with target sum','Sorting','Counting duplicates','B','Two-pointer technique efficiently finds pairs summing to a target in O(n) on sorted arrays','medium'),
('coding','Graphs','Which algorithm finds the shortest path in a weighted graph with non-negative weights?','BFS','DFS','Dijkstra','Bellman-Ford','C','Dijkstra''s algorithm finds shortest paths in graphs with non-negative edge weights','medium'),
('coding','Dynamic Programming','The 0/1 Knapsack problem has time complexity:','O(n)','O(n×W)','O(W)','O(2^n) optimized to O(nW)','B','Standard DP approach is O(n×W) where n=items, W=capacity','medium'),
('coding','Trees','Which traversal of a BST gives sorted output?','Preorder','Postorder','Inorder','Level-order','C','Inorder traversal (Left-Root-Right) of BST produces sorted sequence','easy'),
('coding','Arrays','What does the sliding window technique optimize?','Tree traversals','Subarray/substring problems with fixed/variable windows','Graph BFS','Sorting algorithms','B','Sliding window reduces brute-force O(n²) subarray problems to O(n)','medium'),
('coding','Hashing','Average time complexity of HashMap get/put operations?','O(n)','O(log n)','O(1)','O(n log n)','C','HashMap uses hash function for O(1) average case access','easy'),
('coding','Graphs','Which algorithm detects cycles in a directed graph?','BFS only','DFS with coloring','Dijkstra','Kruskal','B','DFS with 3-color marking (white/gray/black) detects back edges = cycles','medium'),
('coding','Recursion','What is tail recursion?','Recursion with multiple calls','Recursion where recursive call is last operation','Recursion without base case','Mutual recursion','B','Tail recursion allows compilers to optimize stack usage','medium'),
('coding','Sorting','QuickSort''s worst-case time complexity is:','O(n log n)','O(n)','O(n²)','O(n³)','C','Worst case occurs when pivot selection is always smallest/largest element','medium'),
('coding','Data Structures','Which data structure is ideal for implementing a priority queue?','Linked List','Array','Heap','Stack','C','Binary Heap supports O(log n) insert/extract-min/max for priority queues','easy'),
('coding','Greedy','Activity Selection Problem is solved using which approach?','Dynamic Programming','Greedy (sort by finish time)','Divide and Conquer','Backtracking','B','Greedy: selecting activity with earliest finish time is optimal','medium'),
('coding','Backtracking','N-Queens problem uses which technique?','Greedy','BFS','Backtracking','DP','C','Backtracking systematically tries all placements, pruning invalid states','medium'),
('coding','Arrays','What is the space complexity of merge sort?','O(1)','O(log n)','O(n)','O(n log n)','C','Merge sort requires O(n) auxiliary space for merging','medium');

-- ============================================================
-- ADMIN USER
-- ============================================================

-- Password: Admin@123! (bcrypt hash)
INSERT INTO users (id, email, hashed_password, full_name, role, is_demo) VALUES
('b0000000-0000-0000-0000-000000000001',
 'admin@placepilot.edu',
 '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TqznefZkFOiHMd9gGVMKQaxRZDXq',
 'Placement Admin',
 'admin',
 FALSE);

INSERT INTO admins (user_id, designation, college) VALUES
('b0000000-0000-0000-0000-000000000001', 'Placement Officer', 'Demo Engineering College');

-- ============================================================
-- DEMO STUDENT USERS (20 students)
-- Password for all demo students: Student@123!
-- ============================================================

INSERT INTO users (id, email, hashed_password, full_name, role, is_demo) VALUES
('c0000000-0000-0000-0000-000000000001','ananya.sharma@demo.edu','$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TqznefZkFOiHMd9gGVMKQaxRZDXq','Ananya Sharma','student',TRUE),
('c0000000-0000-0000-0000-000000000002','rahul.verma@demo.edu','$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TqznefZkFOiHMd9gGVMKQaxRZDXq','Rahul Verma','student',TRUE),
('c0000000-0000-0000-0000-000000000003','priya.menon@demo.edu','$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TqznefZkFOiHMd9gGVMKQaxRZDXq','Priya Menon','student',TRUE),
('c0000000-0000-0000-0000-000000000004','arjun.nair@demo.edu','$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TqznefZkFOiHMd9gGVMKQaxRZDXq','Arjun Nair','student',TRUE),
('c0000000-0000-0000-0000-000000000005','divya.krishna@demo.edu','$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TqznefZkFOiHMd9gGVMKQaxRZDXq','Divya Krishna','student',TRUE),
('c0000000-0000-0000-0000-000000000006','karthik.rajan@demo.edu','$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TqznefZkFOiHMd9gGVMKQaxRZDXq','Karthik Rajan','student',TRUE),
('c0000000-0000-0000-0000-000000000007','sneha.patel@demo.edu','$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TqznefZkFOiHMd9gGVMKQaxRZDXq','Sneha Patel','student',TRUE),
('c0000000-0000-0000-0000-000000000008','vikram.singh@demo.edu','$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TqznefZkFOiHMd9gGVMKQaxRZDXq','Vikram Singh','student',TRUE),
('c0000000-0000-0000-0000-000000000009','meera.iyer@demo.edu','$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TqznefZkFOiHMd9gGVMKQaxRZDXq','Meera Iyer','student',TRUE),
('c0000000-0000-0000-0000-000000000010','rohan.gupta@demo.edu','$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TqznefZkFOiHMd9gGVMKQaxRZDXq','Rohan Gupta','student',TRUE),
('c0000000-0000-0000-0000-000000000011','aisha.khan@demo.edu','$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TqznefZkFOiHMd9gGVMKQaxRZDXq','Aisha Khan','student',TRUE),
('c0000000-0000-0000-0000-000000000012','suresh.babu@demo.edu','$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TqznefZkFOiHMd9gGVMKQaxRZDXq','Suresh Babu','student',TRUE),
('c0000000-0000-0000-0000-000000000013','lakshmi.prasad@demo.edu','$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TqznefZkFOiHMd9gGVMKQaxRZDXq','Lakshmi Prasad','student',TRUE),
('c0000000-0000-0000-0000-000000000014','deepak.sharma@demo.edu','$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TqznefZkFOiHMd9gGVMKQaxRZDXq','Deepak Sharma','student',TRUE),
('c0000000-0000-0000-0000-000000000015','pooja.reddy@demo.edu','$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TqznefZkFOiHMd9gGVMKQaxRZDXq','Pooja Reddy','student',TRUE),
('c0000000-0000-0000-0000-000000000016','amit.joshi@demo.edu','$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TqznefZkFOiHMd9gGVMKQaxRZDXq','Amit Joshi','student',TRUE),
('c0000000-0000-0000-0000-000000000017','kavya.nambiar@demo.edu','$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TqznefZkFOiHMd9gGVMKQaxRZDXq','Kavya Nambiar','student',TRUE),
('c0000000-0000-0000-0000-000000000018','siddharth.bose@demo.edu','$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TqznefZkFOiHMd9gGVMKQaxRZDXq','Siddharth Bose','student',TRUE),
('c0000000-0000-0000-0000-000000000019','harini.venkatesan@demo.edu','$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TqznefZkFOiHMd9gGVMKQaxRZDXq','Harini Venkatesan','student',TRUE),
('c0000000-0000-0000-0000-000000000020','nikhil.tiwari@demo.edu','$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TqznefZkFOiHMd9gGVMKQaxRZDXq','Nikhil Tiwari','student',TRUE);

-- ============================================================
-- DEMO STUDENT PROFILES
-- ============================================================

INSERT INTO students (id, user_id, phone, college, department, batch, year, cgpa, tenth_percent, twelfth_percent,
    skill_programming, skill_dsa, skill_dbms, skill_oop, skill_web_dev, skill_aiml, skill_communication,
    programming_languages, target_role_id, profile_completeness) VALUES
('d0000000-0000-0000-0000-000000000001','c0000000-0000-0000-0000-000000000001','9876543201','Demo Engineering College','Computer Science','2024',4,8.2,88.5,91.0, 78,75,52,70,65,60,72, ARRAY['Python','Java','C++'], 'a1000000-0000-0000-0000-000000000001', 85),
('d0000000-0000-0000-0000-000000000002','c0000000-0000-0000-0000-000000000002','9876543202','Demo Engineering College','Computer Science','2024',4,7.5,79.0,82.0, 65,60,75,68,72,45,65, ARRAY['Java','C','Python'], 'a1000000-0000-0000-0000-000000000001', 80),
('d0000000-0000-0000-0000-000000000003','c0000000-0000-0000-0000-000000000003','9876543203','Demo Engineering College','Information Technology','2024',4,8.8,92.0,89.5, 85,80,78,82,88,70,80, ARRAY['React','Node.js','Python'], 'a1000000-0000-0000-0000-000000000002', 90),
('d0000000-0000-0000-0000-000000000004','c0000000-0000-0000-0000-000000000004','9876543204','Demo Engineering College','Computer Science','2024',4,6.9,72.0,75.0, 55,48,60,55,40,35,50, ARRAY['C','Java'], 'a1000000-0000-0000-0000-000000000001', 65),
('d0000000-0000-0000-0000-000000000005','c0000000-0000-0000-0000-000000000005','9876543205','Demo Engineering College','Information Technology','2024',4,7.8,85.0,87.0, 72,68,72,70,80,65,75, ARRAY['JavaScript','React','CSS'], 'a1000000-0000-0000-0000-000000000004', 82),
('d0000000-0000-0000-0000-000000000006','c0000000-0000-0000-0000-000000000006','9876543206','Demo Engineering College','Electronics','2024',4,7.2,80.0,82.0, 60,55,65,62,45,50,68, ARRAY['Python','MATLAB'], 'a1000000-0000-0000-0000-000000000005', 70),
('d0000000-0000-0000-0000-000000000007','c0000000-0000-0000-0000-000000000007','9876543207','Demo Engineering College','Computer Science','2024',4,9.1,95.0,94.0, 90,88,85,88,82,80,85, ARRAY['Python','TensorFlow','Java'], 'a1000000-0000-0000-0000-000000000006', 95),
('d0000000-0000-0000-0000-000000000008','c0000000-0000-0000-0000-000000000008','9876543208','Demo Engineering College','Mechanical','2024',4,6.5,68.0,70.0, 45,40,50,42,30,25,55, ARRAY['C'], 'a1000000-0000-0000-0000-000000000007', 55),
('d0000000-0000-0000-0000-000000000009','c0000000-0000-0000-0000-000000000009','9876543209','Demo Engineering College','Computer Science','2024',4,8.5,90.0,88.0, 82,78,80,80,75,72,78, ARRAY['Java','Spring','SQL'], 'a1000000-0000-0000-0000-000000000003', 88),
('d0000000-0000-0000-0000-000000000010','c0000000-0000-0000-0000-000000000010','9876543210','Demo Engineering College','Information Technology','2024',4,7.0,75.0,78.0, 65,62,58,60,55,48,60, ARRAY['Python','JavaScript'], 'a1000000-0000-0000-0000-000000000001', 72),
('d0000000-0000-0000-0000-000000000011','c0000000-0000-0000-0000-000000000011','9876543211','Demo Engineering College','Computer Science','2024',4,8.0,87.0,85.0, 75,72,70,75,68,65,72, ARRAY['Python','R','SQL'], 'a1000000-0000-0000-0000-000000000005', 84),
('d0000000-0000-0000-0000-000000000012','c0000000-0000-0000-0000-000000000012','9876543212','Demo Engineering College','Electronics','2024',4,6.8,73.0,76.0, 52,50,55,50,48,42,58, ARRAY['C','C++'], 'a1000000-0000-0000-0000-000000000007', 62),
('d0000000-0000-0000-0000-000000000013','c0000000-0000-0000-0000-000000000013','9876543213','Demo Engineering College','Information Technology','2024',4,8.3,86.0,90.0, 80,78,82,78,85,55,76, ARRAY['Node.js','MongoDB','React'], 'a1000000-0000-0000-0000-000000000002', 87),
('d0000000-0000-0000-0000-000000000014','c0000000-0000-0000-0000-000000000014','9876543214','Demo Engineering College','Computer Science','2024',4,7.3,78.0,80.0, 68,65,60,65,60,52,65, ARRAY['Java','Python'], 'a1000000-0000-0000-0000-000000000001', 74),
('d0000000-0000-0000-0000-000000000015','c0000000-0000-0000-0000-000000000015','9876543215','Demo Engineering College','Computer Science','2024',4,7.7,83.0,85.0, 72,70,68,70,74,62,70, ARRAY['Python','Django','SQL'], 'a1000000-0000-0000-0000-000000000003', 80),
('d0000000-0000-0000-0000-000000000016','c0000000-0000-0000-0000-000000000016','9876543216','Demo Engineering College','Mechanical','2024',4,6.2,65.0,68.0, 42,38,45,40,30,28,52, ARRAY['C','MATLAB'], 'a1000000-0000-0000-0000-000000000007', 50),
('d0000000-0000-0000-0000-000000000017','c0000000-0000-0000-0000-000000000017','9876543217','Demo Engineering College','Information Technology','2024',4,8.6,91.0,93.0, 85,82,78,85,90,72,82, ARRAY['React','Vue','TypeScript'], 'a1000000-0000-0000-0000-000000000004', 92),
('d0000000-0000-0000-0000-000000000018','c0000000-0000-0000-0000-000000000018','9876543218','Demo Engineering College','Computer Science','2024',4,7.5,80.0,82.0, 70,68,72,68,65,60,68, ARRAY['Python','NumPy','Pandas'], 'a1000000-0000-0000-0000-000000000006', 78),
('d0000000-0000-0000-0000-000000000019','c0000000-0000-0000-0000-000000000019','9876543219','Demo Engineering College','Information Technology','2024',4,8.9,93.0,95.0, 88,86,84,87,80,78,85, ARRAY['Java','Spring Boot','PostgreSQL'], 'a1000000-0000-0000-0000-000000000003', 93),
('d0000000-0000-0000-0000-000000000020','c0000000-0000-0000-0000-000000000020','9876543220','Demo Engineering College','Computer Science','2024',4,7.1,77.0,79.0, 62,60,58,62,55,50,62, ARRAY['C++','Java'], 'a1000000-0000-0000-0000-000000000001', 71);

-- ============================================================
-- SKILL PROFILES FOR DEMO STUDENTS
-- (NOTE: These are synthetic demo values)
-- ============================================================

INSERT INTO skill_profiles (student_id, dsa_score, programming_score, dbms_score, oop_score, aptitude_score, coding_score, technical_score, interview_score, resume_score, leetcode_score, communication_score, web_dev_score, aiml_score, dsa_observations, dbms_observations, aptitude_observations, coding_observations, interview_observations, resume_observations, dsa_trend, aptitude_trend, coding_trend) VALUES
('d0000000-0000-0000-0000-000000000001', 75.0, 78.0, 52.0, 70.0, 82.0, 76.0, 68.0, 61.0, 75.0, 70.0, 72.0, 65.0, 60.0, 3,4,3,3,1,1,'stable','improving','stable'),
('d0000000-0000-0000-0000-000000000002', 60.0, 65.0, 75.0, 68.0, 68.0, 62.0, 72.0, 72.0, 70.0, 55.0, 65.0, 72.0, 45.0, 2,3,2,2,1,1,'stable','stable','stable'),
('d0000000-0000-0000-0000-000000000003', 80.0, 85.0, 78.0, 82.0, 88.0, 85.0, 80.0, 80.0, 82.0, 78.0, 80.0, 88.0, 70.0, 4,4,4,4,2,2,'improving','improving','improving'),
('d0000000-0000-0000-0000-000000000004', 48.0, 55.0, 60.0, 55.0, 58.0, 50.0, 58.0, 45.0, 50.0, 42.0, 50.0, 40.0, 35.0, 2,2,2,2,1,0,'declining','stable','declining'),
('d0000000-0000-0000-0000-000000000005', 68.0, 72.0, 72.0, 70.0, 75.0, 70.0, 74.0, 68.0, 72.0, 65.0, 75.0, 80.0, 65.0, 3,3,3,3,1,1,'stable','improving','stable'),
('d0000000-0000-0000-0000-000000000006', 55.0, 60.0, 65.0, 62.0, 70.0, 58.0, 68.0, 55.0, 60.0, 50.0, 68.0, 45.0, 50.0, 2,3,3,2,1,1,'stable','stable','stable'),
('d0000000-0000-0000-0000-000000000007', 88.0, 90.0, 85.0, 88.0, 90.0, 90.0, 87.0, 85.0, 88.0, 85.0, 85.0, 82.0, 80.0, 5,5,5,5,3,2,'improving','improving','improving'),
('d0000000-0000-0000-0000-000000000008', 40.0, 45.0, 50.0, 42.0, 52.0, 42.0, 48.0, 40.0, 42.0, 35.0, 55.0, 30.0, 25.0, 1,1,2,1,0,0,'stable','stable','stable'),
('d0000000-0000-0000-0000-000000000009', 78.0, 82.0, 80.0, 80.0, 80.0, 80.0, 82.0, 78.0, 80.0, 75.0, 78.0, 75.0, 72.0, 4,4,4,4,2,2,'improving','stable','improving'),
('d0000000-0000-0000-0000-000000000010', 62.0, 65.0, 58.0, 60.0, 65.0, 64.0, 62.0, 58.0, 60.0, 55.0, 60.0, 55.0, 48.0, 2,2,3,2,1,1,'stable','stable','stable'),
('d0000000-0000-0000-0000-000000000011', 72.0, 75.0, 70.0, 75.0, 78.0, 74.0, 72.0, 70.0, 74.0, 68.0, 72.0, 68.0, 65.0, 3,4,3,3,1,1,'stable','improving','stable'),
('d0000000-0000-0000-0000-000000000012', 50.0, 52.0, 55.0, 50.0, 58.0, 50.0, 56.0, 48.0, 50.0, 42.0, 58.0, 48.0, 42.0, 2,2,2,2,0,0,'stable','stable','stable'),
('d0000000-0000-0000-0000-000000000013', 78.0, 80.0, 82.0, 78.0, 82.0, 80.0, 84.0, 76.0, 80.0, 72.0, 76.0, 85.0, 55.0, 4,4,3,4,2,1,'improving','stable','improving'),
('d0000000-0000-0000-0000-000000000014', 65.0, 68.0, 60.0, 65.0, 68.0, 66.0, 64.0, 60.0, 62.0, 58.0, 65.0, 60.0, 52.0, 3,2,3,3,1,1,'stable','stable','stable'),
('d0000000-0000-0000-0000-000000000015', 70.0, 72.0, 68.0, 70.0, 74.0, 72.0, 70.0, 66.0, 68.0, 64.0, 70.0, 74.0, 62.0, 3,3,3,3,2,1,'stable','improving','stable'),
('d0000000-0000-0000-0000-000000000016', 38.0, 42.0, 45.0, 40.0, 48.0, 40.0, 44.0, 38.0, 40.0, 32.0, 52.0, 30.0, 28.0, 1,1,1,1,0,0,'declining','stable','declining'),
('d0000000-0000-0000-0000-000000000017', 82.0, 85.0, 78.0, 85.0, 85.0, 85.0, 80.0, 82.0, 85.0, 80.0, 82.0, 90.0, 72.0, 4,4,4,5,2,2,'improving','improving','improving'),
('d0000000-0000-0000-0000-000000000018', 68.0, 70.0, 72.0, 68.0, 72.0, 70.0, 74.0, 65.0, 68.0, 62.0, 68.0, 65.0, 60.0, 3,3,3,3,1,1,'stable','stable','stable'),
('d0000000-0000-0000-0000-000000000019', 86.0, 88.0, 84.0, 87.0, 88.0, 88.0, 86.0, 85.0, 86.0, 82.0, 85.0, 80.0, 78.0, 5,5,5,5,3,2,'improving','improving','improving'),
('d0000000-0000-0000-0000-000000000020', 60.0, 62.0, 58.0, 62.0, 62.0, 62.0, 60.0, 55.0, 58.0, 52.0, 62.0, 55.0, 50.0, 2,2,2,2,1,0,'stable','stable','stable');

-- ============================================================
-- LEETCODE PROGRESS FOR DEMO STUDENTS
-- (NOTE: Demo data - not live LeetCode API data)
-- ============================================================

INSERT INTO leetcode_progress (student_id, leetcode_username, total_solved, easy_solved, medium_solved, hard_solved, acceptance_rate, contest_rating, is_demo_data) VALUES
('d0000000-0000-0000-0000-000000000001','ananya_demo',145,65,62,18,62.5,1680,TRUE),
('d0000000-0000-0000-0000-000000000002','rahul_demo',98,55,35,8,58.0,1520,TRUE),
('d0000000-0000-0000-0000-000000000003','priya_demo',210,80,95,35,68.0,1820,TRUE),
('d0000000-0000-0000-0000-000000000004','arjun_demo',45,30,12,3,48.0,1350,TRUE),
('d0000000-0000-0000-0000-000000000005','divya_demo',128,58,55,15,60.0,1640,TRUE),
('d0000000-0000-0000-0000-000000000006','karthik_demo',72,40,25,7,52.0,1430,TRUE),
('d0000000-0000-0000-0000-000000000007','sneha_demo',285,90,130,65,72.0,1950,TRUE),
('d0000000-0000-0000-0000-000000000008','vikram_demo',28,20,7,1,42.0,1280,TRUE),
('d0000000-0000-0000-0000-000000000009','meera_demo',195,75,85,35,66.0,1780,TRUE),
('d0000000-0000-0000-0000-000000000010','rohan_demo',88,48,32,8,55.0,1490,TRUE),
('d0000000-0000-0000-0000-000000000011','aisha_demo',155,65,70,20,63.0,1710,TRUE),
('d0000000-0000-0000-0000-000000000012','suresh_demo',52,35,14,3,46.0,1380,TRUE),
('d0000000-0000-0000-0000-000000000013','lakshmi_demo',178,70,78,30,64.0,1750,TRUE),
('d0000000-0000-0000-0000-000000000014','deepak_demo',105,52,42,11,57.0,1560,TRUE),
('d0000000-0000-0000-0000-000000000015','pooja_demo',138,60,62,16,61.0,1660,TRUE),
('d0000000-0000-0000-0000-000000000016','amit_demo',18,15,3,0,38.0,1220,TRUE),
('d0000000-0000-0000-0000-000000000017','kavya_demo',220,82,100,38,69.0,1860,TRUE),
('d0000000-0000-0000-0000-000000000018','siddharth_demo',122,55,52,15,58.0,1600,TRUE),
('d0000000-0000-0000-0000-000000000019','harini_demo',265,85,120,60,71.0,1920,TRUE),
('d0000000-0000-0000-0000-000000000020','nikhil_demo',80,45,28,7,53.0,1460,TRUE);
