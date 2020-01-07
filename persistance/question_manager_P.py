from database import db_connection as con


@con.connection_handler
def get_question(cursor, question_id):
    cursor.execute('SELECT * FROM question WHERE id=%(id)s', {'id': question_id})

    question = cursor.fetchone()
    return question


# DELETE QUESTIONS
@con.connection_handler
def delete_question(cursor, question_id):
    cursor.execute("""
    DELETE FROM question_tag
    WHERE question_id = %(question_id)s;
    DELETE FROM comment
    WHERE question_id = %(question_id)s;
    DELETE FROM question
    WHERE id = %(question_id)s;

    """,
                   {'question_id': question_id})


@con.connection_handler
def get_all_questions(cursor):
    """
    Takes all questions from SQL
    :param cursor:
    :return: all questions
    """
    cursor.execute(""" 
    SELECT * FROM question
    ORDER BY submission_time DESC;
    """)
    all_questions = cursor.fetchall()
    return all_questions


@con.connection_handler
def get_five_questions(cursor):
    """
    Takes first 5 questions from SQL in descenting order
    :param cursor:
    :return: five_questions
    """
    cursor.execute(""" 
    SELECT * FROM question
    ORDER BY submission_time DESC LIMIT 5;
    """)
    five_questions = cursor.fetchall()
    return five_questions


@con.connection_handler
def get_five_questions(cursor):
    cursor.execute(""" 
    SELECT * FROM question
    ORDER BY submission_time DESC LIMIT 5;
    """)
    five_questions = cursor.fetchall()
    return five_questions


@con.connection_handler
def sort_questions(cursor, order, attribute):
    cursor.execute("SELECT * FROM question "
                   "ORDER BY {0} {1}".format(order, attribute))

    sorted_questions = cursor.fetchall()
    return sorted_questions

@con.connection_handler
def update_question_in_db(cursor, id, title,  message, image):
    cursor.execute("""
                   UPDATE question SET title=%(title)s, message=%(message)s, image=%(image)s 
                   WHERE id=%(id)s;""",
                   {"title": title,
                    "message": message,
                    "image": image,
                    "id": id})

#
# some idea for giving table as a function(param)
@con.connection_handler
def create_question(cursor, title, message, image):
    """
    Adds new question to SQL
    :param cursor:
    :param title:
    :param message:
    :param image:
    :return: new question id as a string
    """
    cursor.execute("""
    INSERT INTO question (submission_time,title, message, image)
    VALUES (DATE_TRUNC('minute', now()), %(title)s, %(message)s, %(image)s)
    RETURNING id;
        """, {"title": title,
              "message": message,
              "image": image})
    question_id = cursor.fetchone()
    return str(question_id['id'])

# @con.connection_handler
# def get_all_data(cursor, table_name):
#     cursor.execute("""
#     SELECT * FROM {{ table_name }}
#     ORDER BY submission_time DESC;
#     """)
#     all_questions = cursor.fetchall()
#     return all_questions