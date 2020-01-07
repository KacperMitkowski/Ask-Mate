from flask import Flask, request, redirect, url_for, render_template, flash
from logic import answer_L as aL
from logic import question_L as qL

from flask import Flask, render_template, redirect, request, url_for

app = Flask(__name__)


@app.route('/')
def route_five_questions_list():
    """
    Supports showing first 5 questions
    :return:
    """
    five_questions = qL.get_five()
    return render_template('questions_list.html',
                           all_questions=five_questions)


@app.route('/list')
def route_all_questions_list():
    """
    Supports showing all questions
    :return:
    """
    all_questions = qL.get_all()
    return render_template('questions_list.html',
                           all_questions=all_questions)


@app.route('/question/<question_id>')
def route_question_view(question_id):
    """
    Function supports displaying page of given question and all answers for it
    Function generates effects of voting for question and counts views of question
    :param question_id:
    :return: page of given question
    """

    question = qL.get_question_by_id(question_id)
    all_answers = aL.get_answers_by_id(question_id)
    return render_template('question_page.html',
                           question=question,
                           all_answers=all_answers)


@app.route('/question/<question_id>/delete', methods=['POST'])
def route_delete_question(question_id):
    """
    Function supports deleting questions
    :param question_id:
    :return /list page:
    """
    aL.delete_all_answers_for_question_id(question_id)
    qL.delete_question(question_id)
    return redirect(url_for('route_all_questions_list'))  # /list


@app.route('/question/<question_id>/new-answer', methods=['GET', 'POST'])
def route_post_answer(question_id):
    """
    Function supports adding answer to question
    :param question_id:
    :return: depends of used method
    """

    if request.method == 'GET':
        return render_template('add_answer.html',
                               form_url=url_for('route_post_answer',
                                                question_id=question_id))
    elif request.method == 'POST':
        try:
            message = aL.validate_message(request.form['message'])
            image = request.form['image']
            aL.add_answer_to_database(question_id, message, image)
            return redirect(url_for('route_question_view',
                                    question_id=question_id))
        except aL.WrongLength:
            flash(message='Length of text must be correct')
            return redirect(url_for('route_post_answer',
                                    question_id=question_id))


@app.route('/answer/<answer_id>/edit', methods=['POST', 'GET'])
def route_edit_answer(answer_id):
    if request.method == 'GET':
        return render_template('add_answer.html',
                               answer=aL.get_by_id(answer_id),
                               form_url=url_for('route_edit_answer',
                                                answer_id=answer_id))

    elif request.method == 'POST':
        try:
            message = aL.validate_message(request.form['message'])
            image = request.form['image']
            question_id = aL.find_question_id_in_answer(answer_id)
            aL.update_from_user((message, image), answer_id)
            return redirect(url_for('route_question_view',
                                    question_id=question_id))
        except aL.WrongLength:
            flash(message='Length of text must be correct')
            return redirect(url_for('route_edit_answer',
                                    answer_id=answer_id))


@app.route('/answer/<answer_id>/delete', methods=['POST'])
def route_delete_answer(answer_id):
    """
    Function supports deleting answers
    :param answer_id:
    :return /question page:
    """

    question_id = aL.delete_from_database(answer_id)
    return redirect(url_for('route_question_view',  # display question function
                            question_id=question_id))


@app.route('/list/sorted')
def route_list_sorted():
    """
    :param none
    :return:
    """
    attribute = request.args.get('attribute')
    order = request.args.get('order')
    sorted_all_data = qL.sort_questions(attribute, order)
    return render_template('questions_list.html',
                           all_questions=sorted_all_data)


@app.route('/question/<question_id>/edit', methods=['POST', 'GET'])
def route_edit_question(question_id):
    """
    :param question_id:
    :return:
    """

    question = qL.get_question_by_id(question_id)
    if request.method == 'GET':
        return render_template('add_question.html',
                               question=question,
                               form_url=url_for('route_edit_question', question_id=question['id']))
    elif request.method == 'POST':
        question_id = question['id']
        question_title = request.form['title']
        question_message = request.form['message']
        question_image = request.form['image']
        qL.update_data_by_id(question_id,
                             question_title,
                             question_message,
                             question_image)
        return redirect(url_for('route_question_view',
                                question_id=question_id))


@app.route('/add-question', methods=['POST', 'GET'])
def route_add_question():
    """
    Function supports adding questions to database
    :return: page depending of used method
    """
    if request.method == 'POST':
        title = request.form['title']
        message = request.form['message']
        image = request.form['image']
        question_id = qL.add_question(title, message, image)
        return redirect('/question/' + question_id)

    elif request.method == "GET":
        return render_template('add_question.html',
                               form_url=url_for('route_add_question'))


if __name__ == "__main__":
    app.run(debug=True,
            host='0.0.0.0',
            port=8000)
