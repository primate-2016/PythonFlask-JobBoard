from flask import Flask, render_template

app = Flask(__name__)

@app.route('/') # tell Flask to call this function when http://127.0.0.1/ or http://127.0.0.1/jobs is hit
@app.route('/jobs')
def jobs():
    return render_template('index.html') # tell flask to render the index.html template when this function is called (by hitting the above routes)