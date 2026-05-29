"""Python Quiz Show — Flask backend.

Turns the original console quiz (`quiz.py`) into a full-stack web app:
- JSON API serving questions and grading answers server-side
- SQLite leaderboard (via SQLAlchemy) storing every attempt
- ML pass-probability prediction (see ml.py)

The original `quiz.py` console program is preserved unchanged.
"""
from flask import Flask, jsonify, request, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

from ml import predict_pass_probability

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__, static_folder=BASE_DIR, static_url_path='')

db_path = os.path.join(BASE_DIR, 'quiz.db')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_path.replace('\\', '/')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

try:
    from flask_cors import CORS
    CORS(app)
except Exception:
    pass


# Question bank — answers stay server-side and are never sent to the client.
QUESTIONS = [
    {"id": "q1", "text": "Who founded Python?",
     "answers": ["guido van rossum", "guido von rossum"]},
    {"id": "q2", "text": "Enter one Python Easter Egg command",
     "answers": ["import this", "this.c", "this.s", "this.i", "this.d"]},
    {"id": "q3", "text": "Name one keyword used in exception handling",
     "answers": ["try", "except", "finally"]},
    {"id": "q4", "text": "Expand OOP",
     "answers": ["object oriented programming", "object-oriented programming"]},
    {"id": "q5", "text": "What is (24 / (8 * 1)) + 20 ?",
     "answers": ["23", "23.0"]},
    {"id": "q6", "text": "What is the sorted value of [29, 2, 11, 70]?",
     "answers": ["[2,11,29,70]", "[2, 11, 29, 70]"]},
    {"id": "q7", "text": "Which Python library is used for simple graphics and design?",
     "answers": ["turtle"]},
]
ANSWER_KEY = {q["id"]: q["answers"] for q in QUESTIONS}


class Score(db.Model):
    __tablename__ = 'scores'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False, default='Anonymous')
    score = db.Column(db.Integer, nullable=False)
    total = db.Column(db.Integer, nullable=False, default=len(QUESTIONS))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


with app.app_context():
    db.create_all()


def _normalize(v):
    return str(v or '').strip().lower().replace(' ', '')


def _grade(submitted):
    """Return (per-question correctness dict, total correct)."""
    results, correct = {}, 0
    for qid, accepted in ANSWER_KEY.items():
        got = _normalize(submitted.get(qid, ''))
        ok = any(got == _normalize(a) for a in accepted)
        results[qid] = ok
        correct += 1 if ok else 0
    return results, correct


@app.route('/api/questions')
def api_questions():
    return jsonify([{"id": q["id"], "text": q["text"]} for q in QUESTIONS])


@app.route('/api/submit', methods=['POST'])
def api_submit():
    data = request.get_json(silent=True) or {}
    name = (data.get('name') or 'Anonymous').strip()[:80] or 'Anonymous'
    submitted = data.get('answers') or {}

    results, score = _grade(submitted)

    row = Score(name=name, score=score, total=len(QUESTIONS))
    db.session.add(row)
    db.session.commit()

    # ML: how do players who got this first-3 pattern usually fare?
    first_three = [1 if results[q["id"]] else 0 for q in QUESTIONS[:3]]
    pass_prob = predict_pass_probability(first_three)

    better = Score.query.filter(Score.score > score).count()
    rank = better + 1

    return jsonify({
        'name': name,
        'score': score,
        'total': len(QUESTIONS),
        'results': results,
        'rank': rank,
        'pass_probability': round(pass_prob * 100, 1) if pass_prob is not None else None,
    })


@app.route('/api/leaderboard')
def api_leaderboard():
    rows = (Score.query.order_by(Score.score.desc(), Score.created_at.asc())
            .limit(10).all())
    return jsonify([
        {'name': r.name, 'score': r.score, 'total': r.total,
         'date': r.created_at.strftime('%Y-%m-%d %H:%M')}
        for r in rows
    ])


@app.route('/')
def index():
    return send_from_directory(BASE_DIR, 'index.html')


if __name__ == '__main__':
    port = int(os.environ.get('PORT', '5000'))
    app.run(host='0.0.0.0', port=port, debug=True)
