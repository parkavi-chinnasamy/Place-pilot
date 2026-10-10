"""
AI Mock Interview Service
Generates questions and evaluates answers using Gemini or demo fallback.
"""
from typing import Dict, List
from ..config import get_settings

settings = get_settings()

INTERVIEW_QUESTIONS = {
    "Software Developer": [
        {"q": "Explain the difference between an array and a linked list. When would you prefer one over the other?", "topic": "DSA"},
        {"q": "What is the time complexity of QuickSort and when does it degrade to O(n²)?", "topic": "DSA"},
        {"q": "Explain SOLID principles with a brief example of each.", "topic": "OOP"},
        {"q": "What is a deadlock? How can it be prevented in multi-threaded programs?", "topic": "OS/Concurrency"},
        {"q": "Describe the difference between SQL INNER JOIN and LEFT JOIN with an example.", "topic": "DBMS"},
        {"q": "Walk me through how you would design a URL shortener system.", "topic": "System Design"},
        {"q": "What is REST? What are the key principles of a RESTful API?", "topic": "Web/API"},
        {"q": "Explain how garbage collection works in Java or Python.", "topic": "Programming"},
    ],
    "Full Stack Developer": [
        {"q": "Explain the React component lifecycle. What are the key hooks you use?", "topic": "Frontend"},
        {"q": "What is the difference between authentication and authorization?", "topic": "Security"},
        {"q": "How would you optimize a slow database query?", "topic": "DBMS"},
        {"q": "Explain CORS. How do you handle it in a Node.js/Express application?", "topic": "Web"},
        {"q": "What is the Virtual DOM in React and how does it improve performance?", "topic": "Frontend"},
        {"q": "Explain RESTful API design best practices.", "topic": "Backend"},
        {"q": "How do you handle state management in large React applications?", "topic": "Frontend"},
        {"q": "What is Docker and how does containerisation help in development?", "topic": "DevOps"},
    ],
    "Data Analyst": [
        {"q": "Explain the difference between GROUP BY and HAVING in SQL.", "topic": "SQL"},
        {"q": "What is normalization? Explain 1NF, 2NF, and 3NF.", "topic": "DBMS"},
        {"q": "How would you handle missing values in a dataset?", "topic": "Data Processing"},
        {"q": "Explain the difference between a bar chart and a histogram.", "topic": "Visualization"},
        {"q": "What is a window function in SQL? Give an example.", "topic": "Advanced SQL"},
        {"q": "What is the difference between correlation and causation?", "topic": "Statistics"},
        {"q": "How would you detect and handle outliers in a dataset?", "topic": "Data Quality"},
        {"q": "Explain what a pivot table is and when you'd use it.", "topic": "Analysis"},
    ],
    "AI/ML Engineer": [
        {"q": "Explain the bias-variance tradeoff in machine learning.", "topic": "ML Theory"},
        {"q": "What is overfitting? How do you prevent it?", "topic": "ML Theory"},
        {"q": "Explain the difference between supervised, unsupervised, and reinforcement learning.", "topic": "ML"},
        {"q": "What is gradient descent? Explain variants like SGD and Adam.", "topic": "Optimization"},
        {"q": "How would you handle an imbalanced dataset?", "topic": "Data Preprocessing"},
        {"q": "Explain how a Random Forest works and its advantages over a single decision tree.", "topic": "Ensemble Methods"},
        {"q": "What is cross-validation and why is it important?", "topic": "Model Evaluation"},
        {"q": "Explain the transformer architecture and its key innovation over RNNs.", "topic": "Deep Learning"},
    ],
    "default": [
        {"q": "Tell me about yourself and why you're interested in this role.", "topic": "General"},
        {"q": "Describe a challenging project you worked on and how you handled obstacles.", "topic": "Behavioral"},
        {"q": "What is object-oriented programming? Explain its four pillars.", "topic": "Programming"},
        {"q": "Explain the difference between stack and heap memory.", "topic": "Memory"},
        {"q": "What data structures would you use to implement a cache?", "topic": "DSA"},
        {"q": "How do you stay updated with new technologies?", "topic": "General"},
        {"q": "What are your greatest technical strengths and areas for improvement?", "topic": "Self-Assessment"},
        {"q": "Describe the software development lifecycle (SDLC).", "topic": "Process"},
    ],
}

DEMO_FEEDBACK_TEMPLATES = {
    "strong": {
        "technical_score": 8.0, "relevance_score": 8.5, "clarity_score": 8.0,
        "communication_score": 7.5, "completeness_score": 8.0, "overall_score": 8.0,
        "strengths": ["Clear and structured explanation", "Good use of examples", "Technically accurate"],
        "weaknesses": ["Could provide more depth in edge cases", "Mention time/space complexity trade-offs"],
    },
    "average": {
        "technical_score": 6.0, "relevance_score": 6.5, "clarity_score": 5.5,
        "communication_score": 6.0, "completeness_score": 5.5, "overall_score": 6.0,
        "strengths": ["Covered the basic concept", "Answer was relevant to the question"],
        "weaknesses": ["Explanation lacked depth", "Missing specific examples", "Could improve clarity and structure"],
    },
    "weak": {
        "technical_score": 3.5, "relevance_score": 4.0, "clarity_score": 3.0,
        "communication_score": 4.0, "completeness_score": 3.0, "overall_score": 3.5,
        "strengths": ["Attempted to answer the question"],
        "weaknesses": ["Technical knowledge needs improvement", "Answer was incomplete", "Needs clearer structure and examples"],
    },
}


def get_interview_questions(job_role_name: str, count: int = 5) -> List[Dict]:
    questions = INTERVIEW_QUESTIONS.get(job_role_name, INTERVIEW_QUESTIONS["default"])
    import random
    random.shuffle(questions)
    return questions[:count]


