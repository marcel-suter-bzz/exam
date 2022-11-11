import json
from dataclasses import dataclass
from dateutil import parser
import datetime as datetime


@dataclass
class Event:
    """
    an event for exam repetitions

    author: Marcel Suter
    """

    event_uuid: str
    timestamp: datetime.datetime
    rooms: list
    supervisors: list

    def to_json(self):
        jstring = '{"event_uuid":"' + self.event_uuid + '",' + \
                  '"datetime": "' + self.timestamp + '",' + \
                  '"supervisors":' + json.dumps(self.supervisors) + ',' + \
                  '"rooms":' + json.dumps(self.rooms) + '}'
        return jstring


    @property
    def event_uuid(self):
        return self._event_uuid

    @event_uuid.setter
    def event_uuid(self, value):
        self._event_uuid = value

    @property
    def timestamp(self):
        return self._datetime.strftime("%d.%m.%Y %H:%M")

    @timestamp.setter
    def timestamp(self, value):
        self._datetime = parser.parse(value)

    @property
    def rooms(self):
        return self._rooms

    @rooms.setter
    def rooms(self, value):
        self._rooms = value

    @property
    def supervisors(self):
        return self._supervisors

    @supervisors.setter
    def supervisors(self, value):
        self._supervisors = value
if __name__ == '__main__':
    ''' Check if started directly '''
    pass
