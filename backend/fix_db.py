import sys
sys.path.append('c:\\Users\\Dell\\.gemini\\antigravity\\scratch\\schemo\\backend')
from database import get_connection

conn = get_connection()
cursor = conn.cursor()

try:
    cursor.execute("ALTER TABLE users ADD COLUMN occupation ENUM('Student','Working Professional','Government Employee','Self Employed','Unemployed','Senior Citizen','Other') NOT NULL DEFAULT 'Other';")
    print("Added occupation column")
except Exception as e:
    print(e)
    
try:
    cursor.execute("ALTER TABLE users DROP COLUMN income;")
    print("Dropped income column")
except Exception as e:
    print(e)

conn.commit()
cursor.close()
conn.close()
