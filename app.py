from flask import Flask, render_template, send_from_directory
from flask_cors import CORS
from flask_restful import  Api

from service.EmailService import EmailService
from service.EventlistService import EventlistService
from service.AuthenticationService import AuthorizationService
from service.EventService import EventService
from service.ExamService import ExamService
from service.ExamlistService import ExamlistService
from service.PersonService import PersonService
from service.PeopleListService import PeoplelistService
from service.PrintService import PrintService

app = Flask(__name__)
CORS(app)
app.config.from_pyfile('./.env')
api = Api(app)

api.add_resource(ExamService, '/exam', '/exam/<exam_uuid>')
api.add_resource(ExamlistService, '/exams')
api.add_resource(PersonService, '/person')
api.add_resource(PeoplelistService, '/people/<filter_value>')
api.add_resource(AuthorizationService, '/login', '/login/<email>')
api.add_resource(EventService, '/event/<event_uuid>')
api.add_resource(EventlistService, '/events', '/events/<date>')
api.add_resource(EmailService, '/email', '/email/<exam_uuid>/<type>')
api.add_resource(PrintService, '/print', '/print/<exam_uuid>')

@app.route('/')
def home():
   return render_template('index.html')

@app.route('/output/<filename>')
def page(filename):
    return send_from_directory('output', filename)

if __name__ == '__main__':
    app.run(debug=True)
