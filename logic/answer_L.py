from persistance import answer_manager_P as aP


class WrongLength(Exception):
    """ If text has not valid length"""
    pass


# Create
def add_answer_to_database(question_id, message, image):
    try:
        return aP.add_answer_into_database(question_id, message, image)
    except FileNotFoundError:
        return []


# Get
def get_by_question_id(question_id):
    try:
        return aP.get_answer_by_parameter('question_id', question_id)
    except FileNotFoundError:
        return []


def get_by_id(answer_id):
    try:
        return aP.get_answer_by_parameter('id', answer_id)
    except FileNotFoundError:
        return []


def find_question_id_in_answer(answer_id):
    answer = get_by_id(answer_id)
    for data in answer:
        return data['question_id']


# Update
def update_from_user(new_data, answer_id):
    try:
        return aP.update_two_columns_in_answers(new_data, answer_id)
    except FileNotFoundError:
        pass


# Delete
def delete_from_database(answer_id):
    try:
        return aP.delete_data_in_answer(answer_id)
    except FileNotFoundError:
        pass


def delete_all_answers_for_question_id(question_id):
    all_answers = get_by_question_id(question_id)
    for answer in all_answers:
        answer_id = answer['id']
        delete_from_database(answer_id)


# Validate
def validate_text(text_data, area):
    if len(text_data) in area and not text_data.isspace():
        return text_data

# we have to fix it to check correctly whitespaces.
def validate_message(message):
    try:
        validate_text(message, range(10, 100000))
        return message
    except WrongLength:
        return []

def get_answers_by_id(question_id):
    try:
        all_answers = aP.get_all_answers(question_id)
        return all_answers
    except FileNotFoundError:
        return []
