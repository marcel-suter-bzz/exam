from flask import make_response, g
from flask_restful import Resource, reqparse

from data.ExamDAO import ExamDAO
from util.authorization import token_required


class ExamlistService(Resource):
    """
    services for reading lists of exams

    author: Marcel Suter
    """
    method_decorators = [token_required]

    def __init__(self):
        """
        constructor

        Parameters:

        """
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('student', location='args', help='student')
        self.parser.add_argument('teacher', location='args', help='teacher')
        self.parser.add_argument('date', location='args', help='date')
        self.parser.add_argument('status', location='args', help='status')

    def get(self):
        """
        get a list of exams
        :return: JSON object with the exams
        """
        args = self.parser.parse_args()

        if (g.user.role != 'teacher'):
            args['student'] = g.user.email
            args['teacher'] = ''
            args['date'] = ''
            args['status'] = '' 

        exam_dao = ExamDAO()
        examlist = exam_dao.filtered_list(args['student'], args['teacher'], args['date'], args['status'])
        exams_json = '['
        for exam in examlist:
            data = exam.to_json()
            exams_json += data + ','
        if len(exams_json) > 1:
            exams_json = exams_json[:-1] + ']'
        else:
            exams_json = "[]"
        return make_response(
            exams_json, 200
        )


if __name__ == '__main__':
    ''' Check if started directly '''
    pass