def evaluate_answer(
    question: str,
    answer: str,
    topic: str,
    job_role_name: str,
) -> Dict:
    """Evaluate interview answer using Gemini or demo fallback."""
    if not answer or len(answer.strip()) < 10:
        return {
            **DEMO_FEEDBACK_TEMPLATES["weak"],
            "suggested_answer": "Please provide a detailed answer to get meaningful feedback.",
            "improvement_tips": "Answer the question with specific examples and technical detail.",
            "detailed_feedback": "No substantial answer was provided.",
        }

    if settings.genai_mode == "real" and settings.gemini_api_key:
        try:
            return _gemini_evaluate(question, answer, topic, job_role_name)
        except Exception as e:
            print(f"[GenAI] Interview eval failed: {e}")

    return _demo_evaluate(question, answer, topic)


def _gemini_evaluate(question, answer, topic, job_role_name) -> Dict:
    import google.generativeai as genai
    genai.configure(api_key=settings.gemini_api_key)
    model = genai.GenerativeModel("gemini-pro")

    prompt = f"""You are an expert technical interviewer evaluating a candidate for a {job_role_name} position.

Question: {question}
Topic: {topic}
Candidate's Answer: {answer}

Evaluate and return JSON with these exact keys:
{{
  "technical_score": <0-10>,
  "relevance_score": <0-10>,
  "clarity_score": <0-10>,
  "communication_score": <0-10>,
  "completeness_score": <0-10>,
  "overall_score": <0-10>,
  "strengths": ["strength1", "strength2"],
  "weaknesses": ["weakness1", "weakness2"],
  "suggested_answer": "ideal answer in 3-5 sentences",
  "improvement_tips": "specific actionable tips",
  "detailed_feedback": "2-3 sentence detailed evaluation"
}}"""

    response = model.generate_content(prompt)
    text = response.text.strip()
    if "```json" in text:
        text = text.split("```json")[1].split("```")[0].strip()
    elif "```" in text:
        text = text.split("```")[1].split("```")[0].strip()
    import json
    return json.loads(text)


def _demo_evaluate(question: str, answer: str, topic: str) -> Dict:
    """Rule-based demo evaluator based on answer length and keywords."""
    answer_lower = answer.lower()
    word_count = len(answer.split())

    # Score based on answer quality signals
    quality_signals = {
        "example": 1, "because": 1, "for instance": 1, "such as": 1,
        "complexity": 1, "time": 1, "space": 1, "algorithm": 1,
        "data structure": 1, "design": 1, "implement": 1,
    }
    keyword_hits = sum(1 for kw in quality_signals if kw in answer_lower)

    if word_count > 80 and keyword_hits >= 3:
        template = "strong"
        suggested = _get_suggested_answer(question, topic, "comprehensive")
    elif word_count > 30 and keyword_hits >= 1:
        template = "average"
        suggested = _get_suggested_answer(question, topic, "standard")
    else:
        template = "weak"
        suggested = _get_suggested_answer(question, topic, "basic")

    fb = dict(DEMO_FEEDBACK_TEMPLATES[template])
    fb["suggested_answer"] = suggested
    fb["improvement_tips"] = _get_improvement_tip(topic, template)
    fb["detailed_feedback"] = (
        f"[Demo Feedback] Your answer for '{topic}' received an overall score of {fb['overall_score']}/10. "
        f"{'Good job! You demonstrated solid understanding.' if template=='strong' else 'You covered the basics but can go deeper.' if template=='average' else 'This area needs significant study and practice.'} "
        f"In a real interview, {'continue using examples and details.' if template=='strong' else 'add more technical depth and real examples.' if template=='average' else 'focus on learning the core concepts first.'}"
    )
    return fb


def _get_suggested_answer(question: str, topic: str, depth: str) -> str:
    suggestions = {
        "DSA": "A strong answer would define the concept clearly, compare alternatives (e.g., array vs linked list: O(1) access vs O(1) insert), state time/space complexities, and give a real-world use case.",
        "OOP": "Cover the four pillars: Encapsulation (hiding state), Abstraction (interfaces), Inheritance (reuse), Polymorphism (multiple forms). Give a brief code example for each.",
        "DBMS": "Mention the relevant concept (e.g., normalization levels), explain why it matters for data integrity, and give a concrete SQL example.",
        "Frontend": "Explain the concept, mention browser behaviour or framework specifics, and describe how it affects performance or user experience.",
        "ML Theory": "Define the concept mathematically where possible, give an intuitive explanation, and connect it to practical model behaviour.",
        "System Design": "Use the FAANG system design framework: clarify requirements, estimate scale, design data model, design APIs, choose components, discuss trade-offs.",
        "General": "Structure your answer with: brief intro about yourself/the situation, specific technical detail, and a concrete example or outcome.",
        "SQL": "Show the SQL syntax clearly, explain what each clause does, and provide a real-world scenario where you'd use it.",
    }
    return suggestions.get(topic, f"Provide a clear, structured answer that defines the concept, explains it with an example, and discusses trade-offs or best practices related to {topic}.")


def _get_improvement_tip(topic: str, template: str) -> str:
    tips = {
        "strong": f"Your {topic} answer was strong. To push further: discuss edge cases, mention performance considerations, and relate to production scenarios.",
        "average": f"For {topic}, add more depth: include time/space complexity, give a concrete code snippet or real-world example, and explain why it matters.",
        "weak": f"Start by reviewing {topic} fundamentals. Use resources like GeeksforGeeks or LeetCode Explore. Practice explaining out loud using the 'Explain to a 5-year-old' technique first, then build up to technical precision.",
    }
    return tips.get(template, f"Study {topic} more deeply and practice explaining concepts clearly with examples.")
