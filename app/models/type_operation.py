from datetime import datetime
from . import db

class TypeOperation(db.Model):
    __tablename__ = 'type_operations'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now)

    entries = db.relationship('EntrySAC', back_populates='type_operation', cascade="all, delete-orphan")

    def __repr__(self):
        return f"<TypeOperation {self.name}>"
