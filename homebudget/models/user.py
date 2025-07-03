from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from .. import db

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.Text, nullable=False)
    starting_budget = db.Column(db.Numeric(12,2), default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    categories = db.relationship('Category', back_populates='user', cascade='all, delete')
    expenses = db.relationship('Expense', back_populates='user', cascade='all, delete')

    def set_password(self, pw: str):
        self.password_hash = generate_password_hash(pw)
    def check_password(self, pw: str) -> bool:
        return check_password_hash(self.password_hash, pw)
