from flask import Flask, render_template, request, redirect, url_for

from models import (
    db,
    Member,
    Saving,
    Loan,
    LoanPayment,
    Maintenance,
    RecurringDeposit,
    Expense
)

from datetime import datetime
from sqlalchemy import func


# ==========================
# FLASK APPLICATION
# ==========================

app = Flask(__name__)


# ==========================
# ORACLE DATABASE CONFIGURATION
# ==========================

app.config["SQLALCHEMY_DATABASE_URI"] = (
    "oracle+oracledb://system:Ilarum3639@localhost:1521/"
    "?service_name=XE"
)

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


# Initialize database
db.init_app(app)


# Create database tables
with app.app_context():
    db.create_all()


# ==========================
# DASHBOARD
# ==========================

@app.route("/")
def dashboard():

    member_count = Member.query.filter_by(active="ACTIVE").count()

    total_savings = db.session.query(
        func.sum(Saving.amount)
    ).scalar() or 0

    total_loan = db.session.query(
        func.sum(Loan.outstanding_principal)
    ).filter(
        Loan.status == "ACTIVE"
    ).scalar() or 0

    total_interest = db.session.query(
        func.sum(LoanPayment.interest_amount)
    ).scalar() or 0

    total_maintenance = db.session.query(
        func.sum(Maintenance.amount)
    ).scalar() or 0

    total_rd = db.session.query(
        func.sum(RecurringDeposit.amount)
    ).scalar() or 0

    return render_template(
        "dashboard.html",
        member_count=member_count,
        total_savings=total_savings,
        total_loan=total_loan,
        total_interest=total_interest,
        total_maintenance=total_maintenance,
        total_rd=total_rd
    )


# ==========================
# MEMBERS
# ==========================

@app.route("/members")
def members():

    members = Member.query.order_by(
        Member.member_number
    ).all()

    return render_template(
        "members.html",
        members=members
    )


@app.route("/members/add", methods=["GET", "POST"])
def add_member():

    if request.method == "POST":

        member = Member(
            member_number=request.form["member_number"],
            name=request.form["name"],
            father_name=request.form["father_name"],
            phone=request.form["phone"],
            address=request.form["address"]
        )

        db.session.add(member)
        db.session.commit()

        return redirect(url_for("members"))

    return render_template("add_member.html")


# ==========================
# SAVINGS
# ==========================

@app.route("/savings", methods=["GET", "POST"])
def savings():

    members = Member.query.filter_by(active="ACTIVE").all()
    if request.method == "POST":

        saving = Saving(
            member_id=request.form["member_id"],
            month=request.form["month"],
            amount=float(request.form["amount"]),
            receipt_number=request.form["receipt_number"]
        )

        db.session.add(saving)
        db.session.commit()

        return redirect(url_for("savings"))

    records = Saving.query.order_by(
        Saving.payment_date.desc()
    ).all()

    return render_template(
        "savings.html",
        members=members,
        records=records
    )


# ==========================
# LOANS
# ==========================

@app.route("/loans")
def loans():

    loans = Loan.query.order_by(
        Loan.loan_date.desc()
    ).all()

    return render_template(
        "loans.html",
        loans=loans
    )


@app.route("/loans/add", methods=["GET", "POST"])
def add_loan():

    members = Member.query.filter_by(active=True).all()

    if request.method == "POST":

        amount = float(request.form["loan_amount"])

        loan = Loan(
            loan_number=request.form["loan_number"],
            member_id=request.form["member_NUMBER"],
            loan_amount=amount,
            outstanding_principal=amount,
            interest_rate=1.0
        )

        db.session.add(loan)
        db.session.commit()

        return redirect(url_for("loans"))

    return render_template(
        "add_loan.html",
        members=members
    )


# ==========================
# LOAN PAYMENT
# ==========================

@app.route("/loans/<int:loan_id>/payment", methods=["GET", "POST"])
def loan_payment(loan_id):

    loan = Loan.query.get_or_404(loan_id)

    if request.method == "POST":

        principal = float(
            request.form["principal_amount"]
        )

        opening = loan.outstanding_principal

        # Do not allow principal payment
        # greater than outstanding principal
        if principal > opening:
            principal = opening

        # 1% interest on opening outstanding principal
        interest = opening * loan.interest_rate / 100

        # Total payment
        total = principal + interest

        payment = LoanPayment(
            loan_id=loan.id,
            opening_principal=opening,
            interest_amount=interest,
            principal_amount=principal,
            total_amount=total,
            receipt_number=request.form["receipt_number"]
        )

        # Reduce outstanding principal
        loan.outstanding_principal = opening - principal

        # Close loan when principal becomes zero
        if loan.outstanding_principal <= 0:

            loan.outstanding_principal = 0

            loan.status = "CLOSED"

        db.session.add(payment)

        db.session.commit()

        return redirect(url_for("loans"))

    return render_template(
        "loan_payment.html",
        loan=loan
    )


# ==========================
# MAINTENANCE
# ==========================

@app.route("/maintenance", methods=["GET", "POST"])
def maintenance():

    members = Member.query.filter_by(active=True).all()

    if request.method == "POST":

        record = Maintenance(
            member_id=request.form["member_id"],
            month=request.form["month"],
            amount=float(request.form["amount"]),
            receipt_number=request.form["receipt_number"]
        )

        db.session.add(record)
        db.session.commit()

        return redirect(url_for("maintenance"))

    records = Maintenance.query.order_by(
        Maintenance.payment_date.desc()
    ).all()

    return render_template(
        "maintenance.html",
        members=members,
        records=records
    )


# ==========================
# RECURRING DEPOSIT
# ==========================

@app.route("/recurring-deposit", methods=["GET", "POST"])
def recurring_deposit():

    if request.method == "POST":

        record = RecurringDeposit(
            month=request.form["month"],
            amount=float(request.form["amount"]),
            bank_name=request.form["bank_name"],
            reference_number=request.form["reference_number"],
            remarks=request.form["remarks"]
        )

        db.session.add(record)
        db.session.commit()

        return redirect(url_for("recurring_deposit"))

    records = RecurringDeposit.query.order_by(
        RecurringDeposit.deposit_date.desc()
    ).all()

    return render_template(
        "recurring_deposit.html",
        records=records
    )


# ==========================
# RUN APPLICATION
# ==========================

if __name__ == "__main__":

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )