import sqlite3
import os
from datetime import datetime

def create_connection():
    """Create a database connection to the SQLite database"""
    conn = None
    try:
        # Check if database directory exists, if not create it
        if not os.path.exists('data'):
            os.makedirs('data')
            
        conn = sqlite3.connect('data/lucero_glam_studio.db')
        return conn
    except sqlite3.Error as e:
        print(e)
    return conn

def create_tables():
    """Create tables if they don't exist"""
    conn = create_connection()
    if conn is not None:
        try:
            cursor = conn.cursor()
            
            # Create clients table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS clients (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    first_name TEXT NOT NULL,
                    last_name TEXT NOT NULL,
                    phone_number TEXT NOT NULL,
                    description TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Create appointments table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS appointments (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    client_id INTEGER,
                    service_id INTEGER,
                    appointment_date TIMESTAMP NOT NULL,
                    deposit_amount REAL NOT NULL,
                    notes TEXT,
                    status TEXT DEFAULT 'scheduled',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (client_id) REFERENCES clients (id),
                    FOREIGN KEY (service_id) REFERENCES services (id)
                )
            ''')
            
            # Create services table (for future use)
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS services (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    description TEXT,
                    price REAL NOT NULL,
                    duration_minutes INTEGER NOT NULL
                )
            ''')
            
            # Create payments table (for future use)
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS payments (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    appointment_id INTEGER,
                    amount REAL NOT NULL,
                    payment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    payment_method TEXT,
                    FOREIGN KEY (appointment_id) REFERENCES appointments (id)
                )
            ''')
            
            # Create invoices table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS invoices (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    appointment_id INTEGER,
                    total_amount REAL NOT NULL,
                    paid_amount REAL NOT NULL,
                    change_amount REAL NOT NULL,
                    late_fee REAL DEFAULT 0,
                    discount REAL DEFAULT 0,
                    invoice_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (appointment_id) REFERENCES appointments (id)
                )
            ''')
            
            conn.commit()
        except sqlite3.Error as e:
            print(f"Database error: {e}")
        finally:
            conn.close()
    else:
        print("Error: Cannot create database connection.")

# Client CRUD operations
def add_client(first_name, last_name, phone_number, description=""):
    """Add a new client to the database"""
    conn = create_connection()
    if conn is not None:
        try:
            cursor = conn.cursor()
            sql = '''
                INSERT INTO clients (first_name, last_name, phone_number, description)
                VALUES (?, ?, ?, ?)
            '''
            cursor.execute(sql, (first_name, last_name, phone_number, description))
            conn.commit()
            return cursor.lastrowid
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return None
        finally:
            conn.close()
    else:
        print("Error: Cannot create database connection.")
        return None

def get_all_clients():
    """Get all clients from the database"""
    conn = create_connection()
    if conn is not None:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM clients ORDER BY last_name, first_name")
            rows = cursor.fetchall()
            return rows
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return []
        finally:
            conn.close()
    else:
        print("Error: Cannot create database connection.")
        return []

def get_client_by_id(client_id):
    """Get a client by ID"""
    conn = create_connection()
    if conn is not None:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM clients WHERE id = ?", (client_id,))
            client = cursor.fetchone()
            return client
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return None
        finally:
            conn.close()
    else:
        print("Error: Cannot create database connection.")
        return None

def update_client(client_id, first_name, last_name, phone_number, description):
    """Update a client's information"""
    conn = create_connection()
    if conn is not None:
        try:
            cursor = conn.cursor()
            sql = '''
                UPDATE clients
                SET first_name = ?, last_name = ?, phone_number = ?, description = ?
                WHERE id = ?
            '''
            cursor.execute(sql, (first_name, last_name, phone_number, description, client_id))
            conn.commit()
            return cursor.rowcount
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return 0
        finally:
            conn.close()
    else:
        print("Error: Cannot create database connection.")
        return 0

def delete_client(client_id):
    """Delete a client from the database"""
    conn = create_connection()
    if conn is not None:
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM clients WHERE id = ?", (client_id,))
            conn.commit()
            return cursor.rowcount
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return 0
        finally:
            conn.close()
    else:
        print("Error: Cannot create database connection.")
        return 0

