"""
GenAI Recommendation Engine
Uses Google Gemini when available; falls back to deterministic demo recommendations.
IMPORTANT: Recommendations are generated based on actual student skill data.
           Do NOT generate generic advice when specific data is available.
"""
import os
from typing import Dict, List, Optional
from ..config import get_settings

settings = get_settings()


def generate_recommendations(
    student_name: str,
    skill_profile: Dict[str, float],
    skill_gaps: List[Dict],
    readiness_category: str,
    job_role_name: str,
    positive_factors: List[Dict],
    negative_factors: List[Dict],
) -> Dict:
    """
    Generate personalized recommendations using Gemini or demo fallback.
    Returns structured recommendation data.
    """
    if settings.genai_mode == "real" and settings.gemini_api_key:
        try:
            return _gemini_recommendations(
                student_name, skill_profile, skill_gaps,
                readiness_category, job_role_name, positive_factors, negative_factors
            )
        except Exception as e:
            print(f"[GenAI] Gemini call failed: {e}. Falling back to demo.")

    return _demo_recommendations(
        student_name, skill_profile, skill_gaps,
        readiness_category, job_role_name, positive_factors, negative_factors
    )


def _gemini_recommendations(
    student_name, skill_profile, skill_gaps,
    readiness_category, job_role_name, positive_factors, negative_factors
) -> Dict:
    import google.generativeai as genai
    genai.configure(api_key=settings.gemini_api_key)
    model = genai.GenerativeModel("gemini-pro")

    top_gaps = sorted(skill_gaps, key=lambda x: x.get("gap", 0), reverse=True)[:4]
    strengths = [f["label"] for f in positive_factors[:3]]
    weaknesses = [f["label"] for f in negative_factors[:3]]

    prompt = f"""You are an expert placement preparation coach. Generate a detailed, personalized recommendation for the following student.

Student: {student_name}
Target Role: {job_role_name}
Current Readiness: {readiness_category}

Skill Scores:
{_format_skills(skill_profile)}

Top Skill Gaps (most critical first):
{_format_gaps(top_gaps)}

Strengths: {', '.join(strengths)}
Areas needing improvement: {', '.join(weaknesses)}

Generate a JSON response with these exact keys:
{{
  "summary": "2-3 sentence personalized summary mentioning specific scores",
  "weekly_plan": [
    {{"week": 1, "focus": "skill name", "tasks": ["task1", "task2", "task3"], "goal": "measurable goal"}}
  ],
  "skill_actions": [
    {{"skill": "skill name", "current_score": 0, "target_score": 0, "why_matters": "...", "what_to_learn": ["topic1"], "practice": "specific practice", "priority": 1}}
  ],
  "resources": [
    {{"title": "...", "type": "course/book/platform", "url": "...", "skill": "..."}}
  ],
  "next_steps": ["immediate action 1", "immediate action 2", "immediate action 3"]
}}

Be SPECIFIC. Mention actual scores. Do NOT give generic advice."""

    response = model.generate_content(prompt)
    text = response.text.strip()
    # Clean JSON from markdown code blocks
    if "```json" in text:
        text = text.split("```json")[1].split("```")[0].strip()
    elif "```" in text:
        text = text.split("```")[1].split("```")[0].strip()

    import json
    data = json.loads(text)
    data["is_demo"] = False
    data["generated_by"] = "gemini"
    return data


