from flask import Flask,render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime 
app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///notes.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


class Notes(db.Model):
    sno = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(200),nullable=False)
    desc = db.Column(db.String(500),nullable=False)
    date = db.Column(db.DateTime,default=datetime.now)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"


def create_tables():
    with app.app_context():
        db.create_all()

create_tables()

@app.route('/',methods=['POST','GET'])
def Home():
    if request.method=="POST":
        notes = Notes(title=request.form['title'],desc=request.form['desc'])
        db.session.add(notes)
        db.session.commit()
    allnotes = Notes.query.all()
    return render_template('index.html',allnotes=allnotes)
    # return 'Hello, World!'

@app.route('/update/<int:sno>',methods=['POST','GET'])
def update(sno):
    if request.method=="POST":
        note = Notes.query.filter_by(sno=sno).first()
        note.title = request.form['title']
        note.desc = request.form['desc']
        note.date = datetime.now()
        db.session.add(note)
        db.session.commit()
        return redirect('/')
    note = Notes.query.filter_by(sno=sno).first()
    return render_template('update.html',note=note)

@app.route('/delete/<int:sno>')
def delete(sno):
    print("delete")
    note = Notes.query.filter_by(sno=sno).first()
    print(note)
    db.session.delete(note)
    db.session.commit()
    return redirect('/')

if __name__ =="__main__":
    app.run(debug=True,port=8000)