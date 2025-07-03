from .. import db

class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'))

    user = db.relationship('User', back_populates='categories')
    expenses = db.relationship('Expense', back_populates='category', cascade='all, delete')

    __table_args__ = (db.UniqueConstraint('user_id','name', name='uq_user_category'),)
