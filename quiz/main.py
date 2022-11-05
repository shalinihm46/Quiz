from flask import Flask,jsonify #import flask module
import sqlalchemy
from sqlalchemy import Table, Column, Integer, String, Text
from sqlalchemy.orm import mapper
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base



url="sqlite:///quiz.db"
engine = sqlalchemy.create_engine(url)

db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()


print("connected to database")
from sqlalchemy import Column,MetaData,Table,Text
metadata=MetaData()


class Question(Base):
    __tablename__ = 'questions'
    id=Column(Integer,primary_key=True)
    question = Column(Text)
    op1 = Column(Text)
    op2 = Column(Text)
    op3 = Column(Text)
    op4 = Column(Text)
    answer  = Column(Text)

    def __init__(self, question,op1,op2,op3,op4,answer):
        self.question = question
        self.op1 = op1
        self.op2 = op2
        self.op3 = op3
        self.op4 = op4
        self.answer = answer

    def getJson(self):
        d={
            "que":self.question,
            "ans":[self.op1,self.op2,self.op3,self.op4],
            "key":self.answer
        }
        return d


app = Flask(__name__)#create a instance of the flask web application 

@app.route("/") #takes it to the default domain page
def home():    #define the page we want on our webs
    f=open("index.html")
    text=f.read()
    f.close()
    return text 

    
    
@app.route("/question")
def sendQuestion():
        data=db_session.query(Question).all()
        q=[]
        for row in data:
            q.append(row.getJson())
        return jsonify(q)
    
    

@app.route("/answer/<op>")
def checkAnswer(op):
    if op=="1":
        d={"answer":True}
    else:
        d={"answer":False} 
    return jsonify(d)  

@app.route("/<name>")

def user(name):  #fun defination
    if name.endswith(".css") or name.endswith(".js"):
        f=open(name)
        text=f.read()
        f.close()
        return text  
    else:
        
        return f"Hello {name}" #formatted string




if(__name__ == "__main__"): #to run the flask websit
    app.run(debug=True) #this line gets the website


