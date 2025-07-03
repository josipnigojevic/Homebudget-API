from datetime import datetime
from .. import db

class Expense(db.Model):
    __tablename__ = 'expenses'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(200), nullable=False)
    amount = db.Column(db.Numeric(12,2), nullable=False)
    date = db.Column(db.Date, default=datetime.utcnow)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id', ondelete='CASCADE'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'))

    category = db.relationship('Category', back_populates='expenses')
    user = db.relationship('User', back_populates='expenses')
