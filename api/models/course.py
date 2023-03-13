from ..utils import db
from enum import Enum


class courseList(Enum):
    FrontEnd = 'FrontEnd'
    BackEnd = 'BackEnd'
    Cloud = 'Cloud'


class Course(db.Model):
    __tablename__ = 'course'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.Enum(courseList), nullable=False, default='')
    instructor = db.Column(db.String(30), nullable=False)
    student = db.Column(db.Integer(), db.ForeignKey('student.id'))

    def __repr__(self):
        return f"Course('{self.name}')"

    def save(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_by_id(model, id):
        return model.query.get_or_404(id)

    @classmethod
    def delete_student_course(cls, id):
        model = cls.query.get(id)
        if not model:
            return False
        db.session.delete(model)
        db.session.commit()
        return True
