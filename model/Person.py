from dataclasses import dataclass


@dataclass
class Person(dict):
    """
    a student, teacher or supervisor
    
    author: Marcel Suter
    """

    email: str
    firstname: str = ' '
    lastname: str = ' '
    role: str = ' '

    def to_json(self):
        person_json = '{"email":"' + self.email + '",' + \
                      '"firstname": "' + self.firstname + '", ' + \
                      '"lastname": "' + self.lastname + '", ' + \
                      '"fullname": "' + self.firstname + ' ' + self.lastname + '", ' + \
                      '"role": "' + self.role + '"}'
        return person_json

    @property
    def firstname(self):
        return self._firstname

    @firstname.setter
    def firstname(self, value):
        self._firstname = value

    @property
    def lastname(self):
        return self._lastname

    @lastname.setter
    def lastname(self, value):
        self._lastname = value

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        self._email = value

    @property
    def role(self):
        return self._role

    @role.setter
    def role(self, value):
        self._role = value
