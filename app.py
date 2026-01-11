from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Config
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///winfra_data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Inventory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(200), nullable=False)
    assigned_to = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(20), default='Pending')

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    items = Inventory.query.all()
    return render_template('index.html', items=items)

@app.route('/add_item', methods=['POST'])
def add_item():
    if request.method == 'POST':
        new_item = Inventory(
            name=request.form['name'],
            category=request.form['category'],
            quantity=request.form['quantity']
        )
        db.session.add(new_item)
        db.session.commit()
    return redirect(url_for('index'))

@app.route('/delete_item/<int:id>')
def delete_item(id):
    item = Inventory.query.get_or_404(id)
    db.session.delete(item)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/tasks')
def tasks():
    tasks = Task.query.all()
    return render_template('tasks.html', tasks=tasks)

@app.route('/add_task', methods=['POST'])
def add_task():
    if request.method == 'POST':
        new_task = Task(
            description=request.form['description'],
            assigned_to=request.form['assigned_to']
        )
        db.session.add(new_task)
        db.session.commit()
    return redirect(url_for('tasks'))

@app.route('/complete_task/<int:id>')
def complete_task(id):
    task = Task.query.get_or_404(id)
    task.status = 'Completed'
    db.session.commit()
    return redirect(url_for('tasks'))

if __name__ == "__main__":
    app.run(debug=True)