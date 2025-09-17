'''5. Borrow Book (Transaction)
When a member borrows a book:
Check if the book has stock available.
If available → decrease stock by 1, insert record into borrow_records.
If not available → show error (“Book not available”).

 👉 This must be a transaction (commit both steps, or rollback if one fails).'''
import os
from supabase import create_client, Client
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")
sb: Client = create_client(url, key)

def borrow_book(member_id, book_id):
    # Step 1: Check stock
    book_resp = sb.table("books").select("stock").eq("book_id", book_id).execute()
    if not book_resp.data:
        print("Book not found.")
        return
    stock = book_resp.data[0]["stock"]
    if stock < 1:
        print("Book not available.")
        return

    # Step 2: Transactional borrow
    try:
        # Decrease stock
        update_resp = sb.table("books").update({"stock": stock - 1}).eq("book_id", book_id).execute()
        if not update_resp.data:
            print("Failed to update stock.")
            return

        # Insert borrow record
        borrow_data = {
            "member_id": member_id,
            "book_id": book_id,
            "borrow_date": datetime.now().isoformat(),  # keep timestamp
            "return_date": None
        }
        insert_resp = sb.table("borrow_records").insert(borrow_data).execute()
        if not insert_resp.data:
            # Rollback stock update
            sb.table("books").update({"stock": stock}).eq("book_id", book_id).execute()
            print("Failed to create borrow record. Rolled back stock.")
            return

        print("Book borrowed successfully.")
    except Exception as e:
        # Rollback stock update if any error
        sb.table("books").update({"stock": stock}).eq("book_id", book_id).execute()
        print("Transaction failed:", str(e))

if __name__ == "__main__":
    member_id = int(input("Enter member ID: ").strip())   # cast to int
    book_id = int(input("Enter book ID: ").strip())       # cast to int
    borrow_book(member_id, book_id)
