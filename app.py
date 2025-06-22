# Hashir Shaikh
# CS24I1048

from flask import Flask, render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime,timezone,time

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Todo(db.Model):                                   # Todo Class containing the title , description and time of a todo
    sno = db.Column(db.Integer,primary_key = True)
    title = db.Column(db.String(200),nullable=False)
    desc = db.Column(db.String(500),nullable=False)
    date_created = db.Column(db.DateTime,default=datetime.now())

    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"
    
with app.app_context():
    db.create_all()
    
    
@app.route("/", methods = ['GET','POST'])               # home page
def hello_world():
    if request.method=='POST':

        title =   request.form['title']
        desc = request.form['desc']
        todo = Todo(title = title,desc= desc)
        db.session.add(todo)
        db.session.commit()

    allTodo = Todo.query.all()
    return render_template('index.html',allTodo=allTodo)

@app.route("/delete/<int:sno>")                 # page to delete a specifc query 
def delete(sno):
    todo = Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect('/')

@app.route("/sort")                 # page to sort the queries
def sort():
    allTodo = Todo.query.all()
    for todo in allTodo:

        todo2 = Todo.query.get((todo.sno)+1)

        if todo2!=None:
            print(todo2.date_created)            
            dt = datetime.strptime(todo.date_created.strftime("%Y-%m-%d %H:%M:%S"), "%Y-%m-%d %H:%M:%S")
            dt1 = datetime.strptime(todo2.date_created.strftime("%Y-%m-%d %H:%M:%S"), "%Y-%m-%d %H:%M:%S")

            if dt.day > dt1.day:
                #swap 
                tempt = todo.title
                todo2.title = todo.title
                todo2.title = tempt


                tempd = todo.desc
                todo.desc = todo2.desc
                todo2.desc = tempd    

                tempc = todo.date_created
                todo.date_created = todo2.date_created
                todo2.date_created = tempc
                db.session.add(todo)
                db.session.commit()
                db.session.add(todo2)
                db.session.commit()
                    
            elif dt.day==dt1.day:
                if dt.hour>dt1.hour:
                    tempt = todo.title
                    todo2.title = todo.title
                    todo2.title = tempt


                    tempd = todo.desc
                    todo.desc = todo2.desc
                    todo2.desc = tempd    

                    tempc = todo.date_created
                    todo.date_created = todo2.date_created
                    todo2.date_created = tempc
                    db.session.add(todo)
                    db.session.commit()
                    db.session.add(todo2)
                    db.session.commit()
                    #swap
                elif dt.hour==dt1.hour:
                    if dt.minute>dt1.minute:
                        tempt = todo.title
                        todo2.title = todo.title
                        todo2.title = tempt


                        tempd = todo.desc
                        todo.desc = todo2.desc
                        todo2.desc = tempd    

                        tempc = todo.date_created
                        todo.date_created = todo2.date_created
                        todo2.date_created = tempc
                        db.session.add(todo)
                        db.session.commit()
                        db.session.add(todo2)
                        db.session.commit()
                        #swap
                    
                


        
    return redirect('/')

@app.route("/pintotop/<int:sno>")                 # page to delete a specifc query 
def pintotop(sno):
    todo1 = Todo.query.filter_by(sno=sno).first()
    todo2 = Todo.query.first()
    tempt = todo1.title
    todo1.title = todo2.title
    todo2.title = tempt


    tempd = todo1.desc
    todo1.desc = todo2.desc
    todo2.desc = tempd    

    tempc = todo1.date_created
    todo1.date_created = todo2.date_created
    todo2.date_created = tempc
    db.session.add(todo1)
    db.session.commit()
    db.session.add(todo2)
    db.session.commit()
    return redirect('/')
@app.route("/update/<int:sno>",methods = ['GET',"POST"])    # page to update a specifc query 
def update(sno):
    if request.method=='POST':
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo.query.filter_by(sno=sno).first()
        todo.title = title
        todo.desc = desc
        db.session.add(todo)
        db.session.commit()
        return redirect('/')
    
    todo = Todo.query.filter_by(sno=sno).first()
    return render_template("update.html",todo=todo)

if __name__== '__main__':
    print("Starting Flask app...")
    app.run(host="127.0.0.1",debug=False)


