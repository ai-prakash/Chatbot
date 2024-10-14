import sqlite3

def connect_db():
    conn = sqlite3.connect('orders.db')
    return conn

def init_db():
    """Initialize the database and create the orders table if it doesn't exist."""
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            item TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            status TEXT NOT NULL DEFAULT 'incomplete'
        )
    ''')
    conn.commit()
    conn.close()

def add_order(order_data):
    conn = connect_db()
    cursor = conn.cursor()
    # Add order to the database
    item = order_data['queryResult']['parameters']['item']
    quantity = int(order_data['queryResult']['parameters']['quantity'])
    cursor.execute("INSERT INTO orders (item, quantity) VALUES (?, ?)", (item, quantity))
    conn.commit()
    conn.close()
    return {"fulfillmentText": "Order added successfully."}

def remove_order(order_data):
    conn = connect_db()
    cursor = conn.cursor()
    # Remove order from the database
    item = order_data['queryResult']['parameters']['item']
    cursor.execute("DELETE FROM orders WHERE item = ?", (item,))
    conn.commit()
    conn.close()
    return {"fulfillmentText": "Order removed successfully."}

def complete_order(order_data):
    conn = connect_db()
    cursor = conn.cursor()
    # Mark the order as complete
    item = order_data['queryResult']['parameters']['item']
    cursor.execute("UPDATE orders SET status = 'complete' WHERE item = ?", (item,))
    conn.commit()
    conn.close()
    return {"fulfillmentText": "Order completed successfully."}

def track_order(order_data):
    conn = connect_db()
    cursor = conn.cursor()
    # Track the order in the database
    item = order_data['queryResult']['parameters']['item']
    cursor.execute("SELECT status FROM orders WHERE item = ?", (item,))
    status = cursor.fetchone()
    conn.close()
    
    # Return appropriate status message
    if status:
        return {"fulfillmentText": f"The status of your order is: {status[0]}."}
    else:
        return {"fulfillmentText": "Order not found."}
