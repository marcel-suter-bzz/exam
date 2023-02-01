import json

from flask import current_app

from data.PersonDAO import PersonDAO
from model.Exam import Exam


def condition(exam, student, teacher, date, status):
    """
    condition for filtering the examlist
    :param exam: an exam object to be examined
    :param student
    :param teacher
    :param date
    :param status
    :return: matches filter True/False
    """
    try:
        if student is not None and student != "":
            student = student.lower()
            if student not in exam.student.email.lower():
                return False
        if teacher is not None and teacher != "":
            teacher = teacher.lower()
            if teacher not in exam.teacher.email.lower():
                return False
        if date is not None and \
                date != "all" and \
                date != exam.event_uuid:
            return False
        if status is None or status == '':
            status = 'all'
        if exam.status in ['pendent', 'offen', 'abgegeben', 'erhalten'] and status not in ['open', 'all']:
            return False
        if exam.status in ['erledigt', 'pnab', 'gelöscht'] and status not in ['closed', 'all']:
            return False
    except Exception:
        print('Error in ExamDAO.condition')
    return True


class ExamDAO:
    """
    data access object for exams

    author: Marcel Suter
    """

    def __init__(self):
        """
        constructor

        Parameters:

        """
        self._examdict = {}
        self.load_exams()

    def filtered_list(self, student, teacher, date, status):
        """
        returns the filtered list of exams
        :param student
        :param teacher
        :param date
        :param status
        :return: list of exams
        """

        filtered = []
        for (key, exam) in self._examdict.items():
            if condition(exam, student, teacher, date, status):
                filtered.append(exam)
                if len(filtered) >= 100:
                    break
        return filtered

    def read_exam(self, uuid):
        """
        reads an exam by its uuid
        :param uuid: the unique key
        :return: Exam object
        """

        if uuid in self._examdict:
            return self._examdict[uuid]
        return None

    def save_exam(self, exam):
        """
        saves a new or changed exam
        :param exam:
        :return:
        """
        if exam.exam_uuid not in self._examdict:
            self._examdict[exam.exam_uuid] = exam
        old = self._examdict[exam.exam_uuid]

        if exam.event_uuid is not None:
            old.event_uuid = exam.event_uuid
        if exam.student is not None:
            old.student = exam.student
        if exam.teacher is not None:
            old.teacher = exam.teacher
        if exam.cohort is not None:
            old.cohort = exam.cohort
        if exam.module is not None:
            old.module = exam.module
        if exam.exam_num is not None:
            old.exam_num = exam.exam_num
        if exam.missed is not None:
            old.missed = exam.missed
        if exam.duration is not None and exam.duration != 0:
            old.duration = exam.duration
        if exam.room is not None:
            old.room = exam.room
        if exam.remarks is not None:
            old.remarks = exam.remarks
        if exam.tools is not None:
            old.tools = exam.tools
        if exam.status is not None:
            old.status = exam.status

        exams_json = '['
        for key in self._examdict:
            data = self._examdict[key].to_json(False)
            exams_json += data + ','
        exams_json = exams_json[:-1] + ']'

        file = open(current_app.config['DATAPATH'] + 'exams.json', 'w', encoding='UTF-8')
        file.write(exams_json)
        file.close()

    def load_exams(self):
        """
        loads all exams into _examlist
        :return: none
        :rtype: none
        """
        person_dao = PersonDAO()
        file = open(current_app.config['DATAPATH'] + 'exams.json', encoding='UTF-8')
        exams = json.load(file)
        for item in exams:
            key = item['exam_uuid']
            teacher = person_dao.read_person(item['teacher'])
            student = person_dao.read_person(item['student'])
            exam = Exam(
                exam_uuid=item['exam_uuid'],
                event_uuid=item['event_uuid'],
                teacher=teacher,
                student=student,
                cohort=item['cohort'],
                module=item['module'],
                exam_num=item['exam_num'],
                missed=item['missed'],
                duration=item['duration'],
                room=item['room'],
                remarks=item['remarks'],
                tools=item['tools'],
                status=item['status']
            )
            self._examdict[key] = exam


if __name__ == '__main__':
    ''' Check if started directly '''
    dao = ExamDAO()
    dao.load_exams()
