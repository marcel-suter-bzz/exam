from flask import Flask, send_from_directory
from flask_cors import CORS
from flask_restful import Api

from service.RefreshService import RefreshService
from service.EmailService import EmailService
from service.EventlistService import EventlistService
from service.AuthenticationService import AuthenticationService
from service.EventService import EventService
from service.ExamService import ExamService
from service.ExamlistService import ExamlistService
from service.PersonService import PersonService
from service.PeopleListService import PeoplelistService
from service.PrintService import PrintService

from logging.config import dictConfig

app = Flask(__name__)
CORS(app)
app.config.from_pyfile('./.env')
dictConfig(
    {
        "version": 1,
        "formatters": {
            "default": {
                "format": "[%(asctime)s] %(levelname)s in %(module)s: %(message)s",
            }
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stdout",
                "formatter": "default",
            },
            "file": {
                "class": "logging.FileHandler",
                "filename": app.config['LOG_FILE'],
                "formatter": "default",
            },

        },
        "root": {
            "level": app.config['LOG_LEVEL'],
            "handlers": ["console", "file"]
        },
    }
)
api = Api(app)

api.add_resource(AuthenticationService, '/login')
api.add_resource(RefreshService, '/refresh/<email>')
api.add_resource(ExamService, '/exam', '/exam/<exam_uuid>')
api.add_resource(ExamlistService, '/exams')
api.add_resource(PersonService, '/person')
api.add_resource(PeoplelistService, '/people/<filter_name>', '/people/<filter_name>/<filter_role>')
api.add_resource(EventService, '/event/<event_uuid>')
api.add_resource(EventlistService, '/events', '/events/<date>')
api.add_resource(EmailService, '/email', '/email/<exam_uuid>/<template>')
api.add_resource(PrintService, '/print', '/print/<exam_uuid>')


@app.route('/output/<filename>')
def page(filename):
    return send_from_directory('output', filename)


if __name__ == '__main__':
    app.run(debug=True)
