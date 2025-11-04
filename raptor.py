import uuid

# --- 1. Data Structures ---
MOVIE_SCHEDULE = {
    '1': {'movie': 'Aaryan', 'time': '10:00 AM', 'price': 150, 'seats_available': 50},
    '2': {'movie': 'Bison Kaalamaadan', 'time': '01:30 PM', 'price': 180, 'seats_available': 12},
    '3': {'movie': 'Dude', 'time': '05:00 PM', 'price': 150, 'seats_available': 35},
    '4': {'movie': 'The Girlfriend', 'time': '09:15 PM', 'price': 200, 'seats_available': 5},
}

SNACKS_MENU = {
    '1': {'snack': 'Popcorn (Large)', 'price': 120},
    '2': {'snack': 'Nachos & Cheese', 'price': 150},
    '3': {'snack': 'Coke (Small)', 'price': 60},
}

booked_tickets = {}

# --- 2. Helper Functions ---
def generate_booking_id():
    return str(uuid.uuid4().hex)[:6].upper()

def display_menu(title, menu_dict):
    print(f"\n--- {title} ---")
    for key, item in menu_dict.items():
        if 'movie' in item:
            print(f"  [{key}] {item['movie']} at {item['time']} (Rs.{item['price']}) - Seats: {item['seats_available']}")
        elif 'snack' in item:
            print(f"  [{key}] {item['snack']} (Rs.{item['price']})")
    print("-" * (len(title) + 8))

def get_user_choice(prompt, valid_choices):
    while True:
        choice = input(prompt).strip().upper()
        if choice in valid_choices:
            return choice
        print("❌ Invalid choice. Please try again.")

# --- 3. Core Logic Functions ---
def book_new_ticket():
    display_menu("Available Movies and Showtimes", MOVIE_SCHEDULE)
    movie_choices = MOVIE_SCHEDULE.keys()
    movie_id = get_user_choice("Enter the number of the movie you want to book: ", movie_choices)
    selected_movie = MOVIE_SCHEDULE[movie_id]

    if selected_movie['seats_available'] <= 0:
        print(f"\n😔 Sorry, no seats available for {selected_movie['movie']} at {selected_movie['time']}.")
        return

    try:
        num_tickets = int(input(f"How many tickets do you want to book (1-{selected_movie['seats_available']}): "))
        if not (1 <= num_tickets <= selected_movie['seats_available']):
            print(f"⚠️ Invalid number of tickets. Only {selected_movie['seats_available']} seats remaining.")
            return
    except ValueError:
        print("⚠️ Invalid input. Please enter a number.")
        return

    selected_movie['seats_available'] -= num_tickets
    ticket_cost = num_tickets * selected_movie['price']
    total_cost = ticket_cost
    selected_snacks = []

    snack_choice = get_user_choice("Do you want to add snacks? (Y/N): ", ['Y', 'N'])
    if snack_choice == 'Y':
        display_menu("Snacks Menu", SNACKS_MENU)
        snack_choices = SNACKS_MENU.keys()
        
        while True:
            snack_id = get_user_choice("Enter the number of the snack to add (or 'D' for Done): ", list(snack_choices) + ['D'])
            if snack_id == 'D':
                break
            
            snack_item = SNACKS_MENU[snack_id]
            selected_snacks.append(snack_item['snack'])
            total_cost += snack_item['price']

    booking_id = generate_booking_id()
    
    new_booking = {
        'movie': selected_movie['movie'],
        'time': selected_movie['time'],
        'tickets': num_tickets,
        'cost': total_cost,
        'snacks': selected_snacks if selected_snacks else 'None',
        'movie_id': movie_id
    }
    
    booked_tickets[booking_id] = new_booking

    print("\n\n🎉 --- BOOKING CONFIRMED --- 🎉")
    print(f"*Booking ID:* {booking_id}")
    print(f"Movie: {new_booking['movie']} at {new_booking['time']}")
    print(f"Tickets: {new_booking['tickets']}")
    print(f"Snacks: {', '.join(new_booking['snacks']) if isinstance(new_booking['snacks'], list) else new_booking['snacks']}")
    print(f"Total Amount Paid: Rs.{new_booking['cost']}")
    print("---------------------------------")
    print(f"Please save your Booking ID: *{booking_id}* to modify or cancel your ticket later.")


