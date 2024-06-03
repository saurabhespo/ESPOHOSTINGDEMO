from flask import Flask, request, jsonify
import dbutils
import queryutils
import llmutils

app = Flask(__name__)

@app.route('/answer', methods=['POST'])
def get_answer():
    print('in')
    data = request.json
    user_question = data.get('user_question')
    session_id = data.get('session_id')

    if user_question and session_id:
       answer, followup = main(user_question, session_id)
       return jsonify({'answer': answer, 'followup': followup}), 200
    else:
        return jsonify({'error': 'Invalid request parameters'}), 400

def main(user_question, session_id):
    # Your existing main function code goes here
    session = llmutils.get_history()
    if session is not None:
        if session_id in session:
            history = session[session_id]
        else:
            history = []
    else:
        session = dict()
        history = []

    history.append(user_question)
    session[session_id] = history
    _ = llmutils.write_history(session)

    db = dbutils.get_db()
    table_info = dbutils.get_table_info()

    question = queryutils.query_rewriter(query=user_question, session_history=history)

    sql_query = queryutils.get_sql_query(query=question, table_info=table_info)

    answer = queryutils.execute_sql_query(query=sql_query, db=db)

    answer = queryutils.generate_qna_ans(user_query=question, answer=answer)

    followup = queryutils.generate_qna_followup(user_query=question)
    print(followup)
    return answer,followup

if __name__ == "__main__":
    app.run(port=5005)
