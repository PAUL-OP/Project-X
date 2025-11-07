import uuid

# --- Movie & Showtimes Data (Nov 2025 India releases) ---
MOVIE_SCHEDULE = {
    '1': {
        'title': '120 Bahadur',
        'showtimes': {
            'A': {'time': '10:00 AM', 'price': 220, 'seats': 40},
            'B': {'time': '01:30 PM', 'price': 230, 'seats': 35},
            'C': {'time': '06:00 PM', 'price': 250, 'seats': 30},
            'D': {'time': '09:30 PM', 'price': 260, 'seats': 20},
        }
    },
    '2': {
        'title': 'Haq',
        'showtimes': {
            'A': {'time': '11:00 AM', 'price': 200, 'seats': 30},
            'B': {'time': '02:30 PM', 'price': 210, 'seats': 25},
            'C': {'time': '07:00 PM', 'price': 220, 'seats': 20},
            'D': {'time': '10:15 PM', 'price': 230, 'seats': 15},
        }
    },
    '3': {
        'title': 'Tere Ishk Mein',
        'showtimes': {
            'A': {'time': '12:00 PM', 'price': 180, 'seats': 50},
            'B': {'time': '03:30 PM', 'price': 190, 'seats': 40},
            'C': {'time': '07:45 PM', 'price': 200, 'seats': 25},
            'D': {'time': '11:00 PM', 'price': 210, 'seats': 15},
        }
    }
}

SNACKS_MENU = {
    '1': {'snack': 'Popcorn (Large)', 'price': 120},
    '2': {'snack': 'Nachos & Cheese', 'price': 150},
    '3': {'snack': 'Coke (Small)', 'price': 60},
    '4': {'snack': 'Cold Coffee', 'price': 100},
    '5': {'snack': 'French Fries', 'price': 90},
}

booked_tickets = {}

# --- Helper Functions ---
def generate_id():
    return str(uuid.uuid4().hex[:6]).upper()

def show_menu(title, menu):
    print(f"\n--- {title} ---")
    for k, v in menu.items():
        if 'title' in v:  # Movies
            print(f"[{k}] {v['title']}")
        elif 'snack' in v:  # Snacks
            print(f"[{k}] {v['snack']} (Rs.{v['price']})")
    print("-" * 40)

def get_choice(prompt, valid):
    choice = input(prompt).strip().upper()
    return choice if choice in valid else None

# --- Core Functions ---
def book_ticket():
    show_menu("Movies", MOVIE_SCHEDULE)
    movie_id = get_choice("Choose movie number: ", MOVIE_SCHEDULE.keys())
    if not movie_id: return print("Invalid choice.")

    movie = MOVIE_SCHEDULE[movie_id]

    print(f"\n--- Showtimes for {movie['title']} ---")
    for k, v in movie['showtimes'].items():
        print(f"[{k}] {v['time']} (Rs.{v['price']}) - Seats: {v['seats']}")
    show_id = get_choice("Choose showtime: ", movie['showtimes'].keys())
    if not show_id: return print("Invalid choice.")

    show = movie['showtimes'][show_id]
    if show['seats'] <= 0: return print("No seats available.")

    try:
        n = int(input(f"Tickets (1-{show['seats']}): "))
        if not (1 <= n <= show['seats']): return print("Invalid ticket count.")
    except: return print("Enter a number.")

    show['seats'] -= n
    total = n * show['price']
    snacks = []

    if input("Add snacks? (Y/N): ").strip().upper() == 'Y':
        show_menu("Snacks", SNACKS_MENU)
        while True:
            s = get_choice("Snack number or D to finish: ", list(SNACKS_MENU.keys())+['D'])
            if s == 'D': break
            snacks.append(SNACKS_MENU[s]['snack'])
            total += SNACKS_MENU[s]['price']

    bid = generate_id()
    booked_tickets[bid] = {
        'movie': movie['title'],
        'time': show['time'],
        'tickets': n,
        'snacks': snacks,
        'cost': total,
        'movie_id': movie_id,
        'show_id': show_id
    }

    print("\n--- BOOKING CONFIRMED ---")
    print(f"ID: {bid} | Movie: {movie['title']} | Time: {show['time']}")
    print(f"Tickets: {n} | Snacks: {', '.join(snacks) if snacks else 'None'}")
    print(f"Total: Rs.{total}")

def cancel_ticket():
    if not booked_tickets: return print("No bookings yet.")
    bid = input("Enter Booking ID: ").strip().upper()
    if bid not in booked_tickets: return print("ID not found.")
    b = booked_tickets.pop(bid)
    MOVIE_SCHEDULE[b['movie_id']]['showtimes'][b['show_id']]['seats'] += b['tickets']
    print(f"Booking {bid} cancelled. Seats restored.")

def modify_ticket():
    if not booked_tickets: return print("No bookings yet.")
    bid = input("Enter Booking ID to modify: ").strip().upper()
    if bid not in booked_tickets: return print("ID not found.")
    booking = booked_tickets[bid]

    print(f"\n--- Current Booking {bid} ---")
    print(f"Movie: {booking['movie']} | Time: {booking['time']}")
    print(f"Tickets: {booking['tickets']} | Cost: Rs.{booking['cost']}")
    print(f"Snacks: {', '.join(booking['snacks']) if booking['snacks'] else 'None'}")

    choice = get_choice("Modify [T]ickets or [S]nacks? ", ['T','S'])
    if choice == 'T':
        show = MOVIE_SCHEDULE[booking['movie_id']]['showtimes'][booking['show_id']]
        show['seats'] += booking['tickets']  # restore old seats
        try:
            n = int(input(f"New tickets (1-{show['seats']}): "))
            if not (1 <= n <= show['seats']): return print("Invalid ticket count.")
        except: return print("Enter a number.")
        show['seats'] -= n
        booking['tickets'] = n
        booking['cost'] = n * show['price'] + sum(SNACKS_MENU[s]['price'] for s in SNACKS_MENU if SNACKS_MENU[s]['snack'] in booking['snacks'])
        print(f"Tickets updated. New cost: Rs.{booking['cost']}")
    elif choice == 'S':
        show_menu("Snacks", SNACKS_MENU)
        while True:
            s = get_choice("Snack number or D to finish: ", list(SNACKS_MENU.keys())+['D'])
            if s == 'D': break
            booking['snacks'].append(SNACKS_MENU[s]['snack'])
            booking['cost'] += SNACKS_MENU[s]['price']
            print(f"Added {SNACKS_MENU[s]['snack']}. New cost: Rs.{booking['cost']}")

# --- Main ---
def main():
    while True:
        print("\n--- Movie Ticket System ---")
        print("[1] Book Ticket\n[2] Cancel Ticket\n[3] Modify Ticket\n[4] Exit")
        c = get_choice("Enter choice: ", ['1','2','3','4'])
        if c == '1': book_ticket()
        elif c == '2': cancel_ticket()
        elif c == '3': modify_ticket()
        elif c == '4': break
        else: print("Invalid option.")

if __name__ == "__main__":
    main()
    