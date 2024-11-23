from flask import Flask, request, jsonify, render_template
import mysql.connector

app = Flask(__name__)

# Database connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1223",
    database="API_Project"
)

cursor = db.cursor()

@app.route('/form', methods=['GET'])
def show_form():
    return render_template('form.html')

@app.route('/add-expense', methods=['POST'])
def add_expense():
    try:
        # Extract data from the form
        ID = request.form['ID']
        Item_ID = request.form['Item_ID']
        Item_Name = request.form['Item_Name']
        Item_Type = request.form['Item_Type']
        Amount = request.form['Amount']
        Pay_DATE = request.form['Pay_DATE']
        Who_Payed = request.form['Who_Payed']

        # Insert into the database
        query = """
            INSERT INTO Expenses (ID, Item_ID, Item_Name, Item_Type, Amount, Pay_DATE, Who_Payed)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        values = (ID, Item_ID, Item_Name, Item_Type, Amount, Pay_DATE, Who_Payed)
        cursor.execute(query, values)
        db.commit()

        return jsonify({"message": "Expense added successfully!"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
