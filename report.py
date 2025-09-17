'''7.⁠ ⁠Reports (Advanced Selects)
List top 5 most borrowed books.
List members with overdue books (borrowed but not returned in >14 days).
Count total books borrowed per member.'''
import os
from supabase import create_client, Client
from dotenv import load_dotenv
from datetime import datetime, timedelta

load_dotenv()

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")
sb: Client = create_client(url, key)

def top_5_most_borrowed_books():
    resp = sb.table("borrow_records").select("book_id").execute()
    borrow_data = resp.data
    book_counts = {}
    for record in borrow_data:
        book_counts[record["book_id"]] = book_counts.get(record["book_id"], 0) + 1
    top_books = sorted(book_counts.items(), key=lambda x: x[1], reverse=True)[:5]
    print("\nTop 5 Most Borrowed Books:")
    for book_id, count in top_books:
        book_resp = sb.table("books").select("title").eq("book_id", book_id).execute()
        title = book_resp.data[0]["title"] if book_resp.data else "Unknown"
        print(f"Title: {title}, Times Borrowed: {count}")

def members_with_overdue_books():
    overdue_date = (datetime.now() - timedelta(days=14)).isoformat()
    resp = (
        sb.table("borrow_records")
        .select("member_id, book_id, borrow_date, return_date")
        .is_("return_date", None)
        .lt("borrow_date", overdue_date)
        .execute()
    )
    overdue = resp.data
    print("\nMembers with Overdue Books (>14 days):")
    if overdue:
        for record in overdue:
            member_resp = sb.table("members").select("name, email").eq("member_id", record["member_id"]).execute()
            member = member_resp.data[0] if member_resp.data else {"name": "Unknown", "email": "Unknown"}
            book_resp = sb.table("books").select("title").eq("book_id", record["book_id"]).execute()
            title = book_resp.data[0]["title"] if book_resp.data else "Unknown"
            print(f"Member: {member['name']} ({member['email']}), Book: {title}, Borrowed on: {record['borrow_date']}")
    else:
        print("No overdue books found.")

def total_books_borrowed_per_member():
    resp = sb.table("borrow_records").select("member_id").execute()
    borrow_data = resp.data
    member_counts = {}
    for record in borrow_data:
        member_counts[record["member_id"]] = member_counts.get(record["member_id"], 0) + 1
    print("\nTotal Books Borrowed Per Member:")
    for member_id, count in member_counts.items():
        member_resp = sb.table("members").select("name, email").eq("member_id", member_id).execute()
        member = member_resp.data[0] if member_resp.data else {"name": "Unknown", "email": "Unknown"}
        print(f"Member: {member['name']} ({member['email']}), Total Borrowed: {count}")

if __name__ == "__main__":
    print("1. Top 5 most borrowed books")
    print("2. Members with overdue books (>14 days)")
    print("3. Total books borrowed per member")
    choice = input("Choose report: ").strip()
    if choice == "1":
        top_5_most_borrowed_books()
    elif choice == "2":
        members_with_overdue_books()
    elif choice == "3":
        total_books_borrowed_per_member()
    else:
        print("Invalid choice")
