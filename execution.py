# --- 4. Main Execution ---
def main():
    while True:
        print("\n--- Movie Ticket Booking System ---")
        print("  [1] Book New Ticket")
        print("  [2] Modify Existing Ticket")
        print("  [3] Cancel Ticket")
        print("  [4] Exit")
        print("-----------------------------------")

        choice = get_user_choice("Enter your choice: ", ['1', '2', '3', '4'])

        if choice == '1':
            book_new_ticket()
        elif choice == '2':
            modify_ticket()
        elif choice == '3':
            cancel_ticket()
        elif choice == '4':
            print("\n👋 Thank you for using the Movie Ticket Booking System. Goodbye!")
            break

if __name__ == "_main_":
    main()