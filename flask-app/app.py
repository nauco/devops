from flask import Flask, render_template, request
import psycopg2, ast
app = Flask(__name__)

def db():
    conn = psycopg2.connect(dbname="dev", user = "awsuser", password = "aws!Red1",
                        host = "redshift-cluster-1.crrx4sdg4mct.ap-northeast-2.redshift.amazonaws.com", port = "5439")
    return conn
@app.route('/todo', methods=['GET', 'POST'])
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


@app.route('/test/ei')
def ei():
    return render_template('test.html', step = 1, result = '')

@app.route('/test/sn')
def sn(ei):
    return render_template('test.html', step = 2, result = ei)

@app.route('/test/ft')
def ft(sn):
    return render_template('test.html', step = 3, result = sn)

@app.route('/test/jp')
def jp(ft):
    return render_template('test.html', step = 4, result = ft)

@app.route('/test/result')
def res(jp):
    pool = ["estj", "estp", "enfp", "entp", "esfj", "esfp", "enfj", "entj", "istj", "istp", "infp", "intp", "isfj", "isfp", "infj", "intj"]
    if jp not in pool:
        return render_template('test.html', step = 1, result = '')
    #db connect and save a result
    conn = db()
    cur = conn.cursor()
    cur.execute("SELECT sum(count_mbti) FROM mbti1;")
    cnt = cur.fetchall()
    cur.execute("SELECT * FROM mbti1 WHERE mbti = %(res)s;", {"res": jp.upper()})
    mlist = cur.fetchall()
    cur.execute("UPDATE mbti1 SET count_mbti = count_mbti + 1  WHERE mbti = %(res)s;", {"res": jp.upper()})
    cur.close()
    conn.commit()
    conn.close()
    return render_template('test.html', step = 5, cnt = cnt, mlist = mlist[0], result = jp)

@app.route('/')
def test():
    return render_template('test.html', step = 0)


@app.route("/<string:pick>")
def hello(pick):
    if pick[-1] in "ei":
        return sn(pick)
    elif pick[-1] in "sn":
        return ft(pick)
    elif pick[-1] in "ft":
        return jp(pick)
    elif pick[-1] in "jp":
        return res(pick)
    else:
        return ei()

  
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8000)
