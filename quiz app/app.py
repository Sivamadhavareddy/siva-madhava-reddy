from flask import Flask, render_template, request, redirect, url_for, session, flash
from config import Config
from models import db, Question, QuizAttempt, UserAnswer
from datetime import datetime, timezone
import random

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start', methods=['POST'])
def start():
    username = request.form.get('username')
    if not username:
        return redirect(url_for('index'))
    
    questions = Question.query.all()
    if not questions:
        return "No questions available in the database. Please run seed.py.", 500
        
    random.shuffle(questions) # Optional: randomize questions
    question_ids = [q.id for q in questions]
    
    attempt = QuizAttempt(username=username, total_questions=len(questions))
    db.session.add(attempt)
    db.session.commit()
    
    session['attempt_id'] = attempt.id
    session['username'] = username
    session['question_ids'] = question_ids
    session['current_index'] = 0
    
    return redirect(url_for('quiz'))

@app.route('/quiz')
def quiz():
    if 'attempt_id' not in session:
        return redirect(url_for('index'))
        
    current_index = session.get('current_index', 0)
    question_ids = session.get('question_ids', [])
    
    if current_index >= len(question_ids):
        return redirect(url_for('result'))
        
    question = Question.query.get(question_ids[current_index])
    return render_template('quiz.html', 
                           question=question, 
                           current=current_index + 1, 
                           total=len(question_ids))

@app.route('/submit', methods=['POST'])
def submit():
    if 'attempt_id' not in session:
        return redirect(url_for('index'))
        
    attempt_id = session['attempt_id']
    current_index = session['current_index']
    question_ids = session['question_ids']
    
    if current_index >= len(question_ids):
        return redirect(url_for('result'))
        
    question_id = question_ids[current_index]
    selected_option = request.form.get('option') # 'a', 'b', 'c', or 'd'
    
    question = Question.query.get(question_id)
    is_correct = (selected_option == question.correct_option) if selected_option else False
    
    answer = UserAnswer(
        attempt_id=attempt_id,
        question_id=question_id,
        selected_option=selected_option,
        is_correct=is_correct
    )
    db.session.add(answer)
    db.session.commit()
    
    session['current_index'] += 1
    
    if session['current_index'] >= len(question_ids):
        # Calculate final score
        attempt = QuizAttempt.query.get(attempt_id)
        attempt.completed_at = datetime.now(timezone.utc)
        correct_answers = UserAnswer.query.filter_by(attempt_id=attempt_id, is_correct=True).count()
        attempt.score = correct_answers
        db.session.commit()
        return redirect(url_for('result'))
        
    return redirect(url_for('quiz'))

@app.route('/result')
def result():
    if 'attempt_id' not in session:
        return redirect(url_for('index'))
        
    attempt_id = session['attempt_id']
    attempt = QuizAttempt.query.get(attempt_id)
    answers = UserAnswer.query.filter_by(attempt_id=attempt_id).all()
    
    # Pass necessary data for review
    review_data = []
    for ans in answers:
        review_data.append({
            'question': ans.question,
            'selected': ans.selected_option,
            'is_correct': ans.is_correct
        })
        
    percentage = (attempt.score / attempt.total_questions) * 100 if attempt.total_questions > 0 else 0
    passed = percentage >= 70
        
    return render_template('result.html', attempt=attempt, review_data=review_data, percentage=percentage, passed=passed)

@app.route('/leaderboard')
def leaderboard():
    top_attempts = QuizAttempt.query.filter(QuizAttempt.score.isnot(None)).order_by(QuizAttempt.score.desc(), QuizAttempt.completed_at.asc()).limit(10).all()
    return render_template('leaderboard.html', top_attempts=top_attempts)

@app.route('/certificate/<int:attempt_id>')
def certificate(attempt_id):
    attempt = QuizAttempt.query.get_or_404(attempt_id)
    percentage = (attempt.score / attempt.total_questions) * 100 if attempt.total_questions > 0 else 0
    if percentage < 70:
        return "You must pass the quiz to view this certificate.", 403
    return render_template('certificate.html', attempt=attempt, percentage=percentage)

if __name__ == '__main__':
    app.run(debug=True)
