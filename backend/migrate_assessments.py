import sqlite3

conn = sqlite3.connect('placepilot.db')
cur = conn.cursor()

cur.execute('PRAGMA table_info(assessments)')
cols = [col[1] for col in cur.fetchall()]

new_cols = [
    ('status', "VARCHAR(20) DEFAULT 'completed'"),
    ('attempted_questions', 'INTEGER DEFAULT 0'),
    ('incorrect_answers', 'INTEGER DEFAULT 0'),
    ('unanswered_questions', 'INTEGER DEFAULT 0'),
    ('topic', 'VARCHAR(100)'),
    ('difficulty', 'VARCHAR(20)')
]

for col_name, col_type in new_cols:
    if col_name not in cols:
        cur.execute(f"ALTER TABLE assessments ADD COLUMN {col_name} {col_type}")
        print(f"Added column {col_name}")

cur.execute("UPDATE assessments SET status = 'completed' WHERE status IS NULL")
cur.execute("UPDATE assessments SET attempted_questions = total_questions WHERE attempted_questions IS NULL OR attempted_questions = 0")
cur.execute("UPDATE assessments SET incorrect_answers = total_questions - correct_answers WHERE incorrect_answers IS NULL")
cur.execute("UPDATE assessments SET unanswered_questions = 0 WHERE unanswered_questions IS NULL")

conn.commit()
cur.execute('PRAGMA table_info(assessments)')
print('Current columns in assessments:', [c[1] for c in cur.fetchall()])
conn.close()
