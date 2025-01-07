# fetch.py
# store_leads.py
import sqlite3
import requests

def store_leads():
    # 1. Get the data
    print("Fetching data from server...")
    response = requests.get('http://127.0.0.1:5000/lead')
    data = response.json()
    leads = data['leads']  # Get the leads array
    
    if not leads:
        print("No leads found!")
        return
    
    # 2. Connect to database
    conn = sqlite3.connect('gym.db')
    cursor = conn.cursor()
    
    # 3. Create table automatically from first lead's keys
    first_lead = leads[0]
    columns = list(first_lead.keys())
    columns_sql = ", ".join([f"{col} TEXT" for col in columns])
    
    cursor.execute(f'''
    CREATE TABLE IF NOT EXISTS leads
    ({columns_sql})
    ''')
    
    # 4. Insert data
    placeholders = ", ".join(["?" for _ in columns])
    insert_sql = f"INSERT INTO leads VALUES ({placeholders})"
    
    for lead in leads:
        values = [lead[col] for col in columns]
        cursor.execute(insert_sql, values)
    
    # 5. Save and close
    conn.commit()
    conn.close()
    print(f"Successfully stored {len(leads)} leads!")

store_leads()