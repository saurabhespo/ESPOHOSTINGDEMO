from flask import Flask, request, jsonify
import dbutils
import queryutils
import llmutils
from flask import send_from_directory
import pandas as pd
app = Flask(__name__)


@app.route('/Images/<path:filename>')
def serve_file(filename):
    return send_from_directory("Images", filename)

@app.route('/', methods=['Get'])
def hello():
    return "Hello Welcome to ESPO AI"

@app.route('/answer', methods=['POST'])
def get_answer():

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
    followup,questions = llmutils.get_questions()
    if  user_question not in questions:

        session = llmutils.get_history()
        if session is not None:
            if session_id in session:
                history = session[session_id][-5:]
            else:
                history = []
        else:
            session = dict()
            history = []

        history.append(user_question)
        session[session_id] = history
        _ = llmutils.write_history(session)

        question = queryutils.query_rewriter(query=user_question, session_history=history)
        
    
    else:
        print("not in history")
        question = user_question
    
    print(question)
    db = dbutils.get_db()
    table_info = dbutils.get_table_info()

    sql_query = queryutils.get_sql_query(query=question, table_info=table_info)

    answer = queryutils.execute_sql_query(query=sql_query, db=db)
    print (answer)
    answer = queryutils.generate_qna_ans(user_query=question, answer=answer)
    print (answer)
     #queryutils.generate_qna_followup(user_query=question)
    print (followup)
    return answer, followup

if __name__ == "__main__":
  app.run(debug=True,port=5005)
 