import json
import pickle
import pandas as pd
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask import render_template
import sqlite3
from datetime import datetime

from web3 import Web3


app = Flask(__name__)
CORS(app)
app = Flask(__name__, template_folder='../frontend')


# Initialize database and table with new fields
def init_db():
    conn = sqlite3.connect('visa_data.db')
    c = conn.cursor()

    # Create the table if it doesn't exist
    c.execute('''
        CREATE TABLE IF NOT EXISTS visa_requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            salutation TEXT,
            first_name TEXT,
            last_name TEXT,
            address TEXT,
            email TEXT,
            phone_number TEXT,
            name TEXT,
            passportID TEXT,
            visaType TEXT,
            input_json TEXT,
            prediction TEXT,
            timestamp TEXT
        )
    ''')

    # Commit and close connection
    conn.commit()
    conn.close()


init_db()

# Load model
model = pickle.load(open('ai_model/model.pkl', 'rb'))

# Web3 setup
w3 = Web3(Web3.HTTPProvider('https://worldchain-mainnet.g.alchemy.com/v2/qNoddOiT9woAL3DyvqryFpEwI3W7d6cO'))
contract_address = '0x7EF2e0048f5bAeDe046f6BF797943daF4ED8CB47'

with open('blockchain/abi.json') as f:
    abi = json.load(f)["abi"]

contract = w3.eth.contract(address=contract_address, abi=abi)

@app.route('/')
def home():
    return render_template('index.html')
@app.route('/predict', methods=['POST'])
def predict():
    try:
        input_data = request.get_json()

        # Extract only the required features
        required_features = ['age', 'income', 'nationality_code', 'travel_history']
        filtered_input = {k: input_data[k] for k in required_features if k in input_data}

        # Convert to DataFrame
        df = pd.DataFrame([filtered_input])

        # Prediction
        prediction = model.predict(df)[0]

        return jsonify({'prediction': int(prediction)})

    except Exception as e:
        print(f"Error during prediction: {e}")
        return jsonify({'error': 'An error occurred during prediction'}), 500

@app.route('/issue_visa_simulate', methods=['POST'])
def issue_visa_simulate():
    content = request.json
    try:
        # Extract all fields
        salutation = content.get("salutation", "")
        first_name = content.get("first_name", "")
        last_name = content.get("last_name", "")
        address = content.get("address", "")
        email = content.get("email", "")
        phone_number = content.get("phone_number", "")
        name = content.get("name", "")
        passportID = content.get("passportID", "")
        visaType = content.get("visaType", "")
        prediction = content.get("prediction", "")
        input_json = json.dumps(content)
        timestamp = datetime.now().isoformat()

        # Store all into DB
        conn = sqlite3.connect('visa_data.db')
        c = conn.cursor()
        c.execute('''
            INSERT INTO visa_requests (
                salutation, first_name, last_name, address, email, phone_number,
                name, passportID, visaType, input_json, prediction, timestamp
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            salutation, first_name, last_name, address, email, phone_number,
            name, passportID, visaType, input_json, prediction, timestamp
        ))
        conn.commit()
        conn.close()

        if str(prediction) == "0":
            return jsonify({
                "status": "Visa cannot be issued",
                "message": "Sorry, visa cannot be issued based on the prediction.",
                "db_status": "Stored successfully"
            })

        dummy_tx_hash = "0xcbcc2d77437bf48dd5bb8fd40eb987afbb368511f4d7190a0cc39b19b2decefb"

        return jsonify({
            "status": "Visa issued (simulated)",
            "tx_hash": dummy_tx_hash,
            "message": "This transaction was manually executed on Remix.",
            "db_status": "Stored successfully"
        })

    except Exception as e:
        print(f"Error during visa issue or storing data: {e}")
        return jsonify({'error': 'Failed during visa issue simulation or data storage'}), 500


@app.route('/get_all_visas', methods=['GET'])
def get_all_visas():
    try:
        # Connect to the database
        conn = sqlite3.connect('visa_data.db')
        c = conn.cursor()

        # Execute the query to fetch all data
        c.execute('SELECT id, salutation, first_name, last_name, address, email, phone_number, name, passportID, visaType, prediction, timestamp FROM visa_requests')

        # Fetch all the rows
        rows = c.fetchall()

        if not rows:
            print("No data found in visa_requests table.")
        
        # Close the connection after fetching the data
        conn.close()

        # Structure the fetched data into a list of dictionaries
        visa_list = []
        for row in rows:
            if len(row) == 12:
                visa_list.append({
                    "id": row[0],
                    "salutation": row[1],
                    "first_name": row[2],
                    "last_name": row[3],
                    "address": row[4],
                    "email": row[5],
                    "phone_number": row[6],
                    "name": row[7],
                    "passportID": row[8],
                    "visaType": row[9],
                    "prediction": row[10],
                    "timestamp": row[11]
                })
            else:
                print(f"Unexpected row format: {row}")

        # Return the structured data as a JSON response
        return jsonify(visa_list)

    except Exception as e:
        print(f"Error fetching visa data: {e}")
        return jsonify({'error': 'Failed to retrieve visa data'}), 500

if __name__ == '__main__':
    app.run(debug=True)




















"""
@app.route('/issue_visa_simulate', methods=['POST'])
def issue_visa_simulate():
    content = request.json
    try:
        # Extract data
        name = content.get("name", "")
        passportID = content.get("passportID", "")
        visaType = content.get("visaType", "")
        prediction = content.get("prediction", "")
        input_json = json.dumps(content)
        timestamp = datetime.now().isoformat()

        # Store the data in the database
        conn = sqlite3.connect('visa_data.db')
        c = conn.cursor()
        c.execute('''
            INSERT INTO visa_requests (name, passportID, visaType, input_json, prediction, timestamp)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (name, passportID, visaType, input_json, prediction, timestamp))
        conn.commit()
        conn.close()

        if str(prediction) != "1":
            return jsonify({
                "status": "Visa Denied",
                "message": "Sorry Visa Denied",
                "db_status": "Stored successfully"
            })

        # Simulate processing
        print(f"Issuing visa for: {name}")
        dummy_tx_hash = "0xcbcc2d77437bf48dd5bb8fd40eb987afbb368511f4d7190a0cc39b19b2decefb"

        return jsonify({
            "status": "Visa issued (simulated)",
            "tx_hash": dummy_tx_hash,
            "message": "This transaction was manually executed on Remix.",
            "db_status": "Stored successfully"
        })

    except Exception as e:
        print(f"Error during visa issue or storing data: {e}")
        return jsonify({'error': 'Failed during visa issue simulation or data storage'}), 500

"""