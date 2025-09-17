'''2. Read (Select)
List all books with availability.
Search books by title/author/category.
Show member details and their borrowed books.'''

import os
from supabase import create_client, Client #pip install supabase
from dotenv import load_dotenv # pip install python-dotenv

load_dotenv()

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")
sb: Client = create_client(url, key)

def list_books_with_availability():
    response = sb.table("books").select("book_id, title, author, category, stock").execute()
    books = response.data
    print("\nAll Books with Availability:")
    for book in books:
        print(f"ID: {book['book_id']}, Title: {book['title']}, Author: {book['author']}, Category: {book['category']}, Stock: {book['stock']}")

def search_books(query, field):
    response = sb.table("books").select("book_id, title, author, category, stock").ilike(field, f"%{query}%").execute()
    books = response.data
    print(f"\nBooks matching {field} '{query}':")
    if books:
        for book in books:
            print(f"ID: {book['book_id']}, Title: {book['title']}, Author: {book['author']}, Category: {book['category']}, Stock: {book['stock']}")
    else:
        print("No books found.")

def show_member_details(member_id):
    member_resp = sb.table("members").select("member_id, name, email").eq("member_id", member_id).execute()
    member = member_resp.data
    if not member:
        print("Member not found.")
        return
    member = member[0]
    print(f"\nMember ID: {member['member_id']}, Name: {member['name']}, Email: {member['email']}")
    borrowed_resp = sb.table("borrowed_books").select("book_id, borrow_date, return_date").eq("member_id", member_id).execute()
    borrowed = borrowed_resp.data
    if borrowed:
        print("Borrowed Books:")
        for b in borrowed:
            book_resp = sb.table("books").select("title").eq("book_id", b["book_id"]).execute()
            title = book_resp.data[0]["title"] if book_resp.data else "Unknown"
            print(f"Title: {title}, Borrow Date: {b['borrow_date']}, Return Date: {b['return_date']}")
    else:
        print("No borrowed books.")

if __name__ == "__main__":
    print("1. List all books with availability")
    print("2. Search books by title")
    print("3. Show member details and borrowed books")
    choice = input("Choose option: ").strip()
    if choice == "1":
        list_books_with_availability()
    elif choice == "2":
        query = input("Enter title to search: ").strip()
        search_books(query, "title")
    elif choice == "3":
        member_id = input("Enter member ID: ").strip()