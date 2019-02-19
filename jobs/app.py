from flask import Flask, render_template

# you can preview your work by running 'flask run' in the root of your repo. Then visit http://localhost:5000 in your browser.
app = Flask(__name__) # an instance of the Flask class, pass in the __name__ of this module (i.e. app)

@app.route('/') # tell Flask to call this function when http://127.0.0.1/ or http://127.0.0.1/jobs is hit
@app.route('/jobs')
def jobs():
    return render_template('index.html') # tell flask to render the index.html template when this function is called (by hitting the above routes)