def _demo_recommendations(
    student_name, skill_profile, skill_gaps,
    readiness_category, job_role_name, positive_factors, negative_factors
) -> Dict:
    """
    Deterministic, data-driven demo recommendations.
    Based on ACTUAL student scores — not generic advice.
    Clearly labelled as demo output.
    """
    top_gaps = sorted(skill_gaps, key=lambda x: x.get("gap", 0), reverse=True)[:4]
    strengths_list = [f.get("label", f.get("feature", "")) for f in positive_factors[:3]]
    weak_list = [g["skill_name"].upper() for g in top_gaps[:3]]

    # Build summary from actual data
    strong_str = ", ".join(strengths_list) if strengths_list else "some areas"
    weak_str = ", ".join(weak_list) if weak_list else "several areas"

    aptitude = skill_profile.get("aptitude_score", 0)
    interview = skill_profile.get("interview_score", 0)
    dsa = skill_profile.get("dsa_score", 0)
    dbms = skill_profile.get("dbms_score", 0)
    coding = skill_profile.get("coding_score", 0)

    summary = (
        f"Based on your current profile, {student_name}, your readiness for {job_role_name} is "
        f"'{readiness_category}'. "
        f"Your strongest areas are {strong_str}, while {weak_str} need the most attention. "
        f"Following this personalised plan consistently for 4 weeks should raise your readiness significantly."
    )

    # Skill-specific actions based on actual scores
    skill_actions = []
    resource_map = {
        "dsa": {
            "what_to_learn": ["Arrays & Strings", "Trees & Graphs", "Dynamic Programming", "Sliding Window"],
            "practice": "Solve 10 LeetCode problems per week (4 easy, 5 medium, 1 hard)",
            "resource": {"title": "LeetCode DSA Study Plan", "type": "platform", "url": "https://leetcode.com/study-plan/data-structure/", "skill": "DSA"},
        },
        "dbms": {
            "what_to_learn": ["SQL Joins & Subqueries", "Normalization (1NF–BCNF)", "Indexing & Query Optimization", "Transactions & ACID"],
            "practice": "Complete 10 SQL problems on HackerRank this week",
            "resource": {"title": "SQLZoo Interactive Tutorials", "type": "platform", "url": "https://sqlzoo.net", "skill": "DBMS"},
        },
        "aptitude": {
            "what_to_learn": ["Quantitative Aptitude: Percentages, Ratios", "Logical Reasoning patterns", "Data Interpretation"],
            "practice": "Practice 20 aptitude questions daily on IndiaBix",
            "resource": {"title": "IndiaBix Aptitude Practice", "type": "platform", "url": "https://indiabix.com", "skill": "Aptitude"},
        },
        "interview": {
            "what_to_learn": ["STAR method for behavioral questions", "Technical HR questions for your role", "Communication & clarity techniques"],
            "practice": "Practice 3 mock interview questions per day; record yourself",
            "resource": {"title": "Pramp Mock Interviews", "type": "platform", "url": "https://pramp.com", "skill": "Interview"},
        },
        "programming": {
            "what_to_learn": ["OOP design patterns", "Clean code principles", "Language-specific best practices"],
            "practice": "Build one small project per week applying learned concepts",
            "resource": {"title": "Refactoring Guru – Design Patterns", "type": "website", "url": "https://refactoring.guru/design-patterns", "skill": "Programming"},
        },
        "resume": {
            "what_to_learn": ["ATS-friendly formatting", "Action-oriented bullet points", "Quantifying achievements"],
            "practice": "Revise resume to include measurable impact for each project",
            "resource": {"title": "Resume Worded Analyzer", "type": "tool", "url": "https://resumeworded.com", "skill": "Resume"},
        },
        "leetcode": {
            "what_to_learn": ["Two Pointers", "Binary Search patterns", "HashMap-based optimisation"],
            "practice": "Commit to 1 LeetCode problem every day; review solutions after attempting",
            "resource": {"title": "NeetCode 150", "type": "course", "url": "https://neetcode.io", "skill": "LeetCode"},
        },
        "oop": {
            "what_to_learn": ["SOLID principles", "Design Patterns (Factory, Observer, Singleton)", "Abstraction & polymorphism"],
            "practice": "Implement 5 design patterns from scratch this week",
            "resource": {"title": "Head First Design Patterns", "type": "book", "url": "https://www.oreilly.com/library/view/head-first-design/0596007124/", "skill": "OOP"},
        },
        "web_dev": {
            "what_to_learn": ["React component lifecycle", "REST API design", "CSS layout (Flexbox/Grid)"],
            "practice": "Build a full-stack mini-app with React + Node.js",
            "resource": {"title": "The Odin Project", "type": "course", "url": "https://www.theodinproject.com", "skill": "Web Dev"},
        },
        "aiml": {
            "what_to_learn": ["Supervised vs Unsupervised learning", "sklearn pipeline", "Model evaluation metrics"],
            "practice": "Complete one Kaggle beginner competition this week",
            "resource": {"title": "Fast.ai Practical Deep Learning", "type": "course", "url": "https://course.fast.ai", "skill": "AI/ML"},
        },
    }

    resources = []
    for i, gap in enumerate(top_gaps[:4]):
        sname = gap["skill_name"].lower()
        info = resource_map.get(sname, {
            "what_to_learn": [f"Core {sname} concepts", f"Advanced {sname} topics"],
            "practice": f"Practice {sname} for 1 hour daily",
            "resource": {"title": f"{sname.title()} Study Resources", "type": "general", "url": "https://developer.mozilla.org", "skill": sname},
        })
        current = round(gap.get("student_score", 0), 1)
        required = round(gap.get("required_score", 0), 1)

        skill_actions.append({
            "skill": sname,
            "skill_label": sname.upper(),
            "current_score": current,
            "target_score": required,
            "gap": round(gap.get("gap", 0), 1),
            "why_matters": f"Your {sname.upper()} score ({current}) is {gap.get('gap',0):.0f} points below the required {required} for {job_role_name}.",
            "what_to_learn": info["what_to_learn"],
            "practice": info["practice"],
            "priority": gap.get("priority", i + 1),
            "confidence": gap.get("confidence", "Medium"),
            "observations": gap.get("observations", 0),
        })

        if info["resource"] not in resources:
            resources.append(info["resource"])

    # Weekly plan
    focus_skills = [g["skill_name"].upper() for g in top_gaps[:4]]
    weekly_plan = []
    week_templates = [
        {"focus": focus_skills[0] if focus_skills else "Core Skills",
         "tasks": [f"Study {focus_skills[0] if focus_skills else 'core'} fundamentals 2h/day",
                   f"Solve 8-10 practice problems",
                   f"Take PlacePilot {(focus_skills[0] if focus_skills else 'coding').lower()} test"],
         "goal": f"Raise {focus_skills[0] if focus_skills else 'core'} score by 10 points"},
        {"focus": focus_skills[1] if len(focus_skills) > 1 else "Interview Prep",
         "tasks": [f"Deep dive into {focus_skills[1] if len(focus_skills) > 1 else 'interview'} concepts",
                   "Practice 3 mock interview questions daily",
                   "Review weak areas from Week 1 assessment"],
         "goal": f"Complete all {(focus_skills[1] if len(focus_skills) > 1 else 'interview').lower()} topic modules"},
        {"focus": "Mixed Practice",
         "tasks": ["Combined assessment across all weak skills",
                   "Revise and update your resume",
                   "Attempt 15 LeetCode problems"],
         "goal": "Score ≥70 on PlacePilot mock tests"},
        {"focus": "Final Readiness Check",
         "tasks": ["Full mock assessment in PlacePilot",
                   "Recalculate readiness score",
                   "Review AI recommendations progress"],
         "goal": f"Achieve 'Moderately Ready' or better for {job_role_name}"},
    ]
    for i, tmpl in enumerate(week_templates):
        weekly_plan.append({"week": i + 1, **tmpl})

    next_steps = [
        f"Take the {'aptitude' if aptitude < 70 else 'technical'} assessment in PlacePilot today to get updated scores",
        f"Start with {top_gaps[0]['skill_name'].upper() if top_gaps else 'DSA'} — it has the largest gap",
        "Update your LeetCode progress after every 5 problems solved",
        "Upload an updated resume for re-analysis",
        "Schedule a mock interview session this week",
    ]

    return {
        "summary": summary,
        "weekly_plan": weekly_plan,
        "skill_actions": skill_actions,
        "resources": resources[:6],
        "next_steps": next_steps,
        "is_demo": True,
        "generated_by": "demo-engine",
    }


def _format_skills(profile: Dict) -> str:
    lines = []
    for k, v in profile.items():
        lines.append(f"  {k.replace('_score','').upper()}: {v:.1f}/100")
    return "\n".join(lines)


def _format_gaps(gaps: List) -> str:
    lines = []
    for g in gaps:
        lines.append(f"  {g['skill_name'].upper()}: {g.get('student_score',0):.1f} (need {g.get('required_score',0):.1f}, gap={g.get('gap',0):.1f})")
    return "\n".join(lines)
