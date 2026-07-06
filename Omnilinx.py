from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db.init_app(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    client = db.Column(db.String(100), nullable=False)
    meeting_date = db.Column(db.DateTime, nullable=False)
    owner = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(30), nullable=False, default='Not Started')
    priority = db.Column(db.String(30), nullable=False, default='Low')
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    unique_id = db.Column(db.Integer, unique=True, nullable=False)


    def __repr__(self):
        return '<Task %r>' % self.id


@app.route('/', methods=['POST','GET'])
def index():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        client = request.form['client']
        meeting_date = request.form['meeting_date']
        owner = request.form['owner']
        status = request.form['status']
        priority = request.form['priority']


        meeting_date = datetime.strptime(request.form['meeting_date'], "%Y-%m-%dT%H:%M")

        existing_ids = {t.unique_id for t in Todo.query.all()}
        new_unique_id = 1
        while new_unique_id in existing_ids:
            new_unique_id += 1
        
        new_task = Todo(
            title=title,
            description=description,
            client=client,
            meeting_date=meeting_date,
            owner=owner,
            status=status,
            priority=priority,
            unique_id=new_unique_id
        )

        
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect(url_for('index'))
        except Exception as e:
            return f"There was an issue adding your idea: {e}"

    tasks = Todo.query.order_by(Todo.date_created.desc()).all()
    return render_template('List.html', tasks=tasks)


@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except Exception as e:
        return f"There was a problem deleting that idea: {e}"


@app.route('/confirm_delete/<int:id>')
def confirm_delete(id):
    idea = Todo.query.get_or_404(id)
    return render_template('confirm_delete.html', idea=idea)


@app.route('/search', methods=['GET']) 
def search():
    query = request.args.get('q', '').strip()

    if not query:
        return render_template('search.html', tasks=[])
    
    try:
        title = text(query)
        uid = int(query)
    except ValueError:
        title = None
        uid = None

    tasks = Todo.query.filter(
        (Todo.title.ilike(f"%{query}%")) |
        (Todo.unique_id == uid)
    ).order_by(Todo.date_created).all()

    return render_template('search.html', tasks=tasks)


@app.route('/update/<int:id>', methods = ['POST', 'GET'])
def update(id):
    task = Todo.query.get_or_404(id)
    
    if request.method == 'POST':
        task.title = request.form['title']
        task.description = request.form['description']
        task.client = request.form['client']

        task.meeting_date = datetime.strptime(request.form['meeting_date'], "%Y-%m-%dT%H:%M")

        task.owner = request.form['owner']
        task.status = request.form['status']
        task.priority = request.form['priority']
        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue updating the idea'
    else:
        return render_template('update.html', task=task)

@app.route('/idea/<int:id>')
def idea_details(id):
    idea = Todo.query.get_or_404(id)
    return render_template('idea_details.html', idea=idea)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)