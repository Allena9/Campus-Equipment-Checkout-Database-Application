import sqlite3
from db import connect, init_db, seed_data
import ops

def menu():
    print("""
===== Equipment Checkout (SQLite) =====
1) Initialize DB
2) Seed sample data
3) List items
4) List available items
5) Search items
6) List active loans
7) Add user
8) Add item
9) Checkout item
10) Return loan
11) Update item name
12) Delete loan
13) Delete item
14) Delete user
0) Exit
""")

def main():
    conn = connect()
    init_db(conn)  # auto-create on start

    while True:
        menu()
        choice = input("Choose: ").strip()

        try:
            if choice == "1":
                init_db(conn)
                print("DB initialized (tables created).")

            elif choice == "2":
                seed_data(conn)
                print("Seeded.")

            elif choice == "3":
                ops.list_items(conn)

            elif choice == "4":
                ops.list_items(conn, only_available=True)

            elif choice == "5":
                term = input("Search term: ").strip()
                ops.search_items(conn, term)

            elif choice == "6":
                ops.list_active_loans(conn)

            elif choice == "7":
                name = input("Name: ").strip()
                email = input("Email: ").strip()
                ops.add_user(conn, name, email)

            elif choice == "8":
                name = input("Item name: ").strip()
                category = input("Category: ").strip()
                ops.add_item(conn, name, category)

            elif choice == "9":
                ops.list_users(conn)
                ops.list_items(conn, only_available=True)
                user_id = int(input("User ID: ").strip())
                item_id = int(input("Item ID: ").strip())
                days = input("Days until due (default 7): ").strip()
                days = int(days) if days else 7
                ops.checkout_item(conn, user_id, item_id, days)

            elif choice == "10":
                ops.list_active_loans(conn)
                loan_id = int(input("Loan ID to return: ").strip())
                ops.return_loan(conn, loan_id)

            elif choice == "11":
                ops.list_items(conn)
                item_id = int(input("Item ID to rename: ").strip())
                new_name = input("New name: ").strip()
                ops.update_item_name(conn, item_id, new_name)

            elif choice == "12":
                loan_id = int(input("Loan ID to delete: ").strip())
                ops.delete_loan(conn, loan_id)

            elif choice == "13":
                ops.list_items(conn)
                item_id = int(input("Item ID to delete: ").strip())
                ops.delete_item(conn, item_id)

            elif choice == "14":
                ops.list_users(conn)
                user_id = int(input("User ID to delete: ").strip())
                ops.delete_user(conn, user_id)

            elif choice == "0":
                print("Bye!")
                break

            else:
                print("Invalid option.")

        except ValueError:
            print("Invalid input (expected a number).")
        except sqlite3.IntegrityError as e:
            print(f"Database constraint error: {e}")

    conn.close()

if __name__ == "__main__":
    main()
