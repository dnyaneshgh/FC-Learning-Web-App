from flask import Flask, render_template, url_for, redirect, request
from flask import Flask, jsonify, render_template
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

# Sample data to simulate created sets and flashcards
topic = ""
sql_command = "SELECT Topic FROM Questions GROUP BY Topic"
crsr.execute(sql_command)
myresult = crsr.fetchall()
flashcards = []

@app.route('/')
def main_page():
    return render_template('main_page.html')

@app.route('/process')
def process_page():
    return render_template('process_page.html')

@app.route('/create_set', methods=['GET', 'POST'])
def create_set():
    if request.method == 'POST':
        set_name = request.form['set_name']
        if set_name not in myresult:
            topic = set_name
        return redirect(url_for('create_fc'))
    return render_template('create_set.html')

@app.route('/create_fc', methods=['GET', 'POST'])
def create_fc():
    if request.method == 'POST':
        topic = request.form['topic']
        question = request.form['question']
        answer = request.form['answer']
        hint = request.form.get('hint', '')  # Hint is optional
        flashcards.append({'topic': topic ,'question': question, 'answer': answer, 'hint': hint})

        sql_command = "INSERT INTO Questions(Topic, Question, Answer, Hint) VALUES (%s, %s, %s, %s)"
        val = (topic, question, answer, hint)
        crsr.execute(sql_command, val)
        mydb.commit()

        return render_template('create_fc.html', flashcard_count=len(flashcards) + 1)
    return render_template('create_fc.html', flashcard_count=1)

#Changes pending
@app.route('/select_set')
def select_set():
    return render_template('select_set.html', sets=myresult)

@app.route('/fc_use/<int:index>', methods=['GET', 'POST'])
def fc_use(index):
    topic = "S1"
    sql_command = "SELECT * FROM Questions WHERE Topic = %s"
    val= [topic]
    crsr.execute(sql_command, val)
    data = crsr.fetchall()
    print(data)
    # flashcards.append({'topic': topic ,'question': question, 'answer': answer, 'hint': hint})
    topics = [item[1] for item in data]
    questions = [item[2] for item in data]
    answers = [item[3] for item in data]
    hints = [item[4] for item in data]
    if len(flashcards)==0: 
        for i in range(0,len(data)):
            flashcards.append({'topic': topics[i] ,'question': questions[i], 'answer': answers[i], 'hint': hints[i]})

    print(flashcards)
    

    if not flashcards:
        return redirect(url_for('create_fc'))

    flashcard = flashcards[index]
    total_cards = len(flashcards)

    if request.method == 'POST':
        print(request.form['answer'])
        print(flashcard)
        if flashcard['answer'] != request.form['answer'] and request.form['answer']!="" : # msg answer is right
            print(flashcard)
            flashcards.append(flashcard)
            print(flashcards)
        
        #Answer is wrong: Show message answer is wrong

    next_index = (index + 1) % total_cards
    prev_index = (index - 1 + total_cards) % total_cards

    return render_template('fc_use.html', flashcard=flashcard, current_index=index, next_index=next_index, prev_index=prev_index, total_cards=total_cards)



if __name__ == '__main__':
    app.run(debug=True)