def check_client_exists(first_name, last_name, phone_number):
    """Check if a client with the same name and last name already exists"""
    conn = create_connection()
    if conn is not None:
        try:
            cursor = conn.cursor()
            # Buscar solo por nombre completo (caso exacto)
            cursor.execute("""
                SELECT * FROM clients 
                WHERE first_name = ? AND last_name = ?
            """, (first_name, last_name))
            result = cursor.fetchone()
            return result is not None
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return False
        finally:
            conn.close()
    else:
        print("Error: Cannot create database connection.")
        return False

def search_clients(search_term):
    """Search for clients by name or phone number"""
    conn = create_connection()
    if conn is not None:
        try:
            cursor = conn.cursor()
            search_pattern = f"%{search_term}%"
            sql = '''
                SELECT * FROM clients 
                WHERE first_name LIKE ? OR last_name LIKE ? OR phone_number LIKE ?
                ORDER BY last_name, first_name
            '''
            cursor.execute(sql, (search_pattern, search_pattern, search_pattern))
            rows = cursor.fetchall()
            return rows
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return []
        finally:
            conn.close()
    else:
        print("Error: Cannot create database connection.")
        return []

# Service CRUD operations
def add_service(name, price, duration_minutes, description=""):
    """Add a new service to the database"""
    conn = create_connection()
    if conn is not None:
        try:
            cursor = conn.cursor()
            sql = '''
                INSERT INTO services (name, price, duration_minutes, description)
                VALUES (?, ?, ?, ?)
            '''
            cursor.execute(sql, (name, float(price), int(duration_minutes), description))
            conn.commit()
            return cursor.lastrowid
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return None
        finally:
            conn.close()
    else:
        print("Error: Cannot create database connection.")
        return None

def get_all_services():
    """Get all services from the database"""
    conn = create_connection()
    if conn is not None:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM services ORDER BY name")
            rows = cursor.fetchall()
            return rows
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return []
        finally:
            conn.close()
    else:
        print("Error: Cannot create database connection.")
        return []

def get_service_by_id(service_id):
    """Get a service by ID"""
    conn = create_connection()
    if conn is not None:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM services WHERE id = ?", (service_id,))
            service = cursor.fetchone()
            return service
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return None
        finally:
            conn.close()
    else:
        print("Error: Cannot create database connection.")
        return None

def update_service(service_id, name, price, duration_minutes, description):
    """Update a service's information"""
    conn = create_connection()
    if conn is not None:
        try:
            cursor = conn.cursor()
            sql = '''
                UPDATE services
                SET name = ?, price = ?, duration_minutes = ?, description = ?
                WHERE id = ?
            '''
            cursor.execute(sql, (name, float(price), int(duration_minutes), description, service_id))
            conn.commit()
            return cursor.rowcount
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return 0
        finally:
            conn.close()
    else:
        print("Error: Cannot create database connection.")
        return 0

def delete_service(service_id):
    """Delete a service from the database"""
    conn = create_connection()
    if conn is not None:
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM services WHERE id = ?", (service_id,))
            conn.commit()
            return cursor.rowcount
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return 0
        finally:
            conn.close()
    else:
        print("Error: Cannot create database connection.")
        return 0

def search_services(search_term):
    """Search for services by name"""
    conn = create_connection()
    if conn is not None:
        try:
            cursor = conn.cursor()
            search_pattern = f"%{search_term}%"
            sql = '''
                SELECT * FROM services 
                WHERE name LIKE ?
                ORDER BY name
            '''
            cursor.execute(sql, (search_pattern,))
            rows = cursor.fetchall()
            return rows
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return []
        finally:
            conn.close()
    else:
        print("Error: Cannot create database connection.")
        return []

