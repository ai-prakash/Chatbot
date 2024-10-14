from flask import Flask, render_template, request, redirect, url_for
import requests  # Import requests library to make HTTP requests to FastAPI

app = Flask(__name__)

@app.route('/')
def home():
    # Render the HTML template
    return render_template('index.html')

@app.route('/order', methods=['POST'])
def order():
    # Retrieve form data
    order_data = {
        "item": request.form['item'],
        "quantity": request.form['quantity']
    }
    
    # Send the data to the FastAPI backend
    response = requests.post("http://127.0.0.1:8000/dialogflow", json={"queryResult": {"intent": {"displayName": "newOrder"}, "parameters": order_data}})
    
    # Check response from backend
    if response.status_code == 200:
        return redirect(url_for('home'))
    else:
        return "Error: Failed to place order", 500

if __name__ == '__main__':
    app.run(debug=True)
