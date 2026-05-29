"""Quiz performance ML.

Trains a scikit-learn LogisticRegression that predicts the probability a player
will *pass* the 7-question quiz (>= 5 correct) given only how they did on the
first three questions. Training data is synthetic: each simulated player has a
latent "skill", and answers each question correctly with a probability that
depends on skill vs. that question's difficulty. This is a realistic Item
Response Theory-style simulation, so the model learns a genuine signal.
"""
import numpy as np

NUM_QUESTIONS = 7
PEEK = 3            # we predict from the first 3 questions
PASS_MARK = 5

_model = None


def _simulate(n=4000, seed=7):
    rng = np.random.default_rng(seed)
    # Per-question difficulty (higher = harder).
    difficulty = np.array([-1.0, 1.2, -0.3, -0.8, 0.6, 0.9, 0.2])
    skill = rng.normal(0, 1.4, size=n)
    # P(correct) for each (player, question).
    logits = skill[:, None] - difficulty[None, :]
    probs = 1 / (1 + np.exp(-logits))
    correct = (rng.random((n, NUM_QUESTIONS)) < probs).astype(int)
    X = correct[:, :PEEK].astype(float)             # first 3 answers
    y = (correct.sum(axis=1) >= PASS_MARK).astype(int)
    return X, y


def _get_model():
    global _model
    if _model is None:
        from sklearn.linear_model import LogisticRegression
        X, y = _simulate()
        clf = LogisticRegression()
        clf.fit(X, y)
        _model = clf
    return _model


def predict_pass_probability(first_three_correct):
    """first_three_correct: list/seq of 3 ints (1 correct, 0 wrong). Returns float or None."""
    try:
        model = _get_model()
        x = np.array([list(first_three_correct[:PEEK])], dtype=float)
        if x.shape[1] < PEEK:                       # pad if fewer than 3 given
            x = np.pad(x, ((0, 0), (0, PEEK - x.shape[1])))
        return float(model.predict_proba(x)[0][1])
    except Exception:
        return None
