"""
Seed the SQLite database with demo data.
Run: python seed_db.py
"""
import sys, os
sys.path.insert(0, '.')

from app.database import SessionLocal, engine
from app.models.models import *
from app.utils.auth import hash_password
import uuid

db = SessionLocal()

def seed():
    # Check already seeded
    if db.query(User).filter(User.email == "admin@placepilot.edu").first():
        print("Database already seeded.")
        return

    print("Seeding database...")

    # ── Job Roles ──────────────────────────────────────────────────────────────
    roles_data = [
        ("a1000000-0000-0000-0000-000000000001", "Software Developer",    "General software development"),
        ("a1000000-0000-0000-0000-000000000002", "Full Stack Developer",  "End-to-end web development"),
        ("a1000000-0000-0000-0000-000000000003", "Backend Developer",     "Server-side development"),
        ("a1000000-0000-0000-0000-000000000004", "Frontend Developer",    "UI/UX focused development"),
        ("a1000000-0000-0000-0000-000000000005", "Data Analyst",          "Data processing and SQL"),
        ("a1000000-0000-0000-0000-000000000006", "AI/ML Engineer",        "Machine learning development"),
        ("a1000000-0000-0000-0000-000000000007", "QA Engineer",           "Quality assurance and testing"),
    ]
    role_objs = {}
    for rid, name, desc in roles_data:
        r = JobRole(id=rid, name=name, description=desc)
        db.add(r)
        role_objs[rid] = r

    db.flush()

    # ── Role Requirements ───────────────────────────────────────────────────────
    reqs = [
        # Software Developer
        ("a1000000-0000-0000-0000-000000000001", [("dsa",80,1.5),("programming",75,1.3),("dbms",70,1.0),("oop",70,1.2),("aptitude",65,0.8),("interview",70,1.0),("resume",65,0.7),("leetcode",60,0.8)]),
        # Full Stack Developer
        ("a1000000-0000-0000-0000-000000000002", [("web_dev",85,1.5),("programming",80,1.3),("dbms",75,1.2),("dsa",65,0.8),("interview",70,1.0),("resume",70,0.8),("aptitude",60,0.7)]),
        # Backend Developer
        ("a1000000-0000-0000-0000-000000000003", [("programming",80,1.5),("dbms",80,1.5),("dsa",75,1.2),("oop",75,1.2),("aptitude",65,0.8),("interview",70,1.0),("resume",65,0.7)]),
        # Frontend Developer
        ("a1000000-0000-0000-0000-000000000004", [("web_dev",85,1.5),("programming",75,1.3),("dsa",60,0.7),("interview",70,1.0),("resume",70,0.8)]),
        # Data Analyst
        ("a1000000-0000-0000-0000-000000000005", [("dbms",85,1.5),("aptitude",80,1.3),("aiml",70,1.2),("programming",70,1.0),("interview",65,0.8),("resume",65,0.7)]),
        # AI/ML Engineer
        ("a1000000-0000-0000-0000-000000000006", [("aiml",85,1.5),("programming",80,1.3),("dsa",75,1.0),("aptitude",75,1.0),("dbms",65,0.8),("interview",70,1.0),("leetcode",65,0.9)]),
        # QA Engineer
        ("a1000000-0000-0000-0000-000000000007", [("programming",70,1.2),("aptitude",75,1.3),("dbms",65,0.9),("communication",80,1.2),("interview",70,1.0),("resume",65,0.7)]),
    ]
    for role_id, skills in reqs:
        for skill, score, weight in skills:
            db.add(RoleRequirement(job_role_id=role_id, skill_name=skill, required_score=score, weight=weight))

    db.flush()

    # ── Admin User ─────────────────────────────────────────────────────────────
    admin_user = User(
        id="b0000000-0000-0000-0000-000000000001",
        email="admin@placepilot.edu",
        hashed_password=hash_password("Admin@123!"),
        full_name="Placement Admin",
        role=UserRole.admin,
        is_demo=False,
    )
    db.add(admin_user)
    db.flush()
    db.add(Admin(user_id=admin_user.id, designation="Placement Officer", college="Demo Engineering College"))

    # ── Demo Students ──────────────────────────────────────────────────────────
    students_data = [
        ("Ananya Sharma",     "ananya.sharma@demo.edu",     "CS",  "a1000000-0000-0000-0000-000000000001", 8.2, 88, 91, 78,75,52,70,65,60,72, ["Python","Java","C++"], 75,78,52,70,82,76,68,61,75,70,72, 3,4,3,3,1,1),
        ("Rahul Verma",       "rahul.verma@demo.edu",       "CS",  "a1000000-0000-0000-0000-000000000001", 7.5, 79, 82, 65,60,75,68,72,45,65, ["Java","C","Python"],  60,65,75,68,68,62,72,72,70,55,65, 2,3,2,2,1,1),
        ("Priya Menon",       "priya.menon@demo.edu",       "IT",  "a1000000-0000-0000-0000-000000000002", 8.8, 92, 90, 85,80,78,82,88,70,80, ["React","Node.js","Python"], 80,85,78,82,88,85,80,80,82,78,80, 4,4,4,4,2,2),
        ("Arjun Nair",        "arjun.nair@demo.edu",        "CS",  "a1000000-0000-0000-0000-000000000001", 6.9, 72, 75, 55,48,60,55,40,35,50, ["C","Java"],           48,55,60,55,58,50,58,45,50,42,50, 2,2,2,2,1,0),
        ("Divya Krishna",     "divya.krishna@demo.edu",     "IT",  "a1000000-0000-0000-0000-000000000004", 7.8, 85, 87, 72,68,72,70,80,65,75, ["JavaScript","React","CSS"], 68,72,72,70,75,70,74,68,72,65,75, 3,3,3,3,1,1),
        ("Karthik Rajan",     "karthik.rajan@demo.edu",     "ECE", "a1000000-0000-0000-0000-000000000005", 7.2, 80, 82, 60,55,65,62,45,50,68, ["Python","MATLAB"],    55,60,65,62,70,58,68,55,60,50,68, 2,3,3,2,1,1),
        ("Sneha Patel",       "sneha.patel@demo.edu",       "CS",  "a1000000-0000-0000-0000-000000000006", 9.1, 95, 94, 90,88,85,88,82,80,85, ["Python","TensorFlow","Java"], 88,90,85,88,90,90,87,85,88,85,85, 5,5,5,5,3,2),
        ("Vikram Singh",      "vikram.singh@demo.edu",      "MECH","a1000000-0000-0000-0000-000000000007", 6.5, 68, 70, 45,40,50,42,30,25,55, ["C"],                  40,45,50,42,52,42,48,40,42,35,55, 1,1,2,1,0,0),
        ("Meera Iyer",        "meera.iyer@demo.edu",        "CS",  "a1000000-0000-0000-0000-000000000003", 8.5, 90, 88, 82,78,80,80,75,72,78, ["Java","Spring","SQL"], 78,82,80,80,80,80,82,78,80,75,78, 4,4,4,4,2,2),
        ("Rohan Gupta",       "rohan.gupta@demo.edu",       "IT",  "a1000000-0000-0000-0000-000000000001", 7.0, 75, 78, 65,62,58,60,55,48,60, ["Python","JavaScript"], 62,65,58,60,65,64,62,58,60,55,60, 2,2,3,2,1,1),
        ("Aisha Khan",        "aisha.khan@demo.edu",        "CS",  "a1000000-0000-0000-0000-000000000005", 8.0, 87, 85, 75,72,70,75,68,65,72, ["Python","R","SQL"],    72,75,70,75,78,74,72,70,74,68,72, 3,4,3,3,1,1),
        ("Suresh Babu",       "suresh.babu@demo.edu",       "ECE", "a1000000-0000-0000-0000-000000000007", 6.8, 73, 76, 52,50,55,50,48,42,58, ["C","C++"],             50,52,55,50,58,50,56,48,50,42,58, 2,2,2,2,0,0),
        ("Lakshmi Prasad",    "lakshmi.prasad@demo.edu",    "IT",  "a1000000-0000-0000-0000-000000000002", 8.3, 86, 90, 80,78,82,78,85,55,76, ["Node.js","MongoDB","React"], 78,80,82,78,82,80,84,76,80,72,76, 4,4,3,4,2,1),
        ("Deepak Sharma",     "deepak.sharma@demo.edu",     "CS",  "a1000000-0000-0000-0000-000000000001", 7.3, 78, 80, 68,65,60,65,60,52,65, ["Java","Python"],       65,68,60,65,68,66,64,60,62,58,65, 3,2,3,3,1,1),
        ("Pooja Reddy",       "pooja.reddy@demo.edu",       "CS",  "a1000000-0000-0000-0000-000000000003", 7.7, 83, 85, 72,70,68,70,74,62,70, ["Python","Django","SQL"], 70,72,68,70,74,72,70,66,68,64,70, 3,3,3,3,2,1),
        ("Amit Joshi",        "amit.joshi@demo.edu",        "MECH","a1000000-0000-0000-0000-000000000007", 6.2, 65, 68, 42,38,45,40,30,28,52, ["C","MATLAB"],          38,42,45,40,48,40,44,38,40,32,52, 1,1,1,1,0,0),
        ("Kavya Nambiar",     "kavya.nambiar@demo.edu",     "IT",  "a1000000-0000-0000-0000-000000000004", 8.6, 91, 93, 85,82,78,85,90,72,82, ["React","Vue","TypeScript"], 82,85,78,85,85,85,80,82,85,80,82, 4,4,4,5,2,2),
        ("Siddharth Bose",    "siddharth.bose@demo.edu",    "CS",  "a1000000-0000-0000-0000-000000000006", 7.5, 80, 82, 70,68,72,68,65,60,68, ["Python","NumPy","Pandas"], 68,70,72,68,72,70,74,65,68,62,68, 3,3,3,3,1,1),
        ("Harini Venkatesan", "harini.venkatesan@demo.edu", "IT",  "a1000000-0000-0000-0000-000000000003", 8.9, 93, 95, 88,86,84,87,80,78,85, ["Java","Spring Boot","PostgreSQL"], 86,88,84,87,88,88,86,85,86,82,85, 5,5,5,5,3,2),
        ("Nikhil Tiwari",     "nikhil.tiwari@demo.edu",     "CS",  "a1000000-0000-0000-0000-000000000001", 7.1, 77, 79, 62,60,58,62,55,50,62, ["C++","Java"],          60,62,58,62,62,62,60,55,58,52,62, 2,2,2,2,1,0),
    ]

    pw_hash = hash_password("Student@123!")

    for i, row in enumerate(students_data):
        (name, email, dept, role_id, cgpa, tenth, twelfth,
         sp, sd, sdb, soop, sweb, sai, scomm, langs,
         dsa,prog,dbms,oop,apt,cod,tech,intv,res,lc,comms,
         dsa_o,dbms_o,apt_o,cod_o,intv_o,res_o) = row

        uid = f"c000000{i:02d}-0000-0000-0000-000000000000"
        sid = f"d000000{i:02d}-0000-0000-0000-000000000000"
        uid = f"c{i+1:07d}-0001-0001-0001-000000000001"
        sid = f"d{i+1:07d}-0001-0001-0001-000000000001"

        u = User(id=uid, email=email, hashed_password=pw_hash, full_name=name, role=UserRole.student, is_demo=True)
        db.add(u)
        db.flush()

        s = Student(id=sid, user_id=uid, college="Demo Engineering College", department=dept,
                    batch="2024", year=4, cgpa=cgpa, tenth_percent=tenth, twelfth_percent=twelfth,
                    skill_programming=sp, skill_dsa=sd, skill_dbms=sdb, skill_oop=soop,
                    skill_web_dev=sweb, skill_aiml=sai, skill_communication=scomm,
                    programming_languages=langs, target_role_id=role_id, profile_completeness=80)
        db.add(s)
        db.flush()

        sp_obj = SkillProfile(student_id=sid,
            dsa_score=dsa, programming_score=prog, dbms_score=dbms, oop_score=oop,
            aptitude_score=apt, coding_score=cod, technical_score=tech,
            interview_score=intv, resume_score=res, leetcode_score=lc,
            communication_score=comms, web_dev_score=sweb, aiml_score=sai,
            dsa_observations=dsa_o, dbms_observations=dbms_o, aptitude_observations=apt_o,
            coding_observations=cod_o, interview_observations=intv_o, resume_observations=res_o)
        db.add(sp_obj)

        lc_vals = [145,98,210,45,128,72,285,28,195,88,155,52,178,105,138,18,220,122,265,80]
        easy_v  = [65,55,80,30,58,40,90,20,75,48,65,35,70,52,60,15,82,55,85,45]
        med_v   = [62,35,95,12,55,25,130,7,85,32,70,14,78,42,62,3,100,52,120,28]
        hard_v  = [18,8,35,3,15,7,65,1,35,8,20,3,30,11,16,0,38,15,60,7]
        lc_prog = LeetCodeProgress(student_id=sid, leetcode_username=f"{name.split()[0].lower()}_demo",
            total_solved=lc_vals[i], easy_solved=easy_v[i], medium_solved=med_v[i], hard_solved=hard_v[i],
            acceptance_rate=55+i*0.8, contest_rating=1300+i*35, is_demo_data=True)
        db.add(lc_prog)

    # ── Assessment Questions ────────────────────────────────────────────────────
    apt_qs = [
        ("aptitude","Quantitative","A train travels 360 km in 4 hours. Speed in m/s?","20 m/s","25 m/s","30 m/s","22.5 m/s","B","Speed=360/4=90km/h=25m/s","easy"),
        ("aptitude","Quantitative","8 workers finish in 12 days. 6 workers take?","14","16","18","20","B","8×12=96; 96/6=16","easy"),
        ("aptitude","Quantitative","15% of 480?","66","72","76","78","B","15/100×480=72","easy"),
        ("aptitude","Quantitative","Markup 40%, discount 20%. Net profit?","10%","12%","14%","8%","B","1.4×0.8=1.12→12%","medium"),
        ("aptitude","Logical","Next: 2,6,12,20,30,?","40","42","44","46","B","Differences:4,6,8,10,12→42","easy"),
        ("aptitude","Logical","All Bloops are Razzles, all Razzles are Lazzles. All Bloops are?","Not Lazzles","Lazzles","Not Razzles","None","B","Transitive relation","easy"),
        ("aptitude","Verbal","Opposite of ENIGMATIC?","Mysterious","Clear","Cryptic","Puzzling","B","Enigmatic=mysterious; opposite=clear","easy"),
        ("aptitude","Quantitative","SI on Rs.8000 at 5% for 3 years?","Rs.1200","Rs.1000","Rs.1400","Rs.1600","A","SI=8000×5×3/100=1200","easy"),
        ("aptitude","Logical","Series: ACE,BDF,CEG,?","DFH","DEF","EFG","DGH","A","Each letter +1","easy"),
        ("aptitude","Quantitative","CI on Rs.10000 at 10% for 2 years?","Rs.2000","Rs.2100","Rs.2200","Rs.1900","B","10000×1.1²-10000=2100","medium"),
        ("aptitude","Quantitative","√(0.0256)?","0.16","0.016","1.6","0.6","A","√(256/10000)=16/100=0.16","easy"),
        ("aptitude","Verbal","Odd one out: Laptop,Keyboard,Monitor,Mouse,Hard disk","Laptop","Keyboard","Monitor","Mouse","A","Laptop is complete system","easy"),
        ("aptitude","Quantitative","A:B age ratio 3:5. After 10 years 5:7. A's age?","15","20","25","10","A","3x+10/5x+10=5/7→x=5,A=15","medium"),
        ("aptitude","Logical","A is taller than B, C shorter than A, D taller than C but shorter than B. Shortest?","A","B","C","D","C","A>B>D>C→C","medium"),
        ("aptitude","Quantitative","Man walks 5km/h, runs 10km/h, covers 50km in 7 hours. Ran?","30 km","20 km","25 km","35 km","A","x/5+(50-x)/10=7→run=30","medium"),
    ]
    tech_qs = [
        ("technical","DBMS","Which normal form eliminates partial dependencies?","1NF","2NF","3NF","BCNF","B","2NF removes partial dependencies","easy"),
        ("technical","DBMS","ACID stands for?","Atomicity,Consistency,Isolation,Durability","Availability,Consistency,Isolation,Durability","Atomicity,Concurrency,Isolation,Durability","Atomicity,Consistency,Integration,Durability","A","ACID ensures reliable DB transactions","easy"),
        ("technical","DBMS","Which JOIN returns all rows from both tables?","INNER JOIN","LEFT JOIN","RIGHT JOIN","FULL OUTER JOIN","D","FULL OUTER JOIN returns all rows","easy"),
        ("technical","DBMS","Purpose of GROUP BY?","Sort rows","Filter rows","Group rows for aggregates","Join tables","C","GROUP BY groups for aggregate operations","easy"),
        ("technical","OOP","Which OOP principle hides implementation?","Inheritance","Polymorphism","Encapsulation","Abstraction","C","Encapsulation hides internal state","easy"),
        ("technical","OOP","Method overloading means?","Redefine parent method","Same name different params","Method calling itself","None","B","Overloading=same name,different signatures","easy"),
        ("technical","OOP","Which pattern ensures single instance?","Factory","Observer","Singleton","Strategy","C","Singleton restricts to one object","medium"),
        ("technical","Networking","HTTP 404 means?","Server Error","Unauthorized","Not Found","Bad Request","C","404=resource not found","easy"),
        ("technical","OS","Semaphore used for?","Memory mgmt","Process sync","File handling","CPU scheduling","B","Semaphores control shared resource access","medium"),
        ("technical","DBMS","HAVING clause does?","Filter before group","Filter after GROUP BY","Join tables","Sort results","B","HAVING filters groups after GROUP BY","medium"),
        ("technical","DBMS","TRUNCATE vs DELETE?","Same","TRUNCATE is faster, no row log","DELETE is faster","TRUNCATE logs rows","B","TRUNCATE removes all rows without row-level logging","easy"),
        ("technical","OOP","Liskov Substitution Principle?","Single responsibility","Subtypes substitutable for base","Depend on abstractions","Open-closed","B","LSP: subtypes must be substitutable","medium"),
        ("technical","Networking","DNS purpose?","Encrypt data","Translate domains to IPs","Assign IPs","Route packets","B","DNS=Domain Name System","easy"),
        ("technical","OS","Virtual memory?","Physical RAM","Disk used as RAM extension","Cache","GPU memory","B","Virtual memory extends RAM using disk","easy"),
        ("technical","DBMS","Foreign key?","Primary key in same table","References PK of another table","Composite key","Unique constraint","B","Foreign key enforces referential integrity","easy"),
    ]
    coding_qs = [
        ("coding","Arrays","Binary search time complexity?","O(n)","O(log n)","O(n log n)","O(1)","B","Binary search halves search space","easy"),
        ("coding","Sorting","Best average-case sorting algorithm?","Bubble Sort","Selection Sort","Merge Sort","Insertion Sort","C","Merge Sort is O(n log n) always","easy"),
        ("coding","Data Structures","Stack uses which order?","Queue-like","LIFO","FIFO","Random","B","Stack=Last-In First-Out","easy"),
        ("coding","Graphs","BFS uses?","Stack","Priority Queue","Queue","Array","C","BFS uses Queue for level-by-level traversal","easy"),
        ("coding","Dynamic Programming","Fibonacci DP time complexity?","O(2^n)","O(n)","O(n log n)","O(n²)","B","Bottom-up DP is O(n)","medium"),
        ("coding","Trees","Balanced BST height with n nodes?","O(n)","O(log n)","O(n²)","O(1)","B","Balanced BST height=O(log n)","easy"),
        ("coding","Hashing","Average HashMap get/put complexity?","O(n)","O(log n)","O(1)","O(n log n)","C","HashMap uses hash for O(1) average","easy"),
        ("coding","Dynamic Programming","0/1 Knapsack time complexity?","O(n)","O(n×W)","O(W)","O(2^n)","B","DP table is O(n×W)","medium"),
        ("coding","Trees","BST inorder gives?","Random","Sorted ascending","Sorted descending","Level order","B","Inorder(L,Root,R) on BST=sorted","easy"),
        ("coding","Graphs","Shortest path non-negative weights?","BFS","DFS","Dijkstra","Bellman-Ford","C","Dijkstra for non-negative weights","medium"),
        ("coding","Arrays","Two-pointer technique best for?","Max element","Pair with target sum","Sorting","Counting","B","Two-pointer finds pairs in O(n) on sorted array","medium"),
        ("coding","Sorting","QuickSort worst case?","O(n log n)","O(n)","O(n²)","O(n³)","C","Worst case O(n²) when pivot always min/max","medium"),
        ("coding","Greedy","Activity selection uses?","DP","Greedy (earliest finish)","Divide & Conquer","Backtracking","B","Greedy: select activity with earliest finish","medium"),
        ("coding","Backtracking","N-Queens uses?","Greedy","BFS","Backtracking","DP","C","N-Queens uses systematic backtracking","medium"),
        ("coding","Arrays","Merge Sort space complexity?","O(1)","O(log n)","O(n)","O(n log n)","C","Merge Sort needs O(n) auxiliary space","medium"),
    ]

    for qs in [apt_qs, tech_qs, coding_qs]:
        for q in qs:
            atype, topic, qtext, a, b, c, d, correct, expl, diff = q
            db.add(AssessmentQuestion(
                assessment_type=AssessmentType(atype), topic=topic, question_text=qtext,
                option_a=a, option_b=b, option_c=c, option_d=d,
                correct_option=correct, explanation=expl, difficulty=DifficultyLevel(diff)
            ))

    db.commit()
    print(f"✅ Seeded: 1 admin, {len(students_data)} demo students, {len(apt_qs)+len(tech_qs)+len(coding_qs)} questions, {len(roles_data)} job roles")

if __name__ == "__main__":
    seed()
    db.close()
