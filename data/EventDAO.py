import json
import uuid
from dateutil import parser
from flask import current_app

from model.Event import Event


class EventDAO:
    """
    data access object for events

    author: Marcel Suter
    """

    def __init__(self):
        """
        constructor

        Parameters:

        """
        self._eventdict = {}
        self.load_events()

    def filtered_list(self, filter_value):
        """
        returns the filtered list of events
        :param filter_value: the filter to be applied
        :return: list of events
        """
        date = None
        if filter_value is not None:
            date = parser.parse(filter_value)
        filtered = []
        for (key, event) in self._eventdict.items():
            if date is None or event.timestamp.date() == date.date():
                filtered.append(event)
                if len(filtered) >= 20:
                    break
        return filtered

    def read_event(self, uuid):

        """
        reads an event by its uuid
        :param uuid: the unique key
        :return: Exam object
        """

        if uuid in self._eventdict:
            return self._eventdict[uuid]
        return None

    def save_event(self, event):
        """
        saves a new or changed event
        :param event:
        :return:
        """
        self.load_events()
        if event.event_uuid is None:
            event.event_uuid = str(uuid.uuid4())
        self._eventdict[event.event_uuid] = event
        jstring = Event.schema().dumps(list(self._examvent.values()), many=True)

        file = open(current_app.config['DATAPATH'] + 'events.json', 'w')
        file.write(jstring)
        file.close()

    def load_events(self):

        """
        loads all events into _eventlist
        :return: none
        :rtype: none
        """

        file = open(current_app.config['DATAPATH'] + 'events.json')
        events = json.load(file)
        for item in events:
            key = item['event_uuid']
            event = Event(
                item['event_uuid'],
                item['timestamp'],
                item['rooms'],
                item['supervisors']
            )
            self._eventdict[key] = event


if __name__ == '__main__':
    ''' Check if started directly '''
    pass
