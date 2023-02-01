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
    department: str = ' '
    role: str = ' '

    def to_json(self):
        person_json = '{{' \
                   '"email": "{email}",' \
                   '"firstname": "{firstname}",' \
                   '"lastname": "{lastname}",' \
                   '"fullname": "{fullname}",' \
                   '"department":"{department}",' \
                   '"role":"{role}"' \
                   '}}' \
            .format(
                email=self.email,
                firstname=self.firstname,
                lastname=self.lastname,
                fullname=self.fullname,
                department=self.department,
                role=self.role
            )
        return person_json

    @property
    def fullname(self):
        return self._firstname + ' ' + self._lastname

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

    @property
    def department(self):
        return self._department

    @department.setter
    def department(self, value):
        if value is None:
            self._department = ''
        else:
            self._department = value