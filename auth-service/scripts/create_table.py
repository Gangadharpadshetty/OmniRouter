import os
import sys
from pathlib import Path

from dotenv import load_dotenv

try:
    import psycopg2
except ImportError:
    print("psycopg2 is not installed. Install dependencies from requirements.txt")
    sys.exit(1)

BASE_DIR = Path(__file__).resolve().parent.parent
SQL_FILE = BASE_DIR / "sql" / "create_users_table.sql"

# Load .env from common locations (project root or app/core)
env_candidates = [BASE_DIR / ".env", BASE_DIR / "app" / "core" / ".env"]
for p in env_candidates:
    if p.exists():
        load_dotenv(dotenv_path=str(p))
        break
else:
    load_dotenv()

DATABASE_URL = os.environ.get("DATABASE_URL")
if not DATABASE_URL:
    print("DATABASE_URL is not set in the environment. Please set it (or create a .env file).")
    sys.exit(1)

if not SQL_FILE.exists():
    print(f"SQL file not found: {SQL_FILE}")
    sys.exit(1)

with open(SQL_FILE, "r", encoding="utf-8") as f:
    sql_text = f.read()

print("Connecting to database and executing SQL...")
conn = None
try:
    conn = psycopg2.connect(DATABASE_URL)
    conn.autocommit = True
    with conn.cursor() as cur:
        cur.execute(sql_text)
    print("SQL executed successfully.")
except Exception as e:
    print("Error executing SQL:", e)
    sys.exit(1)
finally:
    if conn:
        conn.close()
import os
import sys
from pathlib import Path

try:
    import psycopg2
except ImportError:
    print("psycopg2 is not installed. Install dependencies from requirements.txt")
    sys.exit(1)

from psycopg2 import sql

BASE_DIR = Path(__file__).resolve().parent.parent
SQL_FILE = BASE_DIR / "sql" / "create_users_table.sql"

DATABASE_URL = os.environ.get("DATABASE_URL")
if not DATABASE_URL:
    print("DATABASE_URL is not set in the environment. Please set it (or create a .env file).")
    sys.exit(1)

with open(SQL_FILE, "r", encoding="utf-8") as f:
    sql_text = f.read()

print("Connecting to database and executing SQL...")
conn = psycopg2.connect(DATABASE_URL)
import os
import sys
from pathlib import Path

from dotenv import load_dotenv

try:
    import psycopg2
except ImportError:
    print("psycopg2 is not installed. Install dependencies from requirements.txt")
    sys.exit(1)

BASE_DIR = Path(__file__).resolve().parent.parent
SQL_FILE = BASE_DIR / "sql" / "create_users_table.sql"

# Load .env from common locations (project root or app/core)
env_candidates = [BASE_DIR / ".env", BASE_DIR / "app" / "core" / ".env"]
for p in env_candidates:
    if p.exists():
        load_dotenv(dotenv_path=str(p))
        break
else:
    load_dotenv()

DATABASE_URL = os.environ.get("DATABASE_URL")
if not DATABASE_URL:
    print("DATABASE_URL is not set in the environment. Please set it (or create a .env file).")
    sys.exit(1)

if not SQL_FILE.exists():
    print(f"SQL file not found: {SQL_FILE}")
    sys.exit(1)

with open(SQL_FILE, "r", encoding="utf-8") as f:
    sql_text = f.read()

print("Connecting to database and executing SQL...")
conn = None
try:
    conn = psycopg2.connect(DATABASE_URL)
    conn.autocommit = True
    with conn.cursor() as cur:
        cur.execute(sql_text)
    print("SQL executed successfully.")
except Exception as e:
    print("Error executing SQL:", e)
    sys.exit(1)
finally:
    if conn:
        conn.close()
