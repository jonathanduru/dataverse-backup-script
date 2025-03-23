import requests
import pyodbc
from msal import PublicClientApplication
from dotenv import load_dotenv
import os

load_dotenv()

# -------------------------------
# Azure App Registration Details
# -------------------------------
CLIENT_ID = os.getenv("CLIENT_ID")
TENANT_ID = os.getenv("TENANT_ID")
AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
SCOPE = [os.getenv("SCOPE")]

# -------------------------------
# Acquire Access Token
# -------------------------------
def acquire_token():
    app = PublicClientApplication(CLIENT_ID, authority=AUTHORITY)
    accounts = app.get_accounts()
    
    result = app.acquire_token_silent(SCOPE, account=accounts[0]) if accounts else None
    if not result:
        result = app.acquire_token_interactive(scopes=SCOPE)
    
    return result["access_token"]

# -------------------------------
# Fetch Tickets from Dataverse
# -------------------------------
def fetch_tickets(token):
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    url = os.getenv("CRM_URL")

    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.json().get("value", [])
    else:
        print("Error:", response.status_code)
        print(response.text)
        return []

# -------------------------------
# Azure SQL Database Connection
# -------------------------------
DB_SERVER = os.getenv("DB_SERVER")
DB_NAME = os.getenv("DB_NAME")
DB_USERNAME = os.getenv("DB_USERNAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")
TICKET_TABLE = os.getenv("TICKET_TABLE")

# Secure connection string for Azure SQL
CONN_STRING = f'''
DRIVER={{ODBC Driver 18 for SQL Server}};
SERVER={DB_SERVER},1433;
DATABASE={DB_NAME};
UID={DB_USERNAME};
PWD={DB_PASSWORD};
Encrypt=yes;
TrustServerCertificate=yes;
'''

# -------------------------------
# Insert Tickets into SQL
# -------------------------------
def insert_tickets_to_sql(tickets):
    try:
        conn = pyodbc.connect(CONN_STRING)
        cursor = conn.cursor()

        for ticket in tickets:
            ticketid = ticket.get("cr42f_ticketid_pk")
            asset = ticket.get("cr42f_affectedasset")
            lastupdated = ticket.get("cr42f_lastupdated")
            status = ticket.get("cr42f_status")
            notes = ticket.get("cr42f_resolutionnotesnew")
            guid = ticket.get("cr42f_ticketid")

            # Delete existing (upsert pattern)
            cursor.execute(f"DELETE FROM {TICKET_TABLE} WHERE cr42f_ticketid_pk = ?", ticketid)

            # Insert new record
            cursor.execute(f"""
                INSERT INTO {TICKET_TABLE} (
                    cr42f_ticketid_pk, cr42f_affectedasset,
                    cr42f_lastupdated, cr42f_status,
                    cr42f_resolutionnotesnew, cr42f_ticketid
                ) VALUES (?, ?, ?, ?, ?, ?)
            """, (ticketid, asset, lastupdated, status, notes, guid))

        conn.commit()
        print(f"{len(tickets)} tickets inserted successfully.")

    except Exception as e:
        print("Failed to insert tickets:", e)

    finally:
        if 'cursor' in locals(): cursor.close()
        if 'conn' in locals(): conn.close()

# -------------------------------
# Main Script
# -------------------------------
if __name__ == "__main__":
    token = acquire_token()

    if not token:
        raise Exception("Token acquisition failed.")

    tickets = fetch_tickets(token)
    insert_tickets_to_sql(tickets)






