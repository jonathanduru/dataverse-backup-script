# Dataverse to Azure SQL Backup Script

This project contains a Python script that backs up ticket data from **Microsoft Dataverse** to an **Azure SQL Database**.

It uses:
- Azure AD authentication (via MSAL – no client secrets)
- Dataverse Web API to fetch records
- pyodbc to insert into SQL using an upsert pattern

---

## What This Project Demonstrates

- Pulling data from **Microsoft Dataverse**
- Writing to **Azure SQL Database**
- Secure auth using **interactive Azure login**
- Storing credentials safely in a `.env` file (excluded via `.gitignore`)
- Clean, minimal Python script with no local server or heavy setup

---

**![Project Overview Screenshot](https://raw.githubusercontent.com/jonathanduru/dataverse-backup-script/master/images/Screenshot%202025-03-23%20143043.png)**

---

## Prerequisites & Setup

Before running the script, make sure you have the following ready:

---

### 1. Azure SQL Database

- Set up an Azure SQL Database and server in your subscription
- Note the:
  - Server name (e.g., `yourserver.database.windows.net`)
  - Database name
  - Username and password

**![SQL Database Overview Screenshot](https://raw.githubusercontent.com/jonathanduru/dataverse-backup-script/refs/heads/master/images/Screenshot%202025-03-23%20145532.png)**

---

### 2. Dataverse Environment

- Use an existing Dataverse environment with ticket data
- Copy your **CRM URL** (e.g., `https://yourorg.crm.dynamics.com`)

**![Tickets Table Screenshot](https://raw.githubusercontent.com/jonathanduru/dataverse-backup-script/refs/heads/master/images/PowerApps_Tickets.png)**

---

### 3. Azure AD App Registration

- Go to Azure Portal → **App registrations** → **New registration**
- Select “Accounts in this org only”
- After registering:
  - Note the **Client ID**
  - Note the **Tenant ID**
    
**![App Registrations 1](https://raw.githubusercontent.com/jonathanduru/dataverse-backup-script/refs/heads/master/images/AppRegistrations1.png)**

- Go to the **API permissions** tab
  - Click **Add a permission**
  - Choose **Dynamics 365** → then select **Delegated permissions**
  - Check **user_impersonation**
  - Click **Add permissions**
- Click **Grant admin consent**

**![App Registrations 2](https://raw.githubusercontent.com/jonathanduru/dataverse-backup-script/refs/heads/master/images/AppRegistrations2.png)**

---

### 4. Local Setup

- Make sure Python **3.8+** is installed
- Install dependencies:

```bash
pip install msal requests pyodbc python-dotenv
```

**![pip Install Success](https://raw.githubusercontent.com/jonathanduru/dataverse-backup-script/refs/heads/master/images/PipInstallSuccess.png)**


---

### 5. Running the Script

> **Note:** Make sure you’ve created a `.env` file in the project folder with your connection details and Azure credentials.  
> Example:
> ```env
> DB_SERVER=yourserver.database.windows.net
> DB_NAME=your_db_name
> DB_USERNAME=your_sql_username
> DB_PASSWORD=your_sql_password
> CLIENT_ID=your_azure_app_client_id
> TENANT_ID=your_azure_tenant_id
> CRM_URL=https://yourorg.crm.dynamics.com/api/data/v9.2/tickets
> TICKET_TABLE=dbo.Tickets
> ```
>- **Never commit your `.env` file**  
  Confirm `.gitignore` is working to keep sensitive data out of version control

Once setup is complete, run the script from your terminal:

```bash
python backup_dataverse_tickets.py
```

What the script does:

- Prompts Azure AD login (interactive browser opens on first run)
- Fetches ticket records from your Dataverse table via Web API
- Inserts records into your Azure SQL table using an upsert pattern (delete + insert)


**![Python Script Run](https://raw.githubusercontent.com/jonathanduru/dataverse-backup-script/refs/heads/master/images/ScriptRun.png)**

---

### 6. Final Notes

You're now backing up ticket data from **Microsoft Dataverse** into **Azure SQL** using a clean and secure Python script.  
It authenticates via Azure AD, queries data through the Web API, and writes it to SQL using an upsert pattern.

**![Updated Table in SSMS](https://raw.githubusercontent.com/jonathanduru/dataverse-backup-script/refs/heads/master/images/TableINssms.png)**

---

### 7. Troubleshooting & Common Issues

If something goes wrong, here are common issues and how to fix them:



#### Authentication Issues

- **Symptom**: Browser opens but login fails, or script crashes at token request.
- **Fix**:
  - Double-check that your app registration has **Dynamics CRM delegated permissions**.
  - Make sure you **granted admin consent** in Azure.
  - Confirm the `CLIENT_ID` and `TENANT_ID` in your `.env` file match your Azure App.

**![App Registrations 2](https://raw.githubusercontent.com/jonathanduru/dataverse-backup-script/refs/heads/master/images/AppRegistrations2.png)**



#### Dataverse Fetch Issues

- **Symptom**: Script runs, but no tickets are returned.
- **Fix**:
  - Ensure the table name and fields in your API URL are correct.
  - Confirm the record type exists and has data in your Dataverse environment.

**![Tickets Table Screenshot](https://raw.githubusercontent.com/jonathanduru/dataverse-backup-script/refs/heads/master/images/TicketsTable.png)**



#### SQL Insert/Connection Issues

- **Symptom**: Database errors or records not inserted.
- **Fix**:
  - Ensure your SQL firewall allows your machine's IP.
  - Make sure **ODBC Driver 18 for SQL Server** is installed.
  - Verify the `DB_SERVER`, `DB_NAME`, `DB_USERNAME`, and `DB_PASSWORD` values in `.env`.

**![Server Firewall](https://raw.githubusercontent.com/jonathanduru/dataverse-backup-script/refs/heads/master/images/Server_Firewall.png)**

---

### Security Best Practices

- **Rotate credentials** regularly:
  - Refresh SQL usernames/passwords
  - Re-register your Azure AD app if needed

- **Never commit your `.env` file**  
  Confirm `.gitignore` is working to keep secrets out of version control

- **Use separate environments** for dev/test/prod when possible


---

Thanks for following along!

