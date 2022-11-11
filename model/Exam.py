from dataclasses import dataclass
import datetime
import logging
from dateutil import parser
from model.Person import Person


@dataclass
class Exam(dict):
    """
    a exam to be taken
    
    author: Marcel Suter
    """

    exam_uuid: str
    event_uuid: str
    student: Person
    teacher: Person
    cohort: str
    module: str
    exam_num: str
    missed: datetime.date
    duration: int
    room: str
    remarks: str
    tools: str
    status: str

    def to_json(self, response=True):
        try:
            jstring = '{"exam_uuid":"' + self.exam_uuid + '",'
            jstring += '"cohort": "' + self.cohort + '", '
            jstring += '"module": "' + self.module + '", '
            jstring += '"exam_num": "' + self.exam_num + '", '
            jstring += '"missed": "' + self.missed.strftime("%Y-%m-%d") + '", '
            jstring += '"duration": ' + str(self.duration) + ', '
            jstring += '"room": "' + self.room + '",'
            jstring += '"remarks": "' + self.remarks + '", '
            jstring += '"tools": "' + self.tools + '", '
            jstring += '"event_uuid": "' + self.event_uuid + '", '
            jstring += '"status": "' + self.status + '", '
            if response:
                jstring += '"teacher": ' + self.teacher.to_json() + ',' + \
                           '"student": ' + self.student.to_json() + '}'
            else:
                jstring += '"teacher":"' + self.teacher.email + '",' + \
                           '"student":"' + self.student.email + '"}'
            return jstring

        except Exception as e:
            logging.exception("An exception was thrown!")
            logging.exception('exam_uuid: ' + self.exam_uuid)
            print('Error')
            return '{}'

    @property
    def exam_uuid(self):
        return self._exam_uuid

    @exam_uuid.setter
    def exam_uuid(self, value):
        self._exam_uuid = value

    @property
    def teacher(self):
        return self._teacher

    @teacher.setter
    def teacher(self, value):
        self._teacher = value

    @property
    def student(self):
        return self._student

    @student.setter
    def student(self, value):
        self._student = value

    @property
    def cohort(self):
        return self._cohort

    @cohort.setter
    def cohort(self, value):
        self._cohort = value

    @property
    def module(self):
        return self._module

    @module.setter
    def module(self, value):
        self._module = value

    @property
    def exam_num(self):
        return self._exam_num

    @exam_num.setter
    def exam_num(self, value):
        self._exam_num = value

    @property
    def missed(self):
        return self._missed

    @missed.setter
    def missed(self, value):
        if value is None or isinstance(value, datetime.date):
            self._missed = value
        else:
            self._missed = parser.parse(value)

    @property
    def duration(self):
        return self._duration

    @duration.setter
    def duration(self, value):
        self._duration = value

    @property
    def room(self):
        return self._room

    @room.setter
    def room(self, value):
        self._room = value

    @property
    def remarks(self):
        return self._remarks

    @remarks.setter
    def remarks(self, value):
        self._remarks = value

    @property
    def tools(self):
        return self._tools

    @tools.setter
    def tools(self, value):
        self._tools = value

    @property
    def event_uuid(self):
        return self._event_uuid

    @event_uuid.setter
    def event_uuid(self, value):
        self._event_uuid = value

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        self._status = value


if __name__ == '__main__':
    ''' Check if started directly '''
    pass