# Appointment CRUD operations
def add_appointment(client_id, service_id, appointment_date, deposit_amount, notes=""):
    """Add a new appointment to the database"""
    print(f"DEBUG: Adding appointment - client_id: {client_id}, service_id: {service_id}, date: {appointment_date}, deposit: {deposit_amount}")
    conn = create_connection()
    if conn is not None:
        try:
            # First check if there's already an appointment at the same time
            cursor = conn.cursor()
            # We'll check appointments within the same hour
            # Convert appointment_date to datetime object if it's a string
            if isinstance(appointment_date, str):
                print(f"DEBUG: Converting string date: {appointment_date}")
                appointment_datetime = datetime.strptime(appointment_date, "%Y-%m-%d %H:%M")
            else:
                print(f"DEBUG: Using datetime object: {appointment_date}")
                appointment_datetime = appointment_date
                
            # Format the appointment date for database storage
            appointment_date_str = appointment_datetime.strftime("%Y-%m-%d %H:%M")
            print(f"DEBUG: Formatted date string: {appointment_date_str}")
                
            # Calculate start and end of the hour for checking conflicts
            hour_start = appointment_datetime.replace(minute=0, second=0, microsecond=0)
            hour_end = hour_start.replace(hour=hour_start.hour + 1)
            
            hour_start_str = hour_start.strftime("%Y-%m-%d %H:%M")
            hour_end_str = hour_end.strftime("%Y-%m-%d %H:%M")
            print(f"DEBUG: Checking conflicts between {hour_start_str} and {hour_end_str}")
            
            # Check for existing appointments in this time slot
            cursor.execute("""
                SELECT COUNT(*) FROM appointments 
                WHERE appointment_date BETWEEN ? AND ?
                AND status = 'scheduled'
            """, (hour_start_str, hour_end_str))
            
            count = cursor.fetchone()[0]
            print(f"DEBUG: Found {count} existing appointments in this time slot")
            if count > 0:
                conn.close()
                print("DEBUG: Time conflict detected")
                return -1  # Indicates time conflict
            
            # If no conflict, proceed with adding the appointment
            print("DEBUG: No conflicts, proceeding with insertion")
            sql = '''
                INSERT INTO appointments (client_id, service_id, appointment_date, deposit_amount, notes, status)
                VALUES (?, ?, ?, ?, ?, ?)
            '''
            print(f"DEBUG: SQL parameters: {client_id}, {service_id}, {appointment_date_str}, {float(deposit_amount)}, {notes}, scheduled")
            cursor.execute(sql, (client_id, service_id, appointment_date_str, float(deposit_amount), notes, "scheduled"))
            conn.commit()
            last_id = cursor.lastrowid
            print(f"DEBUG: Appointment added successfully with ID: {last_id}")
            conn.close()
            return last_id
        except sqlite3.Error as e:
            print(f"DATABASE ERROR: {e}")
            if conn:
                conn.close()
            return None
        except Exception as e:
            print(f"GENERAL ERROR: {e}")
            import traceback
            print(f"TRACEBACK: {traceback.format_exc()}")
            if conn:
                conn.close()
            return None
    else:
        print("ERROR: Cannot create database connection.")
        return None

def get_all_appointments():
    """Get all appointments from the database"""
    conn = create_connection()
    if conn is not None:
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT a.id, c.first_name, c.last_name, s.name, a.appointment_date, a.deposit_amount, a.notes, a.status 
                FROM appointments a
                JOIN clients c ON a.client_id = c.id
                JOIN services s ON a.service_id = s.id
                ORDER BY a.appointment_date DESC
            """)
            rows = cursor.fetchall()
            return rows
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return []
        finally:
            conn.close()
    else:
        print("Error: Cannot create database connection.")
        return []

def get_appointment_by_id(appointment_id):
    """Get an appointment by ID"""
    conn = create_connection()
    if conn is not None:
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT a.id, a.client_id, a.service_id, a.appointment_date, a.deposit_amount, a.notes, a.status, 
                       c.first_name, c.last_name, s.name as service_name, s.price
                FROM appointments a
                JOIN clients c ON a.client_id = c.id
                JOIN services s ON a.service_id = s.id
                WHERE a.id = ?
            """, (appointment_id,))
            appointment = cursor.fetchone()
            return appointment
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return None
        finally:
            conn.close()
    else:
        print("Error: Cannot create database connection.")
        return None

def update_appointment(appointment_id, client_id, service_id, appointment_date, deposit_amount, notes, status):
    """Update an appointment's information"""
    conn = create_connection()
    if conn is not None:
        try:
            # First check if there's already another appointment at the same time (excluding this one)
            cursor = conn.cursor()
            
            # Convert appointment_date to datetime object if it's a string
            if isinstance(appointment_date, str):
                appointment_datetime = datetime.strptime(appointment_date, "%Y-%m-%d %H:%M")
            else:
                appointment_datetime = appointment_date
                
            # Calculate start and end of the hour for checking conflicts
            hour_start = appointment_datetime.replace(minute=0, second=0, microsecond=0)
            hour_end = hour_start.replace(hour=hour_start.hour + 1)
            
            # Check for existing appointments in this time slot (excluding this one)
            cursor.execute("""
                SELECT COUNT(*) FROM appointments 
                WHERE appointment_date BETWEEN ? AND ?
                AND id != ?
                AND status = 'scheduled'
            """, (hour_start.strftime("%Y-%m-%d %H:%M"), hour_end.strftime("%Y-%m-%d %H:%M"), appointment_id))
            
            count = cursor.fetchone()[0]
            if count > 0:
                return -1  # Indicates time conflict
            
            # If no conflict, proceed with updating the appointment
            sql = '''
                UPDATE appointments
                SET client_id = ?, service_id = ?, appointment_date = ?, deposit_amount = ?, notes = ?, status = ?
                WHERE id = ?
            '''
            cursor.execute(sql, (client_id, service_id, appointment_datetime.strftime("%Y-%m-%d %H:%M"), 
                               float(deposit_amount), notes, status, appointment_id))
            conn.commit()
            return cursor.rowcount
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return 0
        finally:
            conn.close()
    else:
        print("Error: Cannot create database connection.")
        return 0

