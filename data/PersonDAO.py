from flask import current_app

from model.Person import Person
import json


def condition(person, filter_value):
    """
    condition for filtering the examlist
    :param person: an person object to be examined
    :param filter_value: the filter condition
    :return: matches filter True/False
    """
    filter_value = filter_value.lower()
    if (filter_value in person.firstname.lower() or
            filter_value in person.lastname.lower()
    ):
        return True
    return False


class PersonDAO:
    """
    data access object for person

    author: Marcel Suter
    """

    def __init__(self):
        """
        constructor

        Parameters:

        """
        self._peopledict = {}
        self.load_people()

    def filtered_list(self, filter_value):
        """
        returns the filtered list of people
        :param filter_value: the filter to be applied
        :return: list of people
        """

        filtered = []
        for (key, person) in self._peopledict.items():
            if condition(person, filter_value):
                filtered.append(person)
        return filtered

    def read_person(self, email, password=None):
        """
        reads a person by its email
        :param email:
        :return: Person object
        """
        person = None
        for (key, item) in self._peopledict.items():

            if (key == email and
                    password in [None, "1234"]  # FIXME
            ):
                return item
        return person

    def authenticate_person(self, email, password):
        """
        authenticates a user
        :param email:
        :param password:
        :return: authentication successful true/false
        """
        for (key, person) in self._peopledict.items():
            if (person.email == email and
                    "1234" == password):
                return True
        return False

    def save_person(self, person):
        """
        saves a new or changed person
        :param person:
        :return:
        """
        self._peopledict[person.email] = person
        jstring = Person.schema().dumps(list(self._peopledict.values()), many=True)
        file = open(current_app.config['DATAPATH'] + 'person.json', 'w')
        file.write(jstring)
        file.close()

    def load_people(self):
        """
                loads all exams into _examlist
                :return: none
                :rtype: none
                """
        file = open(current_app.config['DATAPATH'] + 'person.json')
        people = json.load(file)
        for item in people:
            key = item['email']
            person = Person(
                item['email'],
                item['firstname'],
                item['lastname'],
                item['role']
            )
            self._peopledict[key] = person


if __name__ == '__main__':
    ''' Check if started directly '''
    pass
