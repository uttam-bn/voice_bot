import sqlite3

def init_db():
    conn = sqlite3.connect('complaints.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS complaints (
            id TEXT PRIMARY KEY,
            dealer_name TEXT,
            company TEXT,
            vehicle_name TEXT,
            odometer_reading TEXT,
            days_since_purchase TEXT,
            dealer_address TEXT,
            infotainment_serial_no TEXT UNIQUE,
            city TEXT
        )
    ''')
    conn.commit()
    conn.close()

def store_complaint(complaint_id, dealer_name, company, vehicle_name, odometer_reading, days_since_purchase, dealer_address, infotainment_serial_no, city):
    conn = sqlite3.connect('complaints.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO complaints (id, dealer_name, company, vehicle_name, odometer_reading, days_since_purchase, dealer_address, infotainment_serial_no, city)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (complaint_id, dealer_name, company, vehicle_name, odometer_reading, days_since_purchase, dealer_address, infotainment_serial_no, city))
    conn.commit()
    conn.close()

def is_duplicate_complaint(infotainment_serial_no):
    conn = sqlite3.connect('complaints.db')
    c = conn.cursor()
    c.execute('SELECT * FROM complaints WHERE infotainment_serial_no = ?', (infotainment_serial_no,))
    result = c.fetchone()
    conn.close()
    return result is not None

def get_complaint_id(infotainment_serial_no):
    conn = sqlite3.connect('complaints.db')
    c = conn.cursor()
    c.execute('SELECT id FROM complaints WHERE infotainment_serial_no = ?', (infotainment_serial_no,))
    result = c.fetchone()
    conn.close()
    return result[0] if result else None

def get_complaint_details(complaint_id):
    conn = sqlite3.connect('complaints.db')
    c = conn.cursor()
    c.execute('SELECT * FROM complaints WHERE id = ?', (complaint_id,))
    result = c.fetchone()
    conn.close()
    return result

def get_total_complaints():
    conn = sqlite3.connect('complaints.db')
    c = conn.cursor()
    c.execute('SELECT COUNT(*) FROM complaints')
    result = c.fetchone()
    conn.close()
    return result[0] if result else 0
