from flask import Flask, render_template, request, redirect, url_for 
from pymongo import MongoClient
from urllib.parse import quote_plus
from datetime import datetime

app = Flask(__name__)
fname = quote_plus('dbadmin')
password = quote_plus('dbImp!14@2')
url = 'mongodb://%s:%s@78.38.35.219:27017' % (fname, password)
client = MongoClient(url)
db = client['SM']
collection_users = db['users']
collection_transactions = db['transactions']

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/user', methods=['GET', 'POST'])
def user():
    if request.method == 'POST':
        new_stocknumber_id = request.form.get('new_stocknumber_id')
        fullname = request.form.get('fullname')
        phonenumber = request.form.get('phonenumber')
        age = request.form.get('age')
        address = request.form.get('address')

        # Create a new user document to insert into the database
        new_user = {
            "stocknumber_id": int(new_stocknumber_id),
            "fullname": fullname,
            "phonenumber": phonenumber,
            "age": int(age),
            "address": address
        }

        # Insert the new user into the database
        collection_users.insert_one(new_user)

        # Redirect to the same route to display the user information after insertion
        return redirect(url_for('user'))

    # If it's a GET request or after form submission, render the template with an empty user object
    return render_template('user.html', user={})

@app.route('/addtransaction', methods=['GET', 'POST'])
def add_transaction():
    if request.method == 'POST':
        stocknumber_id = request.form.get('stocknumber_id')
        transaction_id = request.form.get('transaction_id')
        time = request.form.get('time')
        trans_type = request.form.get('type')
        share_name = request.form.get('Share_name')
        amount = request.form.get('Amount')
        price = request.form.get('price')
        total_price = request.form.get('total_price')
        
        new_transaction = {
            "stocknumber_id": int(stocknumber_id),
            "transaction_id": int(transaction_id),
            "time": datetime.strptime(time, '%Y-%m-%dT%H:%M:%SZ'),
            "type": trans_type,
            "Share_name": share_name,
            "Amount": int(amount),
            "price": int(price),
            "total_price": int(total_price)
        }

        collection_transactions.insert_one(new_transaction)
        return redirect(url_for('index'))

    return render_template('addtransaction.html')

if __name__ == '__main__':
    app.run()
