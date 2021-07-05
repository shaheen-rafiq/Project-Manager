from flask import Flask,render_template,url_for,request,redirect
import psycopg2

app=Flask(__name__)
import psycopg2

conn=psycopg2.connect(
    host="localhost",
    database="todo_app_hw",
    user="postgres",
    password="postgres"
)
cur=conn.cursor()

@app.route('/',methods=['POST','GET'])
def index():
    if request.method=='POST':
        cur.execute('SELECT subj_name FROM subject_list')
        subs=cur.fetchall()

        if 'ViewDate' in request.form and 'ViewSubj' in request.form:
            cur.execute('SELECT * FROM todo2 ORDER BY subject,due_date')
            rows=cur.fetchall()
            return render_template("index.html",tasks=rows,subjects=subs)

        if 'ViewDate' in request.form:
            cur.execute('SELECT * FROM todo2 ORDER BY due_date')
            rows=cur.fetchall()
            return render_template("index.html",tasks=rows,subjects=subs)

        if 'ViewSubj' in request.form:
            cur.execute('SELECT * FROM todo2 ORDER BY subject')
            rows=cur.fetchall()
            return render_template("index.html",tasks=rows,subjects=subs)
        
        
        if 'newSubj' in request.form:
            subject_to_insert=request.form['newSubj']
            cur.execute('INSERT INTO subject_list(subj_name) VALUES (%s)',(subject_to_insert,))

        if 'content' in request.form:
            task_content=request.form['content']
            subject_content=request.form['subjects']
            due_date=request.form['date']
            cur.execute('INSERT INTO todo2(subject,content,due_date) VALUES (%s,%s,%s)',(subject_content,task_content,due_date))

        conn.commit()
        return redirect('/')
        
    else:
        cur.execute('SELECT * FROM todo2 ORDER BY subject')
        rows=cur.fetchall()
        cur.execute('SELECT subj_name FROM subject_list')
        subs=cur.fetchall()
        return render_template("index.html",tasks=rows,subjects=subs)

@app.route('/delete/<int:id>')
def deleteTask(id):
    cur.execute('DELETE FROM todo2 WHERE id=%s',(id,))
    conn.commit()
    return redirect('/')

@app.route('/subjects',methods=['GET','POST'])
def subjects():
    if request.method=='POST':
        try:
            toAdd=request.form['addSubj']
            cur.execute('INSERT INTO subject_list(subj_name) VALUES(%s)',(toAdd,))
            return redirect('/subjects')
        except:
            return 'error'
    else:
        cur.execute('SELECT * FROM subject_list')
        subs=cur.fetchall()
        return render_template("subjects.html",subjects=subs)

@app.route('/subjects/delete/<int:id>')
def deleteSubject(id):
    print(id)
    cur.execute('DELETE FROM todo2 WHERE subject=(SELECT subj_name FROM subject_list  WHERE id=%s)',(id,))
    cur.execute('DELETE FROM subject_list WHERE id=%s',(id,))
    conn.commit()
    return redirect('/subjects')


# @app.route('/update/<int:id>',methods=['GET','POST'])
# def updateTask(id):
#     cur.execute('SELECT * FROM todo WHERE id=%s',(id,))
#     query=cur.fetchone()

#     if request.method=='POST':
#         task_content=request.form['content']
#         cur.execute('UPDATE todo SET content=%s WHERE id=%s',(task_content,id))
#         conn.commit()
#         return redirect('/')
#     else:
#         return render_template('Update.html',task=query)

# cur.close()
# conn.close()

if __name__=="__main__":
    app.run(debug=True)