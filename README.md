# PSIT BCA 2nd Year — Interactive Quiz Portal

An interactive online quiz platform built for **PSIT College of Higher Education, Kanpur**
(affiliated to Chhatrapati Shahu Ji Maharaj University, Kanpur), for **BCA 2nd Year**
students.

## What's inside

- Full PSIT-branded UI (landing page, login/signup, dashboards)
- **10 CSJMU BCA 2nd Year subjects** (Semester III & IV), each with a
  **Basic** level quiz and an **Advanced** level quiz — **160 questions total**
- Live countdown timer, progress bar, and a question navigator while taking a quiz
- Student dashboard with subject filters, best score, and attempt history
- Teacher dashboard with quiz creation, share codes, and a **leaderboard**
  (ranked results, class average, highest score) per quiz

## Subjects covered

Python Programming · Operating System · Introduction to Emerging Technologies ·
Internet & Web Technology · Software Engineering · Database Management System ·
Computer Networks · Computer Graphics & Computer Vision ·
Numerical & Statistical Techniques · Soft Computing

## Run locally

```bash
python -m venv venv
source venv/bin/activate       # Windows: venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py
```

Open http://127.0.0.1:5000

The database at `instance/quiz.db` ships pre-populated, so you do **not** need to
run `init_db.py` on first run. Only run it if you intentionally want to rebuild
the seed data (this will erase any quizzes/results you've created since):

```bash
python init_db.py
```

## Demo login

| Role    | Username      | Password |
|---------|---------------|----------|
| Teacher | `bca_teacher` | `bca123` |

Students can sign up for their own account from the **Sign Up** page.