def modify_ticket():
    if not booked_tickets:
        print("\n😔 No tickets have been booked yet to modify.")
        return

    booking_id = input("\nEnter your 6-character Booking ID for modification: ").strip().upper()
    if booking_id not in booked_tickets:
        print(f"\n❌ Booking ID '{booking_id}' not found.")
        return

    booking = booked_tickets[booking_id]
    print(f"\n-- Current Booking for ID: {booking_id} --")
    print(f"Movie: {booking['movie']} | Time: {booking['time']}")
    print(f"Tickets: {booking['tickets']} | Total Cost: Rs.{booking['cost']}")
    print(f"Snacks: {', '.join(booking['snacks']) if isinstance(booking['snacks'], list) else booking['snacks']}")
    print("-" * 35)
    
    modify_option = get_user_choice("What do you want to modify?\n  [S] Snacks\n  [T] Tickets\nEnter choice: ", ['S', 'T'])
    
    if modify_option == 'S':
        print("\n--- Current Snacks ---")
        if isinstance(booking['snacks'], list):
            for i, snack in enumerate(booking['snacks']):
                print(f"  {i+1}. {snack}")
        else:
            print("  None")
        
        display_menu("Snacks Menu to Add", SNACKS_MENU)
        snack_choices = SNACKS_MENU.keys()
        
        while True:
            snack_id = get_user_choice("Enter the number of the snack to add (or 'D' for Done): ", list(snack_choices) + ['D'])
            if snack_id == 'D':
                break
            
            snack_item = SNACKS_MENU[snack_id]
            
            if booking['snacks'] == 'None':
                booking['snacks'] = [snack_item['snack']]
            else:
                booking['snacks'].append(snack_item['snack'])
                
            booking['cost'] += snack_item['price']
            print(f"✅ Added {snack_item['snack']}. New cost: Rs.{booking['cost']}")
            
        print(f"\n✅ Booking *{booking_id}* successfully updated with new snacks.")

    elif modify_option == 'T':
        print("Ticket modification is complex. Please *cancel and re-book* if you need to change the number of tickets.")
        
def cancel_ticket():
    if not booked_tickets:
        print("\n😔 No tickets have been booked yet to cancel.")
        return

    booking_id = input("\nEnter your 6-character Booking ID to cancel: ").strip().upper()
    if booking_id not in booked_tickets:
        print(f"\n❌ Booking ID '{booking_id}' not found.")
        return

    booking = booked_tickets[booking_id]
    confirm = get_user_choice(f"Are you sure you want to CANCEL the booking for {booking['movie']} (Total Cost: Rs.{booking['cost']})? (Y/N): ", ['Y', 'N'])

    if confirm == 'Y':
        movie_id = booking['movie_id']
        MOVIE_SCHEDULE[movie_id]['seats_available'] += booking['tickets']
        
        del booked_tickets[booking_id]
        
        print("\n✅ --- CANCELLATION SUCCESSFUL --- ✅")
        print(f"Booking ID *{booking_id}* for {booking['movie']} has been cancelled.")
        print(f"A refund of Rs.{booking['cost']} will be processed.")
    else:
        print("\nCancellation aborted.")

# --- 4. Main Program Loop ---
def movie_ticket_system():
    print("🎬 Welcome to the Python Movie Ticket System!")
    
    while True:
        print("\n--- MAIN MENU ---")
        print("[B] Browse & Book New Tickets")
        print("[M] Modify an Old Ticket")
        print("[C] Cancel a Ticket")
        print("[E] Exit")
        print("-----------------")

        choice = get_user_choice("Enter your choice (B/M/C/E): ", ['B', 'M', 'C', 'E'])

        if choice == 'B':
            book_new_ticket()
        elif choice == 'M':
            modify_ticket()
        elif choice == 'C':
            cancel_ticket()
        elif choice == 'E':
            print("\n👋 Thank you for using the Movie Ticket System. Goodbye!")
            break

if _name_ == "_main_":
    movie_ticket_system()