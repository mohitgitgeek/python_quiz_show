# python_quiz_show
My 1st year independent project on Quiz show in Python.

## Full-stack web app (frontend + DB + backend + ML)

The original console quiz (`quiz.py`) is now a full-stack web app:

```sh
pip install -r requirements.txt
python quiz_app.py
# open http://localhost:5000
```

- **Frontend:** `index.html` — loads questions from the API and highlights correct/wrong answers.
- **Backend:** Flask (`quiz_app.py`) — serves questions, grades answers server-side, exposes a leaderboard.
- **Database:** SQLite via SQLAlchemy (`quiz.db`) storing every attempt for the leaderboard.
- **Machine Learning:** `ml.py` trains a scikit-learn **LogisticRegression** (on an Item-Response-Theory
  style simulation) that predicts a player's probability of passing (≥5/7) from their first three answers.

The frontend gracefully falls back to **in-browser grading** when no backend is detected, so the static
GitHub Pages deployment keeps working. Set `window.API_BASE` to point the static site at a hosted backend.

The original `quiz.py` console program is preserved unchanged.

## GitHub Pages

This repository now includes a static web version of the quiz at `index.html` and a GitHub Actions workflow at `.github/workflows/deploy-pages.yml` to deploy it to GitHub Pages.
