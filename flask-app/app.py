from flask import Flask, render_template, request
import psycopg2, ast
app = Flask(__name__)

def db():
    conn = psycopg2.connect(dbname="dev", user = "awsuser", password = "aws!Red1",
                        host = "redshift-cluster-1.crrx4sdg4mct.ap-northeast-2.redshift.amazonaws.com", port = "5439")
    return conn
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == "GET":
        cur = db().cursor()
        # Executing a SQL query
        cur.execute("SELECT * from public.todolist")
        todoList = cur.fetchall()
        print(todoList)
        return render_template('index.html', todoList = todoList)
    elif request.method == "POST":
        print("post", request.data.decode('UTF-8'))
        mydata = ast.literal_eval(request.data.decode('UTF-8'))
        print(mydata['element'])

        conn = db()
        cur = conn.cursor()
        cur.execute("INSERT INTO public.todolist(user_id, todo) VALUES ('1', %(obj)s);", {"obj": mydata['element']})
        cur.close()
        conn.commit()
        conn.close()

        return render_template('index.html')

@app.route('/get')
def list():
    cur = db().cursor()
    # Executing a SQL query
    cur.execute("SELECT * from public.todolist")
    todoList = cur.fetchall()
    print(todoList)
    return render_template('index.html', todoList = todoList)
  
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8000)
