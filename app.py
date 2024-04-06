from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from urllib.parse import quote_plus
from datetime import datetime

app = Flask(__name__)
fname = quote_plus('dbadmin')
password = quote_plus('dbImp!14@2')
url = 'mongodb://%s:%s@78.38.35.219:27017' % (fname, password)  # Specify the database name in the connection URL
client = MongoClient(url)
db = client.SM  # Specify the database
collection_users = db.users  # Specify the collections
collection_transactions = db.transactions

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/user', methods=['GET', 'POST'])
def user():
    if request.method == 'POST':
        search_stocknumber_id = request.form.get('search_stocknumber_id')
        if search_stocknumber_id:
            user_data = collection_users.find_one({"stocknumber_id": int(search_stocknumber_id)})
            if user_data:
                return render_template('user.html', user=user_data)
            else:
                error_message = "User with Stock Number ID {} not found.".format(search_stocknumber_id)
                return render_template('user.html', user=None, error_message=error_message)

        else:
            new_stocknumber_id = request.form.get('new_stocknumber_id')
            fullname = request.form.get('fullname')
            phonenumber = request.form.get('phonenumber')
            age = request.form.get('age')
            address = request.form.get('address')

            new_user = {
                "stocknumber_id": int(new_stocknumber_id),
                "fullname": fullname,
                "phonenumber": phonenumber,
                "age": int(age),
                "address": address
            }

            collection_users.insert_one(new_user)
            return redirect(url_for('user'))

    return render_template('user.html', user={})

@app.route('/addtransaction', methods=['GET', 'POST'])
def add_transaction():
    if request.method == 'POST':
        if 'search_transaction_id' in request.form:  # Check if the form is for searching transactions
            transaction_id = request.form.get('search_transaction_id')
            if transaction_id:
                transaction_data = collection_transactions.find_one({"transaction_id": int(transaction_id)})
                if transaction_data:
                    return render_template('addtransaction.html', transaction=transaction_data)
                else:
                    error_message = "Transaction with ID {} not found.".format(transaction_id)
                    return render_template('addtransaction.html', error_message=error_message)

        else:  # Form submission for adding new transaction
            stocknumber_id = request.form.get('stocknumber_id')
            transaction_id = request.form.get('transaction_id')
            time = request.form.get('time')
            trans_type = request.form.get('type')
            share_name = request.form.get('Share_name')
            amount = request.form.get('Amount')
            price = request.form.get('price')
            total_price = request.form.get('total_price')

            # Validate input data
            if not (stocknumber_id and transaction_id and time and trans_type and share_name and amount and price and total_price):
                error_message = "All fields are required."
                return render_template('addtransaction.html', error_message=error_message)

            try:
                # Convert numeric fields to appropriate data types
                stocknumber_id = int(stocknumber_id)
                transaction_id = int(transaction_id)
                amount = int(amount)
                price = float(price)
                total_price = float(total_price)
            except ValueError:
                error_message = "Invalid numeric value provided."
                return render_template('addtransaction.html', error_message=error_message)

            new_transaction = {
                "stocknumber_id": stocknumber_id,
                "transaction_id": transaction_id,
                "time": datetime.strptime(time, '%Y-%m-%dT%H:%M'),
                "type": trans_type,
                "Share_name": share_name,
                "Amount": amount,
                "price": price,
                "total_price": total_price
            }

            try:
                collection_transactions.insert_one(new_transaction)
                return redirect(url_for('add_transaction'))  # Redirect to the same route after insertion
            except Exception as e:
                error_message = "Error inserting data into database: {}".format(str(e))
                return render_template('addtransaction.html', error_message=error_message)

    return render_template('addtransaction.html')

@app.route('/searchtransaction', methods=['POST'])
def search_transaction():
    if request.method == 'POST':
        transaction_id = request.form.get('transaction_id')
        if transaction_id:
            transaction_data = collection_transactions.find_one({"transaction_id": int(transaction_id)})
            if transaction_data:
                return render_template('addtransaction.html', transaction=transaction_data)
            else:
                error_message = "Transaction with ID {} not found.".format(transaction_id)
                return render_template('addtransaction.html', error_message=error_message)
    # Redirect to add_transaction route if no transaction ID provided or if search is unsuccessful
    return redirect(url_for('add_transaction'))

if __name__ == '__main__':
    app.run()
