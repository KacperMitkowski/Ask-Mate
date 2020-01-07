from persistance import question_manager_P as qP


def get_question_by_id(question_id):
    try:
        question = qP.get_question(question_id)
        return question
    except FileNotFoundError:
        return []


def delete_question(question_id):
    try:
        qP.delete_question(question_id)
    except FileNotFoundError:
        pass


def get_all():
    try:
        return qP.get_all_questions()
    except FileNotFoundError:
        return []


def get_five():
    try:
        return qP.get_five_questions()
    except FileNotFoundError:
        return []


def sort_questions(attribute, order):
    try:
        sorted_data = qP.sort_questions(attribute, order)
        return sorted_data
    except FileNotFoundError:
        return []


def update_data_by_id(question_id, question_title, question_message, question_image):
    try:
        return qP.update_question_in_db(question_id,
                                        question_title,
                                        question_message,
                                        question_image)
    except FileNotFoundError:
        return []


def add_question(title, message, image):
    try:
        return qP.create_question(title, message, image)
    except FileNotFoundError:
        return []