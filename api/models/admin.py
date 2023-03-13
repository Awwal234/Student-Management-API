from ..utils import db


class Admin(db.Model):
    __tablename__ = 'admin'
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    email = db.Column(db.String(40), nullable=False, unique=True)
    password = db.Column(db.String(10), nullable=False, unique=True)
    type_acct = db.Column(db.String(5), nullable=False)

    def __repr__(self):
        return f"Admin('{self.email}')"

    def save(self):
        db.session.add(self)
        db.session.commit()