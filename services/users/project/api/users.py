from flask import Blueprint, jsonify, request, render_template
from sqlalchemy import exc

from project.api.models import User
from project import db

users_blueprint = Blueprint('users', __name__, template_folder='./templates')


@users_blueprint.route('/users/ping', methods=['GET'])
def ping_pong():
    return jsonify({
        'status': 'success',
        'message': 'pong'
    })


@users_blueprint.route('/users', methods=['GET'])
def get_all_users():
    """Get all users."""
    response_object = {
        'status': 'success',
        'data': {
            'users': [user.to_json() for user in User. query.all()]
        }
    }
    return jsonify(response_object), 200


@users_blueprint.route('/users', methods=['POST'])
def add_user():
    post_data = request.get_json()
    response_object = {
        'status': '',
        'message': ''
    }
    if not post_data or post_data.get('username') is None:
        response_object['status'] = 'fail'
        response_object['message'] = 'Invalid payload.'
        return jsonify(response_object), 400

    username = post_data.get('username')
    email = post_data.get('email')
    try:
        user = User.query.filter_by(email=email).first()
        if user:
            response_object['status'] = 'fail'
            response_object['message'] = 'Email already exist.'
            return jsonify(response_object), 400

        db.session.add(User(username=username, email=email))
        db.session.commit()
        response_object['status'] = 'success',
        response_object['message'] = f'{email} was added!'
        return jsonify(response_object), 201

    except exc.IntegrityError as e:
        db.session.rollback()
        response_object['status'] = 'fail'
        response_object['message'] = f'{e}'
        return jsonify(response_object), 400


@users_blueprint.route('/users/<user_id>', methods=['GET'])
def get_sinlge_user(user_id):
    """Get single user details."""
    response_object = {
        'status': '',
        'message': ''
    }
    try:
        user = User.query.filter_by(id=int(user_id)).first()
        if not user:
            response_object['status'] = 'fail'
            response_object['message'] = 'User does not exist.'
            return jsonify(response_object), 404

        response_object = {
            'status': 'success',
            'data': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'active': user.active
            }
        }
        return jsonify(response_object), 200
    except ValueError:
        response_object['status'] = 'fail'
        response_object['message'] = 'User does not exist.'
        return jsonify(response_object), 404


@users_blueprint.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        db.session.add(User(username=username, email=email))
        db.session.commit()

    users = User.query.all()
    return render_template('index.html', users=users)
