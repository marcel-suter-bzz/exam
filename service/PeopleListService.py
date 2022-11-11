from flask import make_response
from flask_restful import Resource

from data.PersonDAO import PersonDAO
from util.authorization import token_required, teacher_required


class PeoplelistService(Resource):
    """
    services for reading lists of people

    author: Marcel Suter
    """
    method_decorators = [token_required]

    def __init__(self):
        """
        constructor

        Parameters:

        """
        pass

    @teacher_required
    def get(self, filter_value):
        """
        get a list of people
        :param filter_value: the filter to be applied
        :return: JSON object with the people
        """
        person_dao = PersonDAO()
        peoplelist = person_dao.filtered_list(filter_value)
        people_json = '['
        for person in peoplelist:
            data = person.to_json()
            people_json += data + ','
        people_json = people_json[:-1] + ']'
        return make_response(
            people_json, 200
        )


if __name__ == '__main__':
    ''' Check if started directly '''
    pass
