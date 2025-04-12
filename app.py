from flask import Flask, render_template, redirect, flash,request, session
from dotenv import load_dotenv
import os
from google import genai
from database import *
app = Flask(__name__)
app.config['SECRET_KEY'] = 'hygwdfwgdbgcwd53rreft3dywydt35eyet6d'

load_dotenv()
api_key = os.getenv("API_KEY")

def generate_storie(tone, character_name, topic, place, length):
    prompt = f"""
        Generate a {tone} story with the following details:
        Character Name: {character_name}
        Theme: {topic}
        Setting: {place}
        Length: {length}
        ** dont include theword json in your response
        the result should be en form of a python dictionary:
        generated_story={{ 
            title: the story title,
            story: the story content

        }}

        The story should be engaging, creative, and match the tone of the prompt.
        """
    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model="gemini-2.0-flash", contents=prompt
    )
    
    # Get the text response from the generated content
    data = response.text
    print(data)
    global_scope = globals()
    try:
        # executing the return response to get a dictionary 
        cleaned_response = data.strip("```python\n").strip("```")
        exec(cleaned_response, global_scope)
        return generated_story
    except Exception as e:
        return None


@app.route("/")

def index():
    return render_template("index.html")


@app.route('/generate', methods=['POST', 'GET'])

def generate():
    if request.method == 'GET':
        if request.args['category']:
            category = request.args['category']
            generated_story = generate_storie(tone="funny", character_name="unknown", topic=category, place="any where", length="short")
            if generated_story:
                insert_generated_story(generated_story['title'], generated_story['story'])
                story_id = get_story_id(generated_story['title'],generated_story['story'])
                generated_story['story_id'] = story_id
                return render_template("generated.html",story=generated_story)
            else:
                print("no story generated")
                return "hello"
        return render_template('generate.html')

    if request.method == 'POST':
        charcter_name = request.form.get('character')
        topic = request.form.get('theme')
        place = request.form.get('setting')
        length = request.form.get('length')
        tone = request.form.get('tone')
        if not charcter_name or not topic or not place or not length or not tone:
            print("please provide all fields to generate a story")
        else:
            generated_story = generate_storie(tone,charcter_name,topic,place,length)
            if generated_story:
                insert_generated_story(generated_story['title'], generated_story['story'])
                story_id = get_story_id(generated_story['title'],generated_story['story'])
                generated_story['story_id'] = story_id
                return render_template("generated.html",story=generated_story)
            else:
                print("no story generated")
                return "hello"


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # check if the user provided an email
        if not email:
            flash("Please provide email", "error")
            return redirect('/login')
        
        # check if the user provided a password
        elif not password:
            flash("please Provide password", "error")
            return redirect('/login')
        
        # check if the password is valid
        elif len(password) < 8:
            flash("password must be more than 7 characteres", "error")
            return redirect('/login')
        
        # check if the email already exists
        if(not check_email(email)):
            flash("Invalid email", "error")
            return redirect('/login')
        else:
            if(login_user(email,password)):
                user_data = get_user_id(email)
                session['user_id'] = user_data[0]
                session['username'] = user_data[1]
                flash("Welcome back, You are logged in", "succes")
                return redirect('/')
            else:
                flash("Invalid Password", "error")
                return redirect('/login')
    return render_template('login.html')


@app.route('/register',methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        # check if the user provided a username
        if not username:
            flash("Please provide a username", "error")
            return redirect('/register')
        
        # check if the user provided an email
        elif not email:
            flash("Please provide email", "error")
            return redirect('/register')
        
        # check if the user provided a password
        elif not password:
            flash("please Provide password", "error")
            return redirect('/register')
        
        # check if the password is valid
        elif len(password) < 8:
            flash("password must be more than 7 characteres", "error")
            return redirect('/register')
        
        # check if the email already exists
        if(check_email(email)):
            flash("Sorry Email Already Exists", "warning")
            return redirect('/register')
        else:
            if(register_user(username, email, password)):

                # set user session by the id
                user_data = get_user_id(email)
                session['user_id'] = user_data[0]
                session['username'] = user_data[1] 
                flash("You are registered Welcome ", "succes")
                return redirect('/')
            else:
                flash("Sorry Something Went Wrong", "error")
                return redirect('/register')
        
    return render_template('register.html')


@app.route('/logout')
def logout():
    session.clear()
    flash("You are logged out", "warning")
    return redirect("/login")

@app.route('/')

def generated():
    return render_template('generated.html')

@login_required
@app.route('/save')
def save():
    user_id = request.args['user_id']
    story_id = request.args['story_id']
    results = save_generated_stories(user_id, story_id)
    if(results):
        return "saved"
    else:
        return "notsaved"

@login_required
@app.route('/saved')
def saved():
    user_id = session['user_id']
    results = get_saved_stories(user_id)
    saved_stories = results
    return render_template("saved.html",saved_stories=saved_stories)

    

@login_required
@app.route('/delete_saved_story')
def delete_saved_stories():
    if request.args.get('story_id'):
        user_id = session['user_id']
        story_id = request.args.get('story_id')
        if(remove_from_saved(user_id, story_id)):
            return redirect('/saved')
        else:
            return "Could not Remove"


if(__name__== "__main__"):
    app.run(debug=True)