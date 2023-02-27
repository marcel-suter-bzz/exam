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

    def to_json(self) -> str:
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
    def fullname(self) -> str:
        return self._firstname + ' ' + self._lastname

    @property
    def firstname(self) -> str:
        return self._firstname

    @firstname.setter
    def firstname(self, value) -> None:
        self._firstname = value

    @property
    def lastname(self) -> str:
        return self._lastname

    @lastname.setter
    def lastname(self, value) -> None:
        self._lastname = value

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, value) -> None:
        self._email = value

    @property
    def role(self) -> str:
        return self._role

    @role.setter
    def role(self, value) -> None:
        self._role = value

    @property
    def department(self) -> str:
        return self._department

    @department.setter
    def department(self, value) -> None:
        if value is None:
            self._department = ''
        else:
            self._department = value
