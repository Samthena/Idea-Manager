from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Ideas.db'
db.init_app(app)

class Idea(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(1000), nullable=False)
    client = db.Column(db.String(100), nullable=False)
    meeting_date = db.Column(db.DateTime, nullable=False)
    owner = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(30), nullable=False, default='Нова')
    priority = db.Column(db.String(30), nullable=False, default='Няма')
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    @property
    def unique_id(self):
        return self.id

    def __repr__(self):
        return '<Idea %r>' % self.id


@app.route('/', methods=['POST','GET'])
def index():
    if request.method == 'POST':
        title = request.form['title'].strip()
        description = request.form['description']
        client = request.form['client']
        meeting_date = request.form['meeting_date']
        owner = request.form['owner']
        priority = request.form.get('priority', 'Няма')
        status = request.form.get('status', 'Нова')

        if not title:
            return ('Title is required', 400)

        meeting_date = datetime.strptime(request.form['meeting_date'], "%Y-%m-%dT%H:%M")

        existing_ids = {t.id for t in Idea.query.all()}
        new_unique_id = 1
        while new_unique_id in existing_ids:
            new_unique_id += 1
        
        new_idea = Idea(
            title=title,
            description=description,
            client=client,
            meeting_date=meeting_date,
            owner=owner,
            priority=priority,
            status=status,
            id=new_unique_id
        )

        
        try:
            db.session.add(new_idea)
            db.session.commit()
            return redirect(url_for('index'))
        except Exception as e:
            return f"There was an issue adding your idea: {e}"

    ideas = Idea.query.order_by(Idea.date_created.desc()).all()
    return render_template('List.html', ideas=ideas, tasks=ideas)


@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Idea.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except Exception as e:
        return f"There was a problem deleting that idea: {e}"


@app.route('/confirm_delete/<int:id>')
def confirm_delete(id):
    idea = Idea.query.get_or_404(id)
    return render_template('confirm_delete.html', idea=idea)


@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('q', '').strip()
    priority = request.args.get('priority', '')

    ideas = Idea.query

    if query:
        try:
            uid = int(query)
        except ValueError:
            uid = None

        ideas = ideas.filter(
            (Idea.title.ilike(f"%{query}%")) |
            (Idea.description.ilike(f"%{query}%")) |
            (Idea.client.ilike(f"%{query}%")) |
            (Idea.owner.ilike(f"%{query}%")) |
            (Idea.id == uid)
        )

    if priority:
        ideas = ideas.filter(Idea.priority == priority)

    ideas = ideas.order_by(Idea.date_created.desc()).all()

    return render_template(
        'search.html',
        ideas=ideas,
        tasks=ideas,
        query=query,
        priority=priority
    )

    
@app.route('/filter')
def filter_tasks():
    status = request.args.get('status') or request.form.get('status')
    priority = request.args.get('priority') or request.form.get('priority')
    client = request.args.get('client') or request.form.get('client')
    owner = request.args.get('owner') or request.form.get('owner')

    query = Idea.query

    if status:
        query = query.filter(Idea.status == status)
    if priority:
        query = query.filter(Idea.priority == priority)
    if client:
        query = query.filter(Idea.client == client)
    if owner:
        query = query.filter(Idea.owner == owner)

    ideas = query.order_by(Idea.date_created.desc()).all()

    return render_template(
        'List.html',
        ideas=ideas,
        tasks=ideas,
        status=status,
        client=client,
        owner=owner,
        priority=priority
     )


@app.route('/update/<int:id>', methods = ['POST', 'GET'])
def update(id):
    task = Idea.query.get_or_404(id)
    
    if request.method == 'POST':
        task.title = request.form['title']
        task.description = request.form['description']
        task.client = request.form['client']

        task.meeting_date = datetime.strptime(request.form['meeting_date'], "%Y-%m-%dT%H:%M")

        task.owner = request.form['owner']
        task.status = request.form['status']
        task.priority = request.form.get('priority', 'Няма')
        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue updating the idea'
    else:
        # Editing happens through the modal on the list page (POST only);
        # there's no standalone update page, so just send GETs back there.
        return redirect(url_for('index'))

@app.route("/update-priority/<int:id>", methods=["POST"])
def update_priority(id):
    idea = Idea.query.get_or_404(id)

    idea.priority = request.form["priority"]

    db.session.commit()

    return redirect(request.referrer or url_for("index"))

@app.route('/idea/<int:id>')
def idea_details(id):
    idea = Idea.query.get_or_404(id)
    return render_template('idea_details.html', idea=idea)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)