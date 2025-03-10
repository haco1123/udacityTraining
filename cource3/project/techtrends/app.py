import sqlite3

from flask import Flask, jsonify, json, render_template, request, url_for, redirect, flash
from werkzeug.exceptions import abort
import logger

connection_count = 0

# Function to get a database connection.
# This function connects to database with the name `database.db`
def get_db_connection():
    global connection_count
    connection = sqlite3.connect('database.db')
    connection.row_factory = sqlite3.Row
    connection_count += 1
    return connection

# Function to get a post using its ID
def get_post(post_id):
    connection = get_db_connection()
    post = connection.execute('SELECT * FROM posts WHERE id = ?',
                        (post_id,)).fetchone()
    connection.close()
    return post

# Define the Flask application
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'

# Define the main route of the web application 
@app.route('/')
def index():
    connection = get_db_connection()
    posts = connection.execute('SELECT * FROM posts').fetchall()
    connection.close()
    return render_template('index.html', posts=posts)

# Define how each individual article is rendered 
# If the post ID is not found a 404 page is shown
@app.route('/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    if post is None:
      logger.log('A non-existing article is accessed')
      return render_template('404.html'), 404
    else:
      logger.log('An existing article is retrieved.', f"Title: {post['title']}")
      return render_template('post.html', post=post)

# Define the About Us page
@app.route('/about')
def about():
    logger.log("'About Us' page is retrieved")
    return render_template('about.html')

# Define the post creation functionality 
@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        else:
            connection = get_db_connection()
            connection.execute('INSERT INTO posts (title, content) VALUES (?, ?)',
                         (title, content))
            connection.commit()
            connection.close()

            logger.log('A new article is created.', f"Title: {title}")

            return redirect(url_for('index'))

    return render_template('create.html')

# health status
@app.route('/healthz')
def healthcheck():
    response = app.response_class(
            response=json.dumps({"result":"OK - healthy"}),
            status=200,
            mimetype='application/json'
    )
    logger.log('Status request successfull.')
    return response

# get metrics with connection and posts amount
@app.route('/metrics')
def metrics():
    global connection_count
    connection = get_db_connection()
    posts = connection.execute('SELECT COUNT(id) FROM posts').fetchone()
    connection.close()
    response = app.response_class(
            response=json.dumps({"status":"success","code":0,"data":{"db_connection_count": connection_count, "post_count": posts[0]}}),
            status=200,
            mimetype='application/json'
    )
    logger.log('Metrics request successfull.')
    return respon

# start the application on port 3111
if __name__ == "__main__":
    ## stream logs to a file
    app.run(host='0.0.0.0', port='3111')
