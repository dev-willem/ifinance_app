from datetime import datetime
from . import db
from sqlalchemy.dialects.postgresql import JSONB

class EntrySAC(db.Model):
    __tablename__ = 'entry_sac'

    id = db.Column(db.BigInteger, primary_key=True)
    user_id = db.Column(db.BigInteger, db.ForeignKey('users.id'), nullable=False)
    type_id = db.Column(db.Integer, db.ForeignKey('type_operations.id'), nullable=False)

    principal_value = db.Column(db.Numeric(15, 2), nullable=False)
    interest_rate = db.Column(db.Numeric(5, 2), nullable=False)
    months = db.Column(db.Integer, nullable=False)   # <--- corrigido!
    is_monthly = db.Column(db.Boolean, default=True)
    start_date = db.Column(db.Date, nullable=True)
    output_data = db.Column(JSONB)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now)
    deleted_at = db.Column(db.DateTime, nullable=True)

    user = db.relationship('User', back_populates='operations')
    type_operation = db.relationship('TypeOperation', back_populates='entries')

    def __repr__(self):
        return f"<EntrySAC id={self.id} user={self.user_id}>"

    # ----------------- Calculation Methods ----------------- #

    @staticmethod
    def calculate_amortization(principal_value, months):
        """Cálculo da amortização constante"""
        return round(principal_value / months, 2)

    @staticmethod
    def calculate_total_interest(principal_value, months, interest_rate):
        """Cálculo total dos juros em um financiamento SAC"""
        total_interest = 0
        amortization = principal_value / months
        for _ in range(months):
            interest_frame = principal_value * (interest_rate / 100)
            total_interest += interest_frame
            principal_value -= amortization
        return round(total_interest, 2)

    @staticmethod
    def calculate_payments(principal_value, months, interest_rate):
        """Gera a lista de prestações (amortização + juros)"""
        payments = []
        amortization = principal_value / months
        for _ in range(months):
            interest_frame = principal_value * (interest_rate / 100)
            payment = amortization + interest_frame
            payments.append(round(payment, 2))
            principal_value -= amortization
        return payments
