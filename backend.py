from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

# MySQL database connection details
DB_HOST = 'localhost'
DB_USER = 'root'
DB_PASS = '1223'
DB_NAME = 'API_Project'

# Function to get the database connection
def get_db_connection():
    conn = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASS,
        database=DB_NAME
    )
    return conn

# Route for the homepage
@app.route('/')
def home():
    return render_template('index.html')  # This is your homepage

# Route to show the section options (1 or 2)
@app.route('/section/<int:section_id>')
def section(section_id):
    return render_template('choose_action.html', section_id=section_id)

# Route to handle the form page (Add, Delete, Update, Select)
@app.route('/form/<action>', methods=['GET', 'POST'])
def form(action):
    if action == 'add':
        if request.method == 'POST':
            # Extract form data
            item_id = request.form['Item_ID']
            item_name = request.form['Item_Name']
            item_type = request.form['Item_Type']
            amount = request.form['Amount']
            pay_date = request.form['Pay_DATE']
            who_payed = request.form['Who_Payed']

            # Add data to the database
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                '''INSERT INTO Expenses (Item_ID, Item_Name, Item_Type, Amount, Pay_DATE, Who_Payed)
                   VALUES (%s, %s, %s, %s, %s, %s)''',
                (item_id, item_name, item_type, amount, pay_date, who_payed)
            )
            conn.commit()
            cursor.close()
            conn.close()

            return redirect(url_for('home'))  # Redirect to homepage after successful form submission

        return render_template('add.html')  # The form for adding data

    elif action == 'delete':
        if request.method == 'POST':
            # Extract Item_ID to delete
            item_id = request.form['Item_ID']

            # Delete data from the database
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('DELETE FROM Expenses WHERE Item_ID = %s', (item_id,))
            conn.commit()
            cursor.close()
            conn.close()

            return redirect(url_for('home'))  # Redirect to homepage after deletion
        
        return render_template('delete.html')  # The form for deleting data

    elif action == 'update':
        if request.method == 'POST':
            # Extract form data
            item_id = request.form['Item_ID']
            item_name = request.form['Item_Name']
            item_type = request.form['Item_Type']
            amount = request.form['Amount']
            pay_date = request.form['Pay_DATE']
            who_payed = request.form['Who_Payed']

            # Update data in the database
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE Expenses
                SET Item_Name = %s, Item_Type = %s, Amount = %s, Pay_DATE = %s, Who_Payed = %s
                WHERE Item_ID = %s
            ''', (item_name, item_type, amount, pay_date, who_payed, item_id))
            conn.commit()
            cursor.close()
            conn.close()

            return redirect(url_for('home'))  # Redirect to homepage after successful update

        return render_template('update.html')  # The form for updating data

    elif action == 'select':
        # Get the search query from URL parameters
        search_query = request.args.get('search', '')  # Default empty if no search query is provided
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Search query logic
        if search_query:
            cursor.execute('''
                SELECT * FROM Expenses
                WHERE Item_Name LIKE %s
            ''', ('%' + search_query + '%',))  # Search both Item_Name and Item_Type
            expenses = cursor.fetchall()
            print("Search Query:", search_query)  # Debugging: Print search query
            print("Expenses Found:", expenses)    # Fetch the results
        else:
            expenses = []  # If no search query, set expenses to an empty list

        cursor.close()
        conn.close()

        return render_template('select.html', expenses=expenses)  # Render the template with filtered or empty data

if __name__ == '__main__':
    app.run(debug=True)
