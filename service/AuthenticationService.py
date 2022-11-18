import json
import logging
from datetime import datetime, timedelta

import jwt
import requests
from cryptography.hazmat.primitives import serialization
from flask import make_response, jsonify, current_app, request, g
from flask_restful import Resource, reqparse

from data.PersonDAO import PersonDAO
from util.authorization import make_access_token

parser = reqparse.RequestParser()
parser.add_argument('email', location='form', help='email')
parser.add_argument('password', location='form', help='password')


class AuthenticationService(Resource):
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

    def get(self):
        """
        get a jwt access and refresh token based on the MSAL idToken
        :return:
        """
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization']

        if not token:
            return make_response(jsonify({"message": "A valid token is missing!"}), 401)
        try:
            decoded_token = decode_idtoken(token[7:])
            email = decoded_token['email']
            access, role = make_access_token(email)

            if access is not None:
                refresh = jwt.encode({
                    'exp': datetime.utcnow() + timedelta(minutes=60)
                },
                    current_app.config['REFRESH_TOKEN_KEY'], "HS256"
                )

                return jsonify({
                    'access': access,
                    'refresh': refresh,
                    'email': email,
                    'role': role
                })

            return make_response('could not verify', 404, {'Authentication': '"login failed"'})

        except:
            return make_response(jsonify({"message": "EXAM/login: Invalid token!"}), 401)


def decode_idtoken(token):
    try:
        response = requests.get("https://login.microsoftonline.com/common/discovery/keys")
        keys = response.json()['keys']

        token_headers = jwt.get_unverified_header(token)
        token_alg = token_headers['alg']
        token_kid = token_headers['kid']
        public_key = None
        for key in keys:
            if key['kid'] == token_kid:
                public_key = key

        rsa_pem_key = jwt.algorithms.RSAAlgorithm.from_jwk(json.dumps(public_key))
        rsa_pem_key_bytes = rsa_pem_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )

        decoded_token = jwt.decode(
            token,
            key=rsa_pem_key_bytes,
            verify=True,
            algorithms=[token_alg],
            audience='8b113aa0-1d94-4f7b-a5e7-c7157e1c7b90',
            issuer="https://login.microsoftonline.com/12ea5aa9-906c-4d84-86d2-4713c6ae66d3/v2.0"
        )
        return decoded_token
    except Exception as e:
        logging.exception("EXAM: Error in jwt.decode")
        logging.exception(str(e))
        raise



if __name__ == '__main__':
    ''' Check if started directly '''
    pass
