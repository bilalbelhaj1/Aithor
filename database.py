import mysql.connector
from werkzeug.security import check_password_hash, generate_password_hash
from flask import redirect, session
from functools import wraps

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="Aithor"
)

cursor = conn.cursor()


# function to check if a provided email already exists
def check_email(email):
    cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
    rows = cursor.fetchall()
    if len(rows) > 0:
        return True
    return False


def register_user(username, email, password):
    hash = generate_password_hash(password, method='scrypt', salt_length=16)
    try:
        cursor.execute("INSERT INTO users(username, email, password) VALUES(%s, %s, %s)",(username, email, hash))
        conn.commit()
        return True
        
    except Exception:
        return False
    

def login_user(email, password):
    cursor.execute("SELECT * FROM users WHERE email = %s",(email,))
    rows = cursor.fetchall()
    hash = rows[0][3]
    if not check_password_hash(hash, password, ):
        return False
    return True


def get_user_id(email):
    cursor.execute("SELECT id,username FROM users WHERE email = %s", (email,))
    rows = cursor.fetchall()
    return [rows[0][0],rows[0][1]]


def insert_generated_story(title, story):
    cursor.execute("INSERT INTO stories(title, story) VALUES(%s,%s)",(title,story))
    conn.commit()

def get_story_id(title, story):
    cursor.execute("SELECT story_id FROM stories WHERE title=%s AND story = %s",(title,story))

    row = cursor.fetchall()
    return row[0][0]


def save_generated_stories(user_id, story_id):
    try:
        cursor.execute("INSERT INTO saved_stories(user_id,story_id) VALUES(%s,%s)",(user_id, story_id))
        conn.commit()
        return True
    except Exception as e:
        return False
    

def get_saved_stories(user_id):
    cursor.execute("SELECT story_id,title,story,category,generated_at,SUBSTRING(story,1,100) FROM stories WHERE story_id IN (SELECT story_id FROM saved_stories WHERE user_id = %s)",(user_id,))
    rows = cursor.fetchall()
    stories = []
    if(len(rows) > 0):
        for row in rows:
            story = {}
            story['story_id'] = row[0]
            story['title'] = row[1]
            story['story'] = row[2]
            story['category'] = row[3]
            story['date'] = row[4]
            story['shortcut'] = row[5]

            stories.append(story)
    return stories


def remove_from_saved(user_id, story_id):
    try:
        cursor.execute("DELETE FROM saved_stories WHERE user_id = %s AND story_id = %s",(user_id, story_id))
        conn.commit()
        return True
    except Exception:
        return False


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)

    return decorated_function
