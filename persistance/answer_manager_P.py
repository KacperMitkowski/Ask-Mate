from database import db_connection as con


# Create
@con.connection_handler
def add_answer_into_database(cursor, question_id, message, image):
    cursor.execute("""
    INSERT INTO answer(submission_time, question_id, message, image)
    VALUES (DATE_TRUNC('minute', now()), %(question_id)s, %(message)s, %(image)s)
    """,
                   {'question_id': question_id,
                    'message': message,
                    'image': image})


# Read
@con.connection_handler
def get_answer_by_parameter(cursor, column_name, parameter):
    cursor.execute("""
    SELECT * FROM answer
    WHERE {0} = %(parameter)s
    ORDER BY submission_time DESC;
    """.format(column_name),
                   {'parameter': parameter})
    answers = cursor.fetchall()
    return answers


# Update
@con.connection_handler
def update_two_columns_in_answers(cursor, new_data, answer_id):
    cursor.execute("""
    UPDATE answer
    SET (message, image) = %(new_data)s 
    WHERE id = %(answer_id)s;
    """,
                   {'new_data': new_data,
                    'answer_id': answer_id})


# Delete
@con.connection_handler
def delete_data_in_answer(cursor, answer_id):
    cursor.execute("""
    DELETE FROM comment
    WHERE answer_id = %(answer_id)s;
    DELETE FROM answer
    WHERE id = %(answer_id)s    
    RETURNING id;
    """,
                   {'answer_id': answer_id})
    question_id = cursor.fetchone()
    return question_id['id']


@con.connection_handler
def get_all_answers(cursor, question_id):
    cursor.execute("SELECT * FROM answer "
                   "WHERE question_id=%(question_id)s;",
                   {'question_id': question_id})

    answers = cursor.fetchall()
    return answers
