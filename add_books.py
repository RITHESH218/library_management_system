# add_product.py
import os
from supabase import create_client, Client #pip install supabase
from dotenv import load_dotenv # pip install python-dotenv
 
load_dotenv()
 
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")
sb: Client = create_client(url, key)
 
def add_book(id,name,author,category,s):
    payload = {"book_id": id, "title": name, "author": author, "category": category, "stock": s}
    resp = sb.table("books").insert(payload).execute()
    return resp.data

if __name__ == "__main__":
    id = int(input("Enter book id: ").strip())
    name = input("Enter book title: ").strip()
    author = input("Enter author name: ").strip()
    category = input("Enter book category: ").strip()
    s = int(input("Enter stock count: ").strip())
 
    created = add_book(id,name,author,category,s)
    print("Inserted:", created)
 
 