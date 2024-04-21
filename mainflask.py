from flask import Flask, render_template, url_for, request, redirect, session
from languages import spanish, french, german, vietnamese
import random
import smtplib
from email.message import EmailMessage

translation = None
correct_summary = []
incorrect_summary = []

def test(lang):
    global translation
    global random_word

    if lang == spanish:
        words = "Spanish"
    elif lang == french:
        words = "French"
    elif lang == german:
        words = "German"
    elif lang == vietnamese:
        words = "Vietnamese"
    # Picks a random word from the chosen language
    random_word = random.choice(lang)
    # Gets English translation for that word
    translation = random_word["English"]

    return random_word[f"{words}"]

app = Flask(__name__)

score = 0

@app.route('/')

@app.route('/home')

def home():
    return render_template("index.html")

@app.route('/study',methods=['POST', 'GET'])

def study():
    global score
    global chosen_language
    global translation
    global random_word
    if request.method == 'POST':
            # If "Done" button is clicked
        if 'done_button' in request.form:
            done()
            return redirect(url_for("home"))
        # Gets entered word from user 
        input = request.form.get('input_word')
        correct_translation = None
        # Iterate through the dictionaries of the chosen language
        for word_dict in chosen_language:
                # Check if the input word is found in the dictionary
            if input in word_dict.values():
                    # If found, retrieve its translation using the appropriate key
                correct_translation = word_dict["English"]
                break
        # If user enters correct answer
        if correct_translation == input:
            # Increment the score
            score += 1
            # Append data to correct_summary
            correct_summary.append(random_word)
            return render_template("study.html", language=lang, random_word=test(chosen_language), score=score, exception="")
        else:
            # Prevents score from going negative
            if score == 0:
                score = 0
            else: 
                score -= 1
            prev = translation
            # Append data to incorrect_summary
            incorrect_summary.append(random_word)
            
            return render_template("study.html", language=lang, random_word=test(chosen_language), score=score, exception=f"Wrong. Answer was: {prev}") 
        
    return render_template("study.html", language = lang, random_word = test(chosen_language), score = 0)

@app.route('/result',methods=['POST', 'GET'])

def result():
    output = request.form.to_dict()
    global lang
    lang = output['language'].capitalize()
    global chosen_language
    
    # If user chooses language that we do not provide
    if lang != "Spanish" and lang != "German" and lang != "French" and lang != "Vietnamese":
        exception_dict = {'exception': "We do not support that language. Please Try Again."}
        lang = exception_dict['exception']
        return render_template('index.html', language = lang)
    
    if lang == "Spanish":
        chosen_language = spanish
        return redirect(url_for("study"))
    
    elif lang == "French":
        chosen_language = french
        return redirect(url_for("study"))
    
    elif lang == "German":
        chosen_language = german
        return redirect(url_for("study"))

    elif lang == "Vietnamese":
        chosen_language = vietnamese
        return redirect(url_for("study"))
    

@app.route('/done', methods=['POST'])

# Send SMS and email messages with things you got incorrect
def done():
    number = # ADD NUMBER HERE
    alert("Words you got wrong", f"{incorrect_summary}", number)
    alert("Words you got wrong", f"{incorrect_summary}", "ADD EMAIL HERE")

    return redirect(url_for("home"))

# Messaging function
def alert(subject, body, to):
    msg = EmailMessage()
    msg.set_content(body)
    msg['Subject'] = subject
    msg['To'] = to

    user = "ADD EMAIL HERE"
    
    msg['From'] = user
    password = "ADD PASSWORD HERE"

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(user, password)
    server.send_message(msg)
    server.quit()

if __name__ == "__main__":
    app.run(debug=True)
    
    

