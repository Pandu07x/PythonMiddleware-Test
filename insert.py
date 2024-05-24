import psycopg2
client=psycopg2.connect(database="Test",user="postgres",password="admin@123",host="localhost",port="5432")
client.autocommit=True
cursor=client.cursor()
def insertToken(id,session):
    try:
        query=f"INSERT INTO public.session(user_id, session) VALUES ({id}, '{session}');"
        cursor.execute(query)
        return 200
    except Exception as e:
        print(e, "he")
        return 500

def GetUsername(session):
    try:
        query='select auth.username from "Authentication" as auth join session as s on auth."ID"=s.user_id where s.session=%s'
        cursor.execute(query,session)
        name=cursor.fetchall()
        return name[0][0]


    except Exception as e :
        print(e,"he")
        return 500

