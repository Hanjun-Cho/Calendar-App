from validation import DateValidation, TaskIDValidation, BlockIDValidation, TaskDataFormatValidation, BlockDataFormatValidation
from flask import current_app, Blueprint, request, redirect
import database as db
api = Blueprint('api', __name__, url_prefix='/api')

@api.route("/<date>/tasks/<int:task_id>", methods=['GET', 'DELETE', 'POST'])
def task(date, task_id):
    DateValidation(date)
    TaskIDValidation(date, task_id)
    if request.method == 'GET':
        return db.get_task(date, task_id)
    elif request.method == 'DELETE':
        db.remove_task(date, task_id)
        return {'message': 'successfully removed task'}
    elif request.method == 'POST':
        task_data = request.form
        TaskDataFormatValidation(task_data, update=True)
        db.update_task(date, task_data, task_id)
        return db.get_task(task_data["Date"], task_id)

@api.route("/<date>/blocks/<int:block_id>", methods=['GET', 'DELETE', 'POST'])
def block(date, block_id):
    DateValidation(date)
    BlockIDValidation(date, block_id)
    if request.method == 'GET':
        return db.get_block(date, block_id)
    elif request.method == 'DELETE':
        db.remove_block(date, block_id)
        return {'message': 'successfully removed block'}
    elif request.method == 'POST':
        block_data = request.form
        BlockDataFormatValidation(block_data, update=True)
        db.update_block(date, block_data, block_id)
        return db.get_block(block_data["Date"], block_id)

@api.route("/<date>/tasks", methods=['GET', 'POST'])
def tasks(date):
    DateValidation(date)
    if request.method == 'GET':
        return db.get_all_tasks(date)
    if request.method == 'POST':
        task_data = request.form
        TaskDataFormatValidation(task_data, update=False)
        return db.get_task(date, db.add_task(date, task_data))

@api.route("/<date>/blocks", methods=['GET', 'POST'])
def blocks(date):
    DateValidation(date)
    if request.method == 'GET':
        return db.get_all_blocks(date)
    if request.method == 'POST':
        block_data = request.form
        BlockDataFormatValidation(block_data, update=False)
        return db.get_block(date, db.add_block(date, block_data))
