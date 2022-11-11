import json

import jwt
import requests
from cryptography.hazmat.primitives import serialization
from flask import make_response, jsonify, current_app, request, g
from flask_restful import Resource, reqparse

from data.PersonDAO import PersonDAO
from util.authorization import make_access_token


class RefreshService(Resource):
    """
    service to refresh the access token

    author: Marcel Suter
    """

    def __init__(self):
        """
        constructor

        Parameters:

        """
        pass

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
    except Exception as e:
        raise



if __name__ == '__main__':
    ''' Check if started directly '''
    pass
