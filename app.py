from flask import Flask,request,render_template,redirect,session
from flask_session import  Session
import middleware
import psycopg2
import  insert


app=Flask(__name__,template_folder="template")
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

app.wsgi_app=middleware.SimpleMiddleware(app.wsgi_app)
client=psycopg2.connect(database="Test",user="postgres",password="admin@123",host="localhost",port="5432")
cursor=client.cursor()




@app.route("/lo")
def home():
    try:
        name = session.get("name")
        id=session.get("id")
        print(name)
        log = False
        if name == None:
            log = True
            print("No User Found")
        cursor.execute('select * from "Authentication"')

        # print(data)
        #  request.environ["wsgi_version_name"] = name
        record = cursor.fetchall()
        print(record[0][0])
        insert.insertToken(id, request.environ["HTTP_COOKIE"][8:])

        return render_template("index.html", data=record, log=log)
    except Exception as e:
        print(e)

def GetAuth():
    name=None
    if session["name"] is not None:
        name=session["name"]
    return name


@app.route("/login",methods=["POST"])
def login():
    data=request.form
    print(data)
    username=data["username"]
    password=data["password"]
    query=f'select * from "Authentication" where username=%s and password=%s'
    re=(username,password)
    cursor.execute(query,re)
    dat=cursor.fetchall()
    print(cursor.fetchall(),len(dat),"hello")
    if len(dat)>0:
        session["name"]=username
        session["id"]=dat[0][0]
        # print(request.environ)
        request.environ["name"]=username
        print(dat[0][0],request.cookies)


        return redirect("/lo")
    else:

        return render_template("index.html",error="You have entered wrong password",log=True)





if __name__=="__main__":
    app.run(debug=True)