def delete_appointment(appointment_id):
    """Delete an appointment from the database"""
    conn = create_connection()
    if conn is not None:
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM appointments WHERE id = ?", (appointment_id,))
            conn.commit()
            return cursor.rowcount
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return 0
        finally:
            conn.close()
    else:
        print("Error: Cannot create database connection.")
        return 0

def get_appointments_by_date(date):
    """Get all appointments for a specific date"""
    conn = create_connection()
    if conn is not None:
        try:
            cursor = conn.cursor()
            # Format date as YYYY-MM-DD for SQL query
            date_str = date.strftime("%Y-%m-%d")
            cursor.execute("""
                SELECT a.id, c.first_name, c.last_name, s.name, a.appointment_date, a.deposit_amount, a.notes, a.status,
                       s.duration_minutes, s.price
                FROM appointments a
                JOIN clients c ON a.client_id = c.id
                JOIN services s ON a.service_id = s.id
                WHERE date(a.appointment_date) = ?
                ORDER BY a.appointment_date
            """, (date_str,))
            rows = cursor.fetchall()
            return rows
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return []
        finally:
            conn.close()
    else:
        print("Error: Cannot create database connection.")
        return []

def get_appointments_by_client(client_id):
    """Get all appointments for a specific client"""
    conn = create_connection()
    if conn is not None:
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT a.id, c.first_name, c.last_name, s.name, a.appointment_date, a.deposit_amount, a.notes, a.status 
                FROM appointments a
                JOIN clients c ON a.client_id = c.id
                JOIN services s ON a.service_id = s.id
                WHERE a.client_id = ?
                ORDER BY a.appointment_date DESC
            """, (client_id,))
            rows = cursor.fetchall()
            return rows
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return []
        finally:
            conn.close()
    else:
        print("Error: Cannot create database connection.")
        return []

# Initialize database and tables
def get_pending_appointments_with_clients():
    """Get all scheduled appointments with client information"""
    conn = create_connection()
    if conn is not None:
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT a.id, c.id, c.first_name, c.last_name, s.id, s.name, s.price, a.appointment_date, a.deposit_amount, a.notes, a.status 
                FROM appointments a
                JOIN clients c ON a.client_id = c.id
                JOIN services s ON a.service_id = s.id
                WHERE a.status = 'scheduled'
                ORDER BY a.appointment_date ASC
            """)
            rows = cursor.fetchall()
            return rows
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return []
        finally:
            conn.close()
    else:
        print("Error: Cannot create database connection.")
        return []

def mark_appointment_as_completed(appointment_id):
    """Mark an appointment as completed"""
    conn = create_connection()
    if conn is not None:
        try:
            cursor = conn.cursor()
            cursor.execute("UPDATE appointments SET status = 'completed' WHERE id = ?", (appointment_id,))
            conn.commit()
            return cursor.rowcount
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return 0
        finally:
            conn.close()
    else:
        print("Error: Cannot create database connection.")
        return 0

def save_invoice(appointment_id, total_amount, paid_amount, change_amount, late_fee=0, discount=0):
    """Save invoice information"""
    conn = create_connection()
    if conn is not None:
        try:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO invoices (appointment_id, total_amount, paid_amount, change_amount, late_fee, discount, invoice_date)
                VALUES (?, ?, ?, ?, ?, ?, datetime('now', 'localtime'))
            """, (appointment_id, total_amount, paid_amount, change_amount, late_fee, discount))
            conn.commit()
            return cursor.lastrowid
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return 0
        finally:
            conn.close()
    else:
        print("Error: Cannot create database connection.")
        return 0

def init_db():
    create_tables()
