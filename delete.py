'''4. Delete
Delete a member (only if no borrowed books).
Delete a book (only if not borrowed).'''
import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")
sb: Client = create_client(url, key)

def delete_member(member_id):
    borrowed = sb.table("borrow_records").select("record_id").eq("member_id", member_id).execute().data
    if borrowed:
        print("Cannot delete member: member has borrowed books.")
        return
    resp = sb.table("members").delete().eq("member_id", member_id).execute()
    if resp.data:
        print(f"Member ID {member_id} deleted.")
    else:
        print("Member not found or delete failed.")

def delete_book(book_id):
    borrowed = sb.table("borrow_records").select("record_id").eq("book_id", book_id).execute().data
    if borrowed:
        print("Cannot delete book: book is currently borrowed.")
        return
    resp = sb.table("books").delete().eq("book_id", book_id).execute()
    if resp.data:
        print(f"Book ID {book_id} deleted.")
    else:
        print("Book not found or delete failed.")

if __name__ == "__main__":
    print("1. Delete member")
    print("2. Delete book")
    choice = input("Choose option: ").strip()
    if choice == "1":
        member_id = input("Enter member ID: ").strip()
        delete_member(member_id)
    elif choice == "2":
        book_id = input("Enter book ID: ").strip()
        delete_book(book_id)
    else:
        print("Invalid")