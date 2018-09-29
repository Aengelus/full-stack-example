from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_restful import reqparse, abort, Api, Resource

from datetime import datetime

app = Flask(__name__)
api = Api(app)

CORS(app)

#@app.route("/")
#def hello():
#    return "Hello World!"

#@app.route('/user/<username>')
#def show_user_profile(username):
#    return jsonify(
#        username=username,
#        age=31,
#        city='Leoben'
#    )

# Here we will add our methods for the todo list app. Storage in MongoDB

TODOS = {
    '1': {'task': 'build an API'},
    '2': {'task': '?????'},
    '3': {'task': 'profit!'},
}


def abort_if_todo_doesnt_exist(todo_id):
    if todo_id not in TODOS:
        abort(404, message="Todo {} doesn't exist".format(todo_id))

parser = reqparse.RequestParser()
parser.add_argument('task')


# Todo
# shows a single todo item and lets you delete a todo item
class Todo(Resource):
    def get(self, todo_id):
        abort_if_todo_doesnt_exist(todo_id)
        return TODOS[todo_id]

    def delete(self, todo_id):
        abort_if_todo_doesnt_exist(todo_id)
        del TODOS[todo_id]
        return '', 204

    def put(self, todo_id):
        args = parser.parse_args()
        task = {'task': args['task']}
        TODOS[todo_id] = {task, DateTime}
        return task, 201


# TodoList
# shows a list of all todos, and lets you POST to add new tasks
class TodoList(Resource):
    def get(self):
        return TODOS

    def post(self):
        args = parser.parse_args()
        todo_id = int(max(TODOS.keys()).lstrip('todo')) + 1
        todo_id = '%i' % todo_id
        TODOS[todo_id] = {'task': args['task'], 'creation':datetime.now().isoformat()}
        return TODOS[todo_id], 201

##
## Actually setup the Api resource routing here
##
api.add_resource(TodoList, '/todos')
api.add_resource(Todo, '/todos/<todo_id>')

if __name__ == '__main__':
    # Start application using 'FLASK_APP=server FLASK_ENV=development flask run'
    # Enable 'debug=True' for autoreload
    app.run(host='0.0.0.0', port=5000, debug=True)