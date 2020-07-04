from flask import Flask, render_template, request, redirect, url_for, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import json
import sys

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://rohit:nfs@localhost:5432/todoapp'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Todo(db.Model):
	__tablename__='todos'

	id = db.Column(db.Integer, primary_key=True)
	description = db.Column(db.String(), nullable=False)
	completed = db.Column(db.Boolean, nullable=False, default=False)

	def __repr__(self):
		return f'<todo: id-{self.id}, description-{self.description}'


@app.route('/')
def index():
	return render_template('index.html', data=Todo.query.all())


@app.route('/todos/create', methods=['POST'])
def create_todo():
	error = False
	body = {}
	try:
		description = request.get_json()['description']
		todo = Todo(description=description)
		db.session.add(todo)
		db.session.commit()

		body = {'description': todo.description}
	except:
		error = True
		db.session.rollback()
		print(sys.exc_info())
	finally:
		db.session.close()

	if not error:
		return jsonify(body)
	else:
		abort(500)

if __name__ == '__main__':
	app.run(debug=True)