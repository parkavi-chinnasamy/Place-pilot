# PlacePilot – AI-Powered Placement Preparation Platform

## About the Project

PlacePilot is an AI-powered placement preparation platform designed to help students prepare for campus placements and technical interviews. It brings placement preparation activities into one platform, helping students understand their strengths, identify skill gaps, and improve their interview performance.

The platform combines machine learning, Generative AI, resume analysis, assessments, and personalized recommendations to provide a more structured placement preparation experience.

## Problem Statement

Students often use different platforms to prepare for placements, track coding progress, analyze resumes, and practice interviews. This makes it difficult to understand their overall placement readiness and identify the skills they need to improve.

PlacePilot addresses this problem by integrating these activities into a single platform with personalized preparation guidance and explainable readiness insights.

## Objectives

* Provide a centralized platform for placement preparation.
* Analyze student skills and assess placement readiness.
* Identify skill gaps for specific job roles.
* Analyze resumes and generate personalized interview questions.
* Conduct interactive AI-based mock interviews.
* Provide feedback and recommendations for improvement.
* Help placement officers monitor student preparation progress.

## Key Features

### 1. Student Dashboard

Displays the student's placement readiness score, assessment progress, skill gaps, and recommended learning activities.

### 2. Placement Readiness Prediction

Uses a machine learning model to estimate readiness based on available student assessment and skill data.

### 3. Explainable AI

Uses SHAP (SHapley Additive exPlanations) to explain how individual input features contribute to a model prediction.

### 4. Resume Analysis

Accepts PDF resumes and extracts text using PyMuPDF. The extracted information can be analyzed to identify skills, education, projects, and experience.

### 5. AI Mock Interview

Uses resume information to generate personalized interview questions. The planned enhanced version will support spoken questions, microphone-based answers, adaptive follow-up questions, and a virtual female interviewer.

### 6. Assessments

Supports aptitude, technical, and coding assessments to help students evaluate their preparation.

### 7. Skill Gap Analysis

Identifies areas that need improvement based on available assessment results and target job roles.

### 8. Personalized Recommendations

Uses AI-generated guidance to suggest relevant topics, practice activities, and improvement plans.

### 9. Admin Dashboard

Helps placement officers monitor student progress and identify common skill gaps across a student batch.

## Technology Stack

| Component        | Technologies                                      |
| ---------------- | ------------------------------------------------- |
| Frontend         | React.js, JavaScript, HTML, CSS                   |
| Backend          | Python, FastAPI                                   |
| Database         | SQLite for development, PostgreSQL for production |
| ORM              | SQLAlchemy                                        |
| Machine Learning | Scikit-learn, Random Forest                       |
| Explainable AI   | SHAP                                              |
| Generative AI    | Google Gemini API                                 |
| PDF Parsing      | PyMuPDF                                           |
| Authentication   | JWT and password hashing                          |
| Speech Features  | Browser Speech APIs or compatible speech services |

## System Workflow

1. The student logs in to PlacePilot.
2. Student profile and assessment information are collected.
3. The machine learning model estimates placement readiness.
4. SHAP explains the model's prediction.
5. The platform identifies skill gaps and suggests improvement activities.
6. The student uploads a resume for text extraction and analysis.
7. The AI generates resume-specific interview questions.
8. The mock interview evaluates answers and generates feedback.
9. Student progress can be reviewed through the dashboard.

## Resume Parsing Workflow

1. The student uploads a PDF resume.
2. PyMuPDF extracts selectable text from the PDF.
3. The extracted text is processed to identify relevant resume information.
4. The AI analyzes the extracted information.
5. Personalized interview questions are generated from the student's skills and projects.

Note: Scanned PDF resumes may require OCR if they do not contain selectable text.

## Project Structure

```text
PlacePilot/
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── config.py
│   │   ├── database.py
│   │   ├── models/
│   │   ├── routes/
│   │   ├── schemas/
│   │   ├── services/
│   │   ├── ml/
│   │   └── utils/
│   ├── seed_db.py
│   └── requirements.txt
│
├── frontend/
│   ├── public/
│   ├── src/
│   └── package.json
│
└── README.md
```

## Future Enhancements

* Real-time voice-based AI interviews.
* A lifelike animated female interviewer.
* Adaptive follow-up questions based on spoken answers.
* Improved handling of scanned resumes using OCR.
* Company-specific interview simulations.
* Integration with coding platforms and professional profiles.
* Enhanced placement analytics for colleges.
* Continuous updates to readiness insights as students complete assessments.

## Expected Impact

PlacePilot aims to make placement preparation more personalized, measurable, and accessible. By combining readiness analysis, explainable machine learning, resume-based interview practice, and targeted recommendations, it helps students focus on the areas that need improvement.

## Disclaimer

Placement readiness scores are estimates based on the available input data and model. They should not be interpreted as guaranteed placement outcomes or actual hiring probabilities.
