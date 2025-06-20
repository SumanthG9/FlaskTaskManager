from flask import Flask,render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
db =SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content =db.Column(db.String(250), nullable=False)
    completed =db.Column(db.Boolean, default=False)
    date = db.Column(db.DateTime, default=datetime.now)

    def __repr__(self):
        return "<Task %r>" %self.id

@app.route('/', methods=['GET','POST'])
def index():
    if request.method == 'POST':
        task_content = request.form['content']
        new_task = Task(content=task_content)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return "There was an issue adding the task to the database"
    else:
        tasks= Task.query.order_by(Task.date).all()
        return render_template("index.html", tasks=tasks)

@app.route('/delete/<int:id>')
def delete(id):
    delete_task = Task.query.get_or_404(id)

    try:
        db.session.delete(delete_task)
        db.session.commit()
        return redirect('/')
    except:
        return "There was an error deleting the task"
    
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):  # Ensure 'id' is here
    task = Task.query.get_or_404(id) #

    if request.method == 'POST': #
        try:
            # Update the task content with the new content from the form
            task.content = request.form['content'] #
            db.session.commit() #
            return redirect('/') # Redirect to the index page after successful update
        except:
            return "There was an issue updating the task"
    else: # If it's a GET request, render the update form with existing task data
        return render_template('update.html', task=task)
    

if __name__ =="__main__":
    app.run(debug=True)