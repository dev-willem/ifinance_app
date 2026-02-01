from datetime import datetime
from . import db
from sqlalchemy import JSON

class EntryProfit(db.Model):
    __tablename__ = 'entry_profit'
    
    id = db.Column(db.BigInteger, primary_key=True)
    user_id = db.Column(db.BigInteger, db.ForeignKey('users.id'), nullable=False)
    type_id = db.Column(db.Integer, db.ForeignKey('type_operations.id'), nullable=False)
    
    revenue = db.Column(db.Numeric(15, 2), nullable=False)
    fixed_costs = db.Column(db.Numeric(15, 2), nullable=False)
    variable_costs = db.Column(db.Numeric(15, 2), nullable=False)
    taxes = db.Column(db.Numeric(15, 2), nullable=False)
    output_data = db.Column(JSON)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now)
    deleted_at = db.Column(db.DateTime, nullable=True)

    user = db.relationship('User')
    type_operation = db.relationship('TypeOperation')

    def __repr__(self):
        return f"<EntryProfit id={self.id} user={self.user_id}>"
