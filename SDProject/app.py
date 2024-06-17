from flask import Flask, jsonify, render_template, request
from flask_restful import Resource, Api
from flasgger import Swagger
import mysql.connector

app = Flask(__name__)
api = Api(app)
swagger = Swagger(app)

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="Darshana@1310",
  database="FlashCard"
)
crsr = mydb.cursor()


@app.route('/')
def home():
    title = 'Welcome to Our Website!'
    return render_template('home.html', title=title)


@app.route('/about/')
def about():
    title = 'About Us'
    return render_template('about.html', title=title)

# getting the TopicWise Questions
@app.route("/getTopicQuestions/<topic>")
def getTopicQuestion(topic):
    sql_command = "SELECT * FROM Questions WHERE Topic = %s"
    val= [topic]
    crsr.execute(sql_command, val)
    myresult = crsr.fetchall()
    # adding the Function to learn
    return myresult, 200
    

#To create a Questions
@app.route('/createQuestion/', methods=['Post'])
def createQuestion():
    data = request.get_json()
    sql_command = "INSERT INTO Questions VALUES (%s, %s, %s, %s, %s)"
    val = (data['ID'],data['Topic'], data['Question'],data['Answer'],data['Hint'])
    crsr.execute(sql_command, val)
    mydb.commit()
    return jsonify(data), 201

def learningMode():
    # show Question
    # receive Answer
    # cross check answer
    # Show comment
    #



if __name__ == '__main__':
    app.run(debug=True)