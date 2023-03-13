# A grade model for student with relationship
# Admin access only to update student grades by id
from ..utils import db


class Grade(db.Model):
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    score = db.Column(db.String(10), nullable=False)
    student = db.Column(db.Integer(), db.ForeignKey('student.id'))

    def __repr__(self):
        return f"Grade: {self.score}"

    def save(self):
        db.session.add(self)
        db.session.commit()
