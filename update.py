'''
3. Update
Update book stock (e.g., when more copies are purchased).
Update member info (e.g., change email)'''
import os
from supabase import create_client, Client 
from dotenv import load_dotenv 

load_dotenv()

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")
sb: Client = create_client(url, key)

def update_book_stock(book_id, new_stock):
    resp = sb.table("books").update({"stock": new_stock}).eq("book_id", book_id).execute()
    if resp.data:
        print(f"Updated stock for book ID {book_id} to {new_stock}.")
   
def update_member_email(member_id, new_email):
    resp = sb.table("members").update({"email": new_email}).eq("member_id", member_id).execute()
    if resp.data:
        print(f"Updated email for member ID {member_id} to {new_email}.")
    

if __name__ == "__main__":
    print("1. Update book stock")
    print("2. Update member email")
    choice = input("Choose option: ").strip()
    if choice == "1":
        book_id = input("Enter book ID: ").strip()
        new_stock = int(input("Enter new stock value: ").strip())
        update_book_stock(book_id, new_stock)
    elif choice == "2":
        member_id = input("Enter member ID: ").strip()
        new_email = input("Enter new email: ").strip()
        update_member_email(member_id, new_email)
    else:
        print("Invalid")
