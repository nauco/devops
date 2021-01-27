from flask import Flask, render_template
import psycopg2
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get')
def list():
    conn = psycopg2.connect(dbname="dev", user = "awsuser", password = "aws!Red1",
                            host = "redshift-cluster-1.crrx4sdg4mct.ap-northeast-2.redshift.amazonaws.com", port = "5439")
    cur = conn.cursor()
    # Executing a SQL query
    cur.execute("SELECT * from public.todo")
    todoList = cur.fetchall()
    print(todoList)
    return render_template('index.html', todoList = todoList)
  
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8000)
