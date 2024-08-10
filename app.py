# Import libraries
from flask import Flask, request, url_for, redirect, render_template, Response, Request

# Sample data
transactions = [
    {'id': 1, 'date': '2023-06-01', 'amount': 100},
    {'id': 2, 'date': '2023-06-02', 'amount': -200},
    {'id': 3, 'date': '2023-06-03', 'amount': 300}
]

# Instantiate Flask functionality
app = Flask(__name__)

# Read operation
@app.route("/")
def get_transactions():
    return render_template("transactions.html", transactions=transactions)

# Create operation
@app.route("/add", methods=["GET", "POST"])
def add_transaction():
    if request.method == "GET":
        return render_template("form.html")
    elif request.method == "POST":
        content = request.form
        data = dict(id=len(transactions)+1)
        data.update(content.items())
        transactions.append(data)
        return redirect(url_for("get_transactions"))
    
# Update operation
@app.route("/edit/<int:transaction_id>", methods=["GET", "POST"])
def edit_transaction(transaction_id):
    if request.method == "GET":
        for t in transactions:
            if t['id'] == transaction_id:
                return render_template("edit.html", transaction=t)
    elif request.method == "POST":
        content = request.form
        for t in transactions:
            if t['id'] == transaction_id:
                for k, v in content.items():
                    t[k] = v
                return redirect(url_for("get_transactions"))

# Delete operation
@app.route("/delete/<int:transaction_id>")
def delete_transaction(transaction_id):
    transaction_copy = transactions.copy()
    for t in transaction_copy:
        if t['id'] == transaction_id:
            transactions.remove(t)
            return redirect(url_for("get_transactions"))
        
# Search Transaction
@app.route("/search", methods=["GET", "POST"])
def search_transactions():
    if request.method == "GET":
        return render_template("search.html")
    elif request.method == "POST":
        minimum, maximum = [float(v) for v in request.form.values()]
        filtered_transactions = [t for t in transactions if t['amount'] >= minimum and t['amount'] <= maximum]
        return render_template("transactions.html", transactions=filtered_transactions)
    
# Calculate total balance
@app.route("/balance")
def total_balance():
    total = sum([float(t['amount']) for t in transactions])
    return render_template("transactions.html", transactions=transactions, total_balance=total)

if __name__ == "__main__":
    # Run the Flask app
    app.run(debug=True)