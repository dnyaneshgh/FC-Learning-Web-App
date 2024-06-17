from flask import Flask, render_template, url_for, redirect, request

app = Flask(__name__)

# Sample data to simulate created sets and flashcards
created_sets = []
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
        if set_name not in created_sets:
            created_sets.append(set_name)
        return redirect(url_for('create_fc'))
    return render_template('create_set.html')

@app.route('/create_fc', methods=['GET', 'POST'])
def create_fc():
    if request.method == 'POST':
        question = request.form['question']
        answer = request.form['answer']
        hint = request.form.get('hint', '')  # Hint is optional
        flashcards.append({'question': question, 'answer': answer, 'hint': hint})
        return render_template('create_fc.html', flashcard_count=len(flashcards) + 1)
    return render_template('create_fc.html', flashcard_count=1)

@app.route('/select_set')
def select_set():
    return render_template('select_set.html', sets=created_sets)

@app.route('/fc_use/<int:index>', methods=['GET', 'POST'])
def fc_use(index):
    if not flashcards:
        return redirect(url_for('create_fc'))

    flashcard = flashcards[index]
    total_cards = len(flashcards)

    if request.method == 'POST':
        user_answer = request.form['answer']
        # Here, you can add code to check the user's answer
        # For simplicity, we'll just pass the user answer back to the template

    next_index = (index + 1) % total_cards
    prev_index = (index - 1 + total_cards) % total_cards

    return render_template('fc_use.html', flashcard=flashcard, current_index=index, next_index=next_index, prev_index=prev_index, total_cards=total_cards)

if __name__ == '__main__':
    app.run(debug=True)
