from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_restful import reqparse, abort, Api, Resource

from datetime import datetime

# importing MongoDB client
from flask_pymongo import PyMongo

from bson.json_util import dumps
from bson.objectid import ObjectId

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://localhost:27017/todo'
mongo = PyMongo(app)
api = Api(app)

CORS(app)

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
#        abort_if_todo_doesnt_exist(todo_id)
#        return TODOS[todo_id]
#        query = mongo.db.todo.count()
        query = mongo.db.todo.find(
#            {"task": 'Charlie'}
            {"_id": int(todo_id)}
        )
        return dumps(query)

    def delete(self, todo_id):
        query = mongo.db.todo.remove(
#            {"task": todo_id}
#            {"$or":[ {"_id": int(todo_id)}, {"_id": ObjectId(todo_id)}]}
            {"$or":[ {"_id": int(todo_id)}]}
        )
        return dumps(query), 204

    def put(self, todo_id):
        '''
        Function to update the user.
        '''
        data = parser.parse_args()
        query = mongo.db.todo.update(
            {"_id": int(todo_id)},
            {'task' : data['task']})
        return dumps(query)

# TodoList
# shows a list of all todos, and lets you POST to add new tasks
class TodoList(Resource):
    def get(self):
        query = mongo.db.todo.find()
        return dumps(query)

    def post(self):
        data = parser.parse_args()
#        args = parser.parse_args()
        task = data['task']
        todo_id = int(mongo.db.todo.count()) + 1
        try:
            status = mongo.db.todo.insert({
                "_id": todo_id,
                'task' : task,
                'created' : datetime.now().isoformat()
            })
            return dumps('Success')
        except Exception as e:
            return dumps({'error' : str(e)})

#        TODOS[todo_id] = {'task': args['task'], 'creation':datetime.now().isoformat()}
#        return TODOS[todo_id], 201

##
## Actually setup the Api resource routing here
##
api.add_resource(TodoList, '/todos')
api.add_resource(Todo, '/todos/<todo_id>')

if __name__ == '__main__':
    # Start application using 'FLASK_APP=server FLASK_ENV=development flask run'
    # Enable 'debug=True' for autoreload
    app.run(host='0.0.0.0', port=5000, debug=True)