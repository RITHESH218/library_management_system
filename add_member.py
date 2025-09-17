# add_product.py
import os
from supabase import create_client, Client #pip install supabase
from dotenv import load_dotenv # pip install python-dotenv
 
load_dotenv()
 
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")
sb: Client = create_client(url, key)
 
def add_product(id,name,mail):
    payload = {"member_id": id, "name": name, "email": mail}
    resp = sb.table("members").insert(payload).execute()
    return resp.data

if __name__ == "__main__":
    id = int(input("Enter member id: ").strip())
    name = input("Enter member name: ").strip()
    mail = input("Enter member email: ").strip()
 
    created = add_product(id,name,mail)
    print("Inserted:", created)
 
 