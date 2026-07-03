from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "super_secret_key_123456"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# 数据库模型
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(50))

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    student_id = db.Column(db.String(20), unique=True)
    score = db.Column(db.Float)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)

# 初始化数据库
with app.app_context():
    db.create_all()
    if not Student.query.first():
        students = [
            Student(name="张三", student_id="2025001", score=92.5),
            Student(name="李四", student_id="2025002", score=85.0),
            Student(name="王五", student_id="2025003", score=78.0),
            Student(name="赵六", student_id="2025004", score=96.0)
        ]
        db.session.add_all(students)
        db.session.commit()

# 登录
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username, password=password).first()
        if user:
            return redirect(url_for('dashboard'))
        flash("用户名或密码错误")
    return render_template('login.html')

# 注册
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if not User.query.filter_by(username=username).first():
            user = User(username=username, password=password)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('login'))
        flash("用户名已存在")
    return render_template('register.html')

# 学生列表
@app.route('/dashboard')
def dashboard():
    students = Student.query.all()
    return render_template('dashboard.html', students=students)

# 添加学生
@app.route('/add', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        name = request.form['name']
        student_id = request.form['student_id']
        score = float(request.form['score'])
        new_student = Student(name=name, student_id=student_id, score=score)
        db.session.add(new_student)
        db.session.commit()
        return redirect(url_for('dashboard'))
    return render_template('add.html')

# 编辑学生
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    student = Student.query.get_or_404(id)
    if request.method == 'POST':
        student.name = request.form['name']
        student.student_id = request.form['student_id']
        student.score = float(request.form['score'])
        db.session.commit()
        return redirect(url_for('dashboard'))
    return render_template('edit.html', student=student)

# 删除学生
@app.route('/delete/<int:id>')
def delete(id):
    student = Student.query.get_or_404(id)
    db.session.delete(student)
    db.session.commit()
    return redirect(url_for('dashboard'))

# 首页
@app.route('/')
def index():
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run()

