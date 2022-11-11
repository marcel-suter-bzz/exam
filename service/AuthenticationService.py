from datetime import datetime, timedelta

import jwt
from flask import make_response, jsonify, current_app, request
from flask_restful import Resource, reqparse

from data.PersonDAO import PersonDAO

parser = reqparse.RequestParser()
parser.add_argument('email', location='form', help='email')
parser.add_argument('password', location='form', help='password')


class AuthorizationService(Resource):
    """
    services for Authentication

    author: Marcel Suter
    """

    def __init__(self):
        """
        constructor

        Parameters:

        """
        pass

    def post(self):
        """
        authenticates a user
        :return: http response
        """
        args = parser.parse_args()
        access, role = make_access_token(args.email)

        if access is not None:
            refresh = jwt.encode({
                'exp': datetime.utcnow() + timedelta(minutes=60)
            },
                current_app.config['REFRESH_TOKEN_KEY'], "HS256"
            )

            return jsonify({
                'access': access,
                'refresh': refresh,
                'email': args.email,
                'role': role
            })

        return make_response('could not verify', 404, {'Authentication': '"login failed"'})

    def get(self, email):
        """
        get a new access token using the refresh token
        :param email  the email address
        :return: access token
        """
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization']

        if not token:
            return make_response(jsonify({"message": "A valid token is missing!"}), 401)
        try:
            data = jwt.decode(token[7:], current_app.config['REFRESH_TOKEN_KEY'], algorithms=["HS256"])
            access, role = make_access_token(email)
            return jsonify({
                'access': access,
                'email': email,
                'role': role
            })
        except:
            pass

        return make_response(jsonify({"message": "Invalid token!"}), 401)

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
            'exp': datetime.utcnow() + timedelta(minutes=5)
        },
            current_app.config['ACCESS_TOKEN_KEY'], "HS256"
        )
        return access, person.role
    else:
        return None, "guest"

if __name__ == '__main__':
    ''' Check if started directly '''
    pass
