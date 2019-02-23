from flask import Flask, render_template, g # g is Flask's global helper to enable database connection 
import sqlite3

PATH = 'db/jobs.sqlite' # constant to point to the sqlite database at this path

# you can preview your work by running 'flask run' in the root of your repo. Then visit http://localhost:5000 in your browser.
app = Flask(__name__) # instantiate an instance of the Flask class, pass in the __name__ of this module (i.e. app)

def open_connection(): # create a function to connect to the database
    connection = getattr(g, '_connection', None) # use the built-in gettattr() to get the _connection attribute of the 'g' object
    if connection == None: # if g doesn't have a database connection
        connection = g._connection = sqlite3.connect(PATH) # set g's connection object to the sqlite connection
    connection.row_factory = sqlite3.Row # all rows returned from the database will be named tuples
    return connection

def execute_sql(sql, values=(), commit=False, single=False):
    connection = open_connection()
    cursor = connection.execute(sql, values)
    if commit == True:
        results = connection.commit()
    else:
        results = cursor.fetchone() if single else cursor.fetchall()

    cursor.close()
    return results

@app.teardown_appcontext # this decorator ensures the db connection is destroyed when the app context is destroyed
def close_connection(exception):
    connection = getattr(g, '_connection', None)
    if connection is not None:
        connection.close()
        
@app.route('/') # tell Flask to call this jobs() function when http://127.0.0.1/ or http://127.0.0.1/jobs is hit
@app.route('/jobs')
def jobs():
    jobs = execute_sql('SELECT job.id, job.title, job.description, job.salary, employer.id as employer_id, employer.name as employer_name FROM job JOIN employer ON employer.id = job.employer_id')
    return render_template('index.html', jobs=jobs) # tell flask to render the index.html template when this function is called (by hitting the above routes)

@app.route('/job/<job_id>')
def job(job_id):
    job = execute_sql('SELECT job.id, job.title, job.description, job.salary, employer.id as employer_id, employer.name as employer_name FROM job JOIN employer ON employer.id = job.employer_id WHERE job.id = ?', [job_id], single=True)
    return render_template('job.html', job=job)

@app.route('/employer/<employer_id>')
def employer(employer_id):
    employer = execute_sql('SELECT * FROM employer WHERE id=?', [employer_id], single=True)
    jobs = execute_sql('SELECT job.id, job.title, job.description, job.salary FROM job JOIN employer ON employer.id = job.employer_id WHERE employer.id = ?', [employer_id])
    reviews = execute_sql('SELECT review, rating, title, date, status FROM review JOIN employer ON employer.id = review.employer_id WHERE employer.id = ?', [employer_id])
    return render_template('employer.html', employer=employer, jobs=jobs, reviews=reviews)
