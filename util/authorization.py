from functools import wraps
import jwt
from flask import jsonify, request, make_response, g, current_app
from data.PersonDAO import PersonDAO
from datetime import datetime, timedelta


def token_required(func):
    """
    checks if the authorization token is valid
    :param func: callback function
    :return:
    """

    @wraps(func)
    def decorator(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization']

        if not token:
            return make_response(jsonify({"message": "A valid token is missing!"}), 401)
        try:
            data = jwt.decode(token[7:], current_app.config['ACCESS_TOKEN_KEY'], algorithms=["HS256"])
            email = data['email']
            person_dao = PersonDAO()
            g.user = person_dao.read_person(email)
        except:
            return make_response(jsonify({"message": "EXAM/auth: Invalid token!"}), 401)

        return func(*args, **kwargs)

    return decorator


def teacher_required(func):
    @wraps(func)
    def wrap(*args, **kwargs):
        if not g.user.role == 'teacher':
            return make_response(jsonify({"message": "not allowed for students"}), 401)
        return func(*args, **kwargs)

    return wrap

def make_access_token(email):
    """
    creates an access token
    :param email: the email address of the user
    :return: token
    """
    person_dao = PersonDAO()
    person = person_dao.read_person(email)
    if person is not None:
        access = jwt.encode({
            'email': email,
            'role': person.role,
            'exp': datetime.utcnow() + timedelta(minutes=15)
        },
            current_app.config['ACCESS_TOKEN_KEY'], "HS256"
        )
        return access, person.role
    else:
        return None, "guest"

if __name__ == '__main__':
    ''' Check if started directly '''
    pass
