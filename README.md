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

📸 **[Insert screenshot of your GitHub repo with README + description]**

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

📸 **[Insert screenshot of your Azure SQL database + connection settings]**

---

### 2. Dataverse Environment

- Use an existing Dataverse environment with ticket data
- Copy your **CRM URL** (e.g., `https://yourorg.crm.dynamics.com`)

📸 **[Insert screenshot of your Dataverse table or the Tickets entity in CRM]**

---

### 3. Azure AD App Registration

- Go to Azure Portal → **App registrations** → **New registration**
- Select “Accounts in this org only”
- After registering:
  - Copy the **Client ID**
  - Copy the **Tenant ID**
- Add **Dynamics CRM delegated permissions**
- Click **Grant admin consent**

📸 **[Insert screenshot of the App Registration and permissions added]**

---

### 4. Local Setup

- Make sure Python **3.8+** is installed
- Install dependencies:

```bash
pip install msal requests pyodbc python-dotenv
```

📸 **[Insert screenshot of your VS Code terminal with pip install success]**


---

### 5. Running the Script

Once setup is complete, run the script from your terminal:

```bash
python backup_dataverse_tickets.py
```

What the script does:

- Prompts Azure AD login (interactive browser opens on first run)
- Fetches ticket records from your Dataverse table via Web API
- Inserts records into your Azure SQL table using an upsert pattern (delete + insert)

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

📸 **[Insert screenshot of your terminal showing “X tickets inserted successfully.”]**

---

### 6. Troubleshooting & Common Issues

If something goes wrong, here are common issues and how to fix them:

---

#### Authentication Issues

- **Symptom**: Browser opens but login fails, or script crashes at token request.
- **Fix**:
  - Double-check that your app registration has **Dynamics CRM delegated permissions**.
  - Make sure you **granted admin consent** in Azure.
  - Confirm the `CLIENT_ID` and `TENANT_ID` in your `.env` file match your Azure App.

📸 **[Insert screenshot of your Azure App registration permissions panel]**

---

#### Dataverse Fetch Issues

- **Symptom**: Script runs, but no tickets are returned.
- **Fix**:
  - Ensure the table name and fields in your API URL are correct.
  - Confirm the record type exists and has data in your Dataverse environment.

📸 **[Insert screenshot of your Dataverse table with sample ticket rows visible]**

---

#### SQL Insert/Connection Issues

- **Symptom**: Database errors or records not inserted.
- **Fix**:
  - Ensure your SQL firewall allows your machine's IP.
  - Make sure **ODBC Driver 18 for SQL Server** is installed.
  - Verify the `DB_SERVER`, `DB_NAME`, `DB_USERNAME`, and `DB_PASSWORD` values in `.env`.

📸 **[Insert screenshot of SQL Server firewall settings or local error message]**

---

### 7. Final Notes

You're now backing up ticket data from **Microsoft Dataverse** into **Azure SQL** using a clean and secure Python script.  
It authenticates via Azure AD, queries data through the Web API, and writes it to SQL using an upsert pattern.

📸 **[Insert final screenshot of your SQL table showing inserted ticket records]**

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

