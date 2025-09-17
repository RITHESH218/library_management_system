'''6. Return Book (Transaction)
When a member returns a book:
Update the borrow_records.return_date.
Increase book stock by 1.
Again, both must happen in a single transaction.'''
import os
from supabase import create_client, Client
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")
sb: Client = create_client(url, key)

def return_book(member_id, book_id):
    # Find the active borrow record (not returned yet)
    borrow_resp = (
        sb.table("borrow_records")
        .select("record_id, return_date")
        .eq("member_id", member_id)
        .eq("book_id", book_id)
        .is_("return_date", None)  # "is null"
        .execute()
    )

    if not borrow_resp.data:
        print("No active borrow record found for this member and book.")
        return

    record_id = borrow_resp.data[0]["record_id"]

    # Get current stock
    book_resp = sb.table("books").select("stock").eq("book_id", book_id).execute()
    if not book_resp.data:
        print("Book not found.")
        return
    stock = book_resp.data[0]["stock"]

    try:
        # Step 1: Update borrow record with return date
        update_borrow = (
            sb.table("borrow_records")
            .update({"return_date": datetime.now().isoformat()})
            .eq("record_id", record_id)
            .execute()
        )
        if not update_borrow.data:
            print("Failed to update borrow record.")
            return

        # Step 2: Increase book stock
        update_stock = (
            sb.table("books")
            .update({"stock": stock + 1})
            .eq("book_id", book_id)
            .execute()
        )
        if not update_stock.data:
            sb.table("borrow_records").update({"return_date": None}).eq("record_id", record_id).execute()
            print("Failed to update book stock. Rolled back borrow record.")
            return

        print("Book returned successfully.")
    except Exception as e:
        sb.table("borrow_records").update({"return_date": None}).eq("record_id", record_id).execute()
        print("Transaction failed:", str(e))

if __name__ == "__main__":
    member_id = int(input("Enter member ID: ").strip())
    book_id = int(input("Enter book ID: ").strip())
    return_book(member_id, book_id)
