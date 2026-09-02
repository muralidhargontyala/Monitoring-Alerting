from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


# =========================================================
# MEMBERS
# =========================================================

class Member(db.Model):

    __tablename__ = "members"

    id = db.Column(
        "member_id",
        db.Integer,
        primary_key=True
    )

    member_number = db.Column(
        "member_number",
        db.String(20),
        unique=True,
        nullable=False
    )

    name = db.Column(
        "name",
        db.String(100),
        nullable=False
    )

    father_name = db.Column(
        "father_name",
        db.String(100)
    )

    phone = db.Column(
        "phone",
        db.String(20)
    )

    address = db.Column(
        "address",
        db.String(250)
    )

    joining_date = db.Column(
        "joining_date",
        db.Date,
        default=datetime.utcnow
    )

    # Python property = active
    # Oracle column = STATUS
    active = db.Column(
        "STATUS",
        db.String(20),
        nullable=False,
        default="ACTIVE"
    )

    savings = db.relationship(
        "Saving",
        backref="member",
        lazy=True
    )

    loans = db.relationship(
        "Loan",
        backref="member",
        lazy=True
    )

    maintenance = db.relationship(
        "Maintenance",
        backref="member",
        lazy=True
    )


# =========================================================
# SAVINGS
# =========================================================

class Saving(db.Model):

    __tablename__ = "savings"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    member_id = db.Column(
        db.Integer,
        db.ForeignKey("members.member_id"),
        nullable=False
    )

    month = db.Column(
        db.String(20),
        nullable=False
    )

    amount = db.Column(
        db.Float,
        default=1000
    )

    payment_date = db.Column(
        db.Date,
        default=datetime.utcnow
    )

    receipt_number = db.Column(
        db.String(50)
    )


# =========================================================
# LOANS
# =========================================================

class Loan(db.Model):

    __tablename__ = "loans"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    loan_number = db.Column(
        db.String(50),
        unique=True,
        nullable=False
    )

    member_id = db.Column(
        db.Integer,
        db.ForeignKey("members.member_id"),
        nullable=False
    )

    loan_amount = db.Column(
        db.Float,
        nullable=False
    )

    outstanding_principal = db.Column(
        db.Float,
        nullable=False
    )

    interest_rate = db.Column(
        db.Float,
        default=1.0
    )

    loan_date = db.Column(
        db.Date,
        default=datetime.utcnow
    )

    status = db.Column(
        db.String(20),
        default="ACTIVE"
    )

    payments = db.relationship(
        "LoanPayment",
        backref="loan",
        lazy=True
    )


# =========================================================
# LOAN PAYMENTS
# =========================================================

class LoanPayment(db.Model):

    __tablename__ = "loan_payments"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    loan_id = db.Column(
        db.Integer,
        db.ForeignKey("loans.id"),
        nullable=False
    )

    payment_date = db.Column(
        db.Date,
        default=datetime.utcnow
    )

    opening_principal = db.Column(
        db.Float,
        nullable=False
    )

    interest_amount = db.Column(
        db.Float,
        nullable=False
    )

    principal_amount = db.Column(
        db.Float,
        nullable=False
    )

    total_amount = db.Column(
        db.Float,
        nullable=False
    )

    receipt_number = db.Column(
        db.String(50)
    )


# =========================================================
# MAINTENANCE
# =========================================================

class Maintenance(db.Model):

    __tablename__ = "maintenance"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    member_id = db.Column(
        db.Integer,
        db.ForeignKey("members.member_id"),
        nullable=False
    )

    month = db.Column(
        db.String(20),
        nullable=False
    )

    amount = db.Column(
        db.Float,
        default=1000
    )

    payment_date = db.Column(
        db.Date,
        default=datetime.utcnow
    )

    receipt_number = db.Column(
        db.String(50)
    )


# =========================================================
# RECURRING DEPOSIT
# =========================================================

class RecurringDeposit(db.Model):

    __tablename__ = "recurring_deposits"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    month = db.Column(
        db.String(20),
        nullable=False
    )

    amount = db.Column(
        db.Float,
        default=20000
    )

    deposit_date = db.Column(
        db.Date,
        default=datetime.utcnow
    )

    bank_name = db.Column(
        db.String(100)
    )

    reference_number = db.Column(
        db.String(100)
    )

    remarks = db.Column(
        db.String(250)
    )


# =========================================================
# EXPENSE
# =========================================================

class Expense(db.Model):

    __tablename__ = "expenses"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    expense_date = db.Column(
        db.Date,
        default=datetime.utcnow
    )

    category = db.Column(
        db.String(100)
    )

    description = db.Column(
        db.String(250)
    )

    amount = db.Column(
        db.Float,
        nullable=False
    )