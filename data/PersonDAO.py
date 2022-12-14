from flask import current_app

from model.Person import Person
import json


def condition(person, filter_value):
    """
    condition for filtering the examlist
    :param person: a person object to be examined
    :param filter_value: the filter condition
    :return: matches filter True/False
    """
    filter_value = filter_value.lower()
    if filter_value in person.fullname.lower():
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

    def read_person(self, email):
        """
        reads a person by its email
        :param email:
        :return: Person object
        """
        person = None
        for (key, item) in self._peopledict.items():

            if key.casefold() == email.casefold():
                return item
        return person

    def load_people(self):
        """
                loads all exams into _examlist
                :return: none
                :rtype: none
                """
        file = open(current_app.config['DATAPATH'] + 'people.json', encoding='UTF-8')
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
