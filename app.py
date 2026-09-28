from flask import Flask, render_template, request, redirect, url_for, flash, session, abort
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import os
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///quiz.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    user_type = db.Column(db.String(10), nullable=False)  # 'teacher' or 'student'

class Quiz(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    questions = db.relationship('Question', backref='quiz', lazy=True, cascade="all, delete-orphan")
    share_code = db.Column(db.String(10), unique=True, nullable=True)
    timer = db.Column(db.Integer, nullable=False)  # Timer in minutes
    subject = db.Column(db.String(120), nullable=False, default="General")
    level = db.Column(db.String(20), nullable=False, default="Basic")  # 'Basic' or 'Advanced'

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'), nullable=False)
    question_text = db.Column(db.String(500), nullable=False)
    correct_answer = db.Column(db.String(500), nullable=False)
    option_a = db.Column(db.String(500), nullable=False)
    option_b = db.Column(db.String(500), nullable=False)
    option_c = db.Column(db.String(500), nullable=False)
    option_d = db.Column(db.String(500), nullable=False)

class Result(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'), nullable=False)
    score = db.Column(db.Float, nullable=False)
    date_taken = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    student = db.relationship('User', backref='results')

def init_db():
    with app.app_context():
        db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['user_type'] = user.user_type
            session['username'] = user.username
            return redirect(url_for('dashboard'))
        flash('Invalid username or password')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('user_type', None)
    session.pop('username', None)
    flash('You have been logged out.')
    return redirect(url_for('index'))

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    if session['user_type'] == 'teacher':
        quizzes = Quiz.query.filter_by(teacher_id=session['user_id']).order_by(Quiz.subject, Quiz.level).all()
        total_attempts = Result.query.join(Quiz).filter(Quiz.teacher_id == session['user_id']).count()
        return render_template('teacher_dashboard.html', quizzes=quizzes, total_attempts=total_attempts)
    else:
        quizzes = Quiz.query.order_by(Quiz.subject, Quiz.level).all()
        subjects = sorted({q.subject for q in quizzes})
        my_results = Result.query.filter_by(student_id=session['user_id']).all()
        best_score_by_quiz = {}
        attempts_by_quiz = {}
        for r in my_results:
            attempts_by_quiz[r.quiz_id] = attempts_by_quiz.get(r.quiz_id, 0) + 1
            if r.quiz_id not in best_score_by_quiz or r.score > best_score_by_quiz[r.quiz_id]:
                best_score_by_quiz[r.quiz_id] = r.score
        quizzes_attempted = len(attempts_by_quiz)
        avg_score = round(sum(best_score_by_quiz.values()) / len(best_score_by_quiz), 1) if best_score_by_quiz else 0
        return render_template(
            'student_dashboard.html',
            quizzes=quizzes,
            subjects=subjects,
            best_score_by_quiz=best_score_by_quiz,
            attempts_by_quiz=attempts_by_quiz,
            quizzes_attempted=quizzes_attempted,
            avg_score=avg_score,
        )

@app.route('/create_quiz', methods=['GET', 'POST'])
def create_quiz():
    if 'user_id' not in session or session['user_type'] != 'teacher':
        return redirect(url_for('login'))
    if request.method == 'POST':
        quiz = Quiz(
            title=request.form['title'],
            teacher_id=session['user_id'],
            timer=int(request.form['timer']),
            subject=request.form.get('subject', 'General'),
            level=request.form.get('level', 'Basic')
        )
        db.session.add(quiz)
        db.session.commit()

        # Get the number of questions from the form
        question_count = int(request.form['question_count'])
        
        # Process each question
        for i in range(question_count):
            question = Question(
                quiz_id=quiz.id,
                question_text=request.form[f'question_text_{i}'],
                correct_answer=request.form[f'correct_answer_{i}'],
                option_a=request.form[f'option_a_{i}'],
                option_b=request.form[f'option_b_{i}'],
                option_c=request.form[f'option_c_{i}'],
                option_d=request.form[f'option_d_{i}']
            )
            db.session.add(question)
        
        db.session.commit()
        flash('Quiz created successfully')
        return redirect(url_for('dashboard'))
    return render_template('create_quiz.html')


@app.route('/delete_quiz/<int:quiz_id>', methods=['POST'])
def delete_quiz(quiz_id):
    if 'user_id' not in session or session['user_type'] != 'teacher':
        return redirect(url_for('login'))
    quiz = Quiz.query.get_or_404(quiz_id)
    if quiz.teacher_id != session['user_id']:
        abort(403)
    db.session.delete(quiz)
    db.session.commit()
    flash('Quiz deleted successfully')
    return redirect(url_for('dashboard'))

@app.route('/take_quiz/<int:quiz_id>', methods=['GET', 'POST'])
def take_quiz(quiz_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    quiz = Quiz.query.get_or_404(quiz_id)
    if session['user_type'] == 'student' and request.method == 'POST':
        score = 0
        for question in quiz.questions:
            if request.form.get(f'question_{question.id}') == question.correct_answer:
                score += 1
        if len(quiz.questions) > 0:
            result = Result(student_id=session['user_id'], quiz_id=quiz_id, score=(score / len(quiz.questions)) * 100)
        else:
            result = Result(student_id=session['user_id'], quiz_id=quiz_id, score=0)
        db.session.add(result)
        db.session.commit()
        flash(f'Your score: {result.score:.2f}%')
        return redirect(url_for('dashboard'))
    return render_template('take_quiz.html', quiz=quiz)

@app.route('/view_results/<int:quiz_id>')
def view_results(quiz_id):
    if 'user_id' not in session or session['user_type'] != 'student':
        return redirect(url_for('login'))
    quiz = Quiz.query.get_or_404(quiz_id)
    results = Result.query.filter_by(student_id=session['user_id'], quiz_id=quiz_id).order_by(Result.date_taken.desc()).all()
    best_score = max((r.score for r in results), default=None)
    return render_template('quiz_results.html', quiz=quiz, results=results, is_leaderboard=False, best_score=best_score)

@app.route('/share_quiz/<int:quiz_id>')
def share_quiz(quiz_id):
    if 'user_id' not in session or session['user_type'] != 'teacher':
        return redirect(url_for('login'))
    quiz = Quiz.query.get_or_404(quiz_id)
    if quiz.teacher_id != session['user_id']:
        abort(403)
    if not quiz.share_code:
        quiz.share_code = os.urandom(5).hex()
        db.session.commit()
    return render_template('share_quiz.html', quiz=quiz)

@app.route('/join_quiz', methods=['GET', 'POST'])
def join_quiz():
    if 'user_id' not in session or session['user_type'] != 'student':
        return redirect(url_for('login'))
    if request.method == 'POST':
        share_code = request.form['share_code']
        quiz = Quiz.query.filter_by(share_code=share_code).first()
        if quiz:
            return redirect(url_for('take_quiz', quiz_id=quiz.id))
        else:
            flash('Invalid share code. Please try again.')
    return render_template('join_quiz.html')

@app.route('/quiz_results/<int:quiz_id>')
def quiz_results(quiz_id):
    if 'user_id' not in session or session['user_type'] != 'teacher':
        return redirect(url_for('login'))
    quiz = Quiz.query.get_or_404(quiz_id)
    if quiz.teacher_id != session['user_id']:
        abort(403)
    results = Result.query.filter_by(quiz_id=quiz_id).order_by(Result.score.desc(), Result.date_taken.asc()).all()
    avg_score = round(sum(r.score for r in results) / len(results), 1) if results else 0
    high_score = max((r.score for r in results), default=0)
    return render_template('quiz_results.html', quiz=quiz, results=results, is_leaderboard=True,
                            avg_score=avg_score, high_score=high_score)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user_type = request.form['user_type']
        
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username already exists. Please choose a different one.')
            return redirect(url_for('signup'))
        
        hashed_password = generate_password_hash(password)
        new_user = User(username=username, password=hashed_password, user_type=user_type)
        db.session.add(new_user)
        db.session.commit()
        
        flash('Account created successfully. Please log in.')
        return redirect(url_for('login'))
    return render_template('signup.html')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)