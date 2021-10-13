from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db = SQLAlchemy(app)

class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"

@app.route("/", methods=['GET', 'POST'])
def home():
    if request.method=='POST':
       t = request.form['title']
       d = request.form['desc']
       todo = Todo(title=t,desc=d)
       db.session.add(todo)
       db.session.commit()

    return render_template('home.html')

@app.route("/show")
def show():
    allTodo = Todo.query.all()
    return render_template('showdata.html',all_Todos=allTodo)

@app.route("/update/<int:sno>", methods=['GET', 'POST'])
def update(sno):
    if request.method=='POST':
       t = request.form['title']
       d = request.form['desc']
       todo = Todo.query.filter_by(sno=sno).first()
       todo.title = t
       todo.desc = d
       db.session.add(todo)
       db.session.commit()
       return redirect("/show")
    
    todo = Todo.query.filter_by(sno=sno).first()
    return render_template('update.html',todo=todo)

@app.route("/delete/<int:sno>")
def delete(sno):
    todo = Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect('/show')

if __name__ == "__main__":
    app.run(debug=True, port=8000)
    #if custom port needed 
    #app.run(debug=True, port=8000)