from flask import Flask
from flask import jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/")
def hello():
    return "Hello World!"

@app.route('/user/<username>')
def show_user_profile(username):
    # show the user profile for that user
    return jsonify(
        username=username,
        age=31,
        city='Leoben'
    )

@app.route('/post/<int:post_id>')
def show_post(post_id):
    # show the post with the given id, the id is an integer
    return 'Post %d' % post_id

@app.route('/path/<path:subpath>')
def show_subpath(subpath):
    # show the subpath after /path/
    return 'Subpath %s' % subpath

if __name__ == '__main__':
     app.run(host='0.0.0.0')
     app.run(port=5000)