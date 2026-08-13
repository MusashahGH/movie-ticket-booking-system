import os
import sys
import sqlite3 ## SQL Connection
from google import genai ## chatbot
from datetime import datetime

movies = {
    "1": {"title": "The Super Mario Galaxy Movie", "language": "English", "price": 800},
    "2": {"title": "Spider-Man: Brand New Day", "language": "English", "price": 800},
    "3": {"title": "Michael", "language": "English", "price": 700},
    "4": {"title": "The Devil Wears Prada 2", "language": "English", "price": 700},
    "5": {"title": "The Odyssey", "language": "English", "price": 800},
    "6": {"title": "Jawani Phir Nahi Ani 3", "language": "Urdu", "price": 600},
    "7": {"title": "Quaid-e-Azam Zindabad", "language": "Urdu", "price": 600},
    "8": {"title": "Teefa in Trouble", "language": "Urdu", "price": 550},
    "9": {"title": "Bhooth Bangla", "language": "Urdu", "price": 550},
    "10": {"title": "Parey Hut Love", "language": "Urdu", "price": 500},
}

shows = {
    "1": ["10:00 AM", "02:00 PM", "06:00 PM", "10:00 PM"],
    "2": ["11:00 AM", "03:00 PM", "07:00 PM"],
    "3": ["12:00 PM", "04:00 PM", "08:00 PM"],
    "4": ["01:00 PM", "05:00 PM", "09:00 PM"],
    "5": ["10:30 AM", "02:30 PM", "06:30 PM", "10:30 PM"],
    "6": ["11:30 AM", "03:30 PM", "07:30 PM"],
    "7": ["12:30 PM", "04:30 PM", "08:30 PM"],
    "8": ["01:30 PM", "05:30 PM", "09:30 PM"],
    "9": ["10:00 AM", "02:00 PM", "06:00 PM"],
    "10": ["11:00 AM", "03:00 PM", "07:00 PM"],
}

ROWS = 8
COLS = 10

seat_maps = {}
for m_id in movies:
    seat_maps[m_id] = {}
    for show_time in shows[m_id]:
        seat_maps[m_id][show_time] = [["O" for _ in range(COLS)] for _ in range(ROWS)]

bookings = {}
booking_counter = 1000
def init_db(): ## SQL Create
    global conn, cursor, booking_counter
    conn = sqlite3.connect("movie_tickets.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS bookings (
            booking_id TEXT PRIMARY KEY,
            name TEXT,
            movie TEXT,
            show_time TEXT,
            seats TEXT,
            total INTEGER,
            timestamp TEXT
        )
    """)
    conn.commit()
    
    # Load the highest booking ID from database to avoid duplicates
    cursor.execute("SELECT MAX(booking_id) FROM bookings")
    result = cursor.fetchone()[0]
    if result:
        booking_counter = int(result[2:]) if result.startswith("BK") else 1000
    else:
        booking_counter = 1000


def init_chatbot(): ## chatbot call
    global client
    client = genai.Client()

def get_live_context():
    cursor.execute("SELECT COUNT(*) FROM bookings")
    total_bookings = cursor.fetchone()[0]

    movie_list_text = "\n".join(
        f"{m_id}: {info['title']} ({info['language']}) - Rs.{info['price']} - Shows: {', '.join(shows[m_id])}"
        for m_id, info in movies.items()
    )

    return f"""You are a helpful assistant for a movie ticket booking system.

Current movies available:
{movie_list_text}

Total bookings made so far: {total_bookings}

Answer questions about movies, prices, showtimes, and how to book tickets. Keep answers short and friendly. For live seat availability, tell them to use menu option 3."""

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def pause():
    input("\nPress Enter to continue...")


def print_header(title):
    clear_screen()
    print("=" * 55)
    print(f"{title.center(55)}")
    print("=" * 55)


def seat_label(row, col):
    return f"{chr(65 + row)}{col + 1}"


def print_seat_map(grid):
    print("\n        SCREEN THIS SIDE")
    print("   " + "-" * (COLS * 4))
    col_header = "    " + "".join(f"{c + 1:>4}" for c in range(COLS))
    print(col_header)
    for r in range(ROWS):
        row_str = f"{chr(65 + r):>2} |"
        for c in range(COLS):
            row_str += f"{grid[r][c]:>4}"
        print(row_str)
    print("\nLegend: O = Available   X = Booked\n")


def show_movies():
    print_header("NOW SHOWING")
    print(f"{'ID':<5}{'Title':<34}{'Language':<12}{'Price':<8}")
    print("-" * 61)
    for m_id, info in movies.items():
        print(f"{m_id:<5}{info['title']:<34}{info['language']:<12}Rs.{info['price']:<5}")


def select_movie():
    show_movies()
    m_id = input("\nEnter Movie ID (or 0 to go back): ").strip().upper()
    if m_id == "0":
        return None
    if m_id not in movies:
        print("Invalid movie ID.")
        pause()
        return None
    return m_id


def select_show(m_id):
    print_header(f"SHOW TIMES - {movies[m_id]['title']}")
    for idx, t in enumerate(shows[m_id], start=1):
        print(f"{idx}. {t}")
    choice = input("\nSelect show number (or 0 to go back): ").strip()
    if choice == "0":
        return None
    if not choice.isdigit() or not (1 <= int(choice) <= len(shows[m_id])):
        print("Invalid choice.")
        pause()
        return None
    return shows[m_id][int(choice) - 1]


def select_seats(m_id, show_time):
    grid = seat_maps[m_id][show_time]
    print_header(f"{movies[m_id]['title']} | {show_time}")
    print_seat_map(grid)
    raw = input("Enter seats to book (e.g. A1,A2,B5) or 0 to go back: ").strip().upper()
    if raw == "0":
        return None

    seat_list = [s.strip() for s in raw.split(",") if s.strip()]
    if not seat_list:
        print("No seats entered.")
        pause()
        return None

    parsed = []
    for s in seat_list:
        if len(s) < 2 or not s[0].isalpha() or not s[1:].isdigit():
            print(f"Invalid seat format: {s}")
            pause()
            return None
        row = ord(s[0]) - 65
        col = int(s[1:]) - 1
        if not (0 <= row < ROWS) or not (0 <= col < COLS):
            print(f"Seat out of range: {s}")
            pause()
            return None
        if grid[row][col] == "X":
            print(f"Seat {s} is already booked.")
            pause()
            return None
        parsed.append((row, col, s))

    return parsed


def confirm_bookings(m_id, show_time, seats):
    grid = seat_maps[m_id][show_time]
    price = movies[m_id]["price"]
    total = price * len(seats)

    print_header("CONFIRM BOOKING")
    print(f"Movie : {movies[m_id]['title']}")
    print(f"Show : {show_time}")
    print(f"Seats : {', '.join(s[2] for s in seats)}")
    print(f"Price : Rs.{price} x {len(seats)} = Rs.{total}")

    name = input("\nEnter your name: ").strip()
    if not name:
        name = "Guest"

    confirm = input("Confirm booking? (y/n): ").strip().lower()
    if confirm != "y":
        print("Booking cancelled.")  
        pause()  
        return  


    global booking_counter
    booking_counter += 1
    booking_id = f"BK{booking_counter}"

    for row, col, _ in seats:
        grid[row][col] = "X"

    bookings[booking_id] = {
        "name": name,
        "movie": movies[m_id]["title"],
        "show_time": show_time,
        "seats": [s[2] for s in seats],
        "total": total,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
    }
    cursor.execute( ## SQL Insert 
        "INSERT INTO bookings (booking_id, name, movie, show_time, seats, total, timestamp) VALUES (?, ?, ?, ?, ?, ?, ?)",
        (
            booking_id,
            name,
            movies[m_id]["title"],
            show_time,
            ", ".join(s[2] for s in seats),
            total,
            bookings[booking_id]["timestamp"],
        ),
    )
    conn.commit()

    print_header("BOOKING CONFIRMED")
    print(f"Booking ID : {booking_id}")
    print(f"Name       : {name}")
    print(f"Movie      : {movies[m_id]['title']}")
    print(f"Show Time  : {show_time}")
    print(f"Seats      : {', '.join(s[2] for s in seats)}")
    print(f"Total Paid : Rs.{total}")
    print(f"Booked On  : {bookings[booking_id]['timestamp']}")
    pause()


def book_ticket_flow():
    m_id = select_movie()
    if not m_id:
        return
    show_time = select_show(m_id)
    if not show_time:
        return
    seats = select_seats(m_id, show_time)
    if not seats:
        return
    confirm_bookings(m_id, show_time, seats)


def view_bookings():
    print_header("ALL BOOKINGS")
    cursor.execute("SELECT booking_id, name, movie, show_time, seats, total, timestamp FROM bookings") ## SQL view in code 
    rows = cursor.fetchall()
    if not rows:
        print("No bookings yet.")
        pause()
        return
    for bid, name, movie, show_time, seats, total, timestamp in rows:
        print(f"\nBooking ID : {bid}")
        print(f"Name        : {name}")
        print(f"Movie       : {movie}")
        print(f"Show Time   : {show_time}")
        print(f"Seats       : {seats}")
        print(f"Total Paid : Rs.{total}")
        print(f"Booked On  : {timestamp}")
        print("-" * 40)
    pause()


def cancel_booking():
    print_header("CANCEL BOOKING")
    bid = input("Enter Booking ID to cancel: ").strip().upper()

    cursor.execute("SELECT * FROM bookings")
    all_rows = cursor.fetchall()

    found_row = None
    for row in all_rows:
        if row[0] == bid:
            found_row = row
            break

    if found_row is None:
        print("Booking ID not found.")
        pause()
        return

    movie_id = found_row[2]
    show_time = found_row[4]
    seats = found_row[5]

    if movie_id in seat_maps and show_time in seat_maps[movie_id]:
        grid = seat_maps[movie_id][show_time]
        seat_list = seats.split(", ")
        for s in seat_list:
            row_num = ord(s[0]) - 65
            col_num = int(s[1:]) - 1
            grid[row_num][col_num] = "O"

    cursor.execute("DELETE FROM bookings WHERE booking_id = ?", (bid,)) ## SQL DELETE
    conn.commit()
    bookings.pop(bid, None)

    print(f"Booking {bid} cancelled successfully.")
    pause()


def view_seat_availability():
    m_id = select_movie()
    if not m_id:
        return
    show_time = select_show(m_id)
    if not show_time:
        return
    print_header(f"{movies[m_id]['title']} | {show_time}")
    print_seat_map(seat_maps[m_id][show_time])
    pause()

def chat_with_assistant(): ## chatbot
    print_header("MOVIE ASSISTANT CHATBOT")
    print("Movies, prices, ya showtimes ke baare mein kuch bhi pucho. Wapas jaane ke liye 'exit' likho.\n")

    system_prompt = get_live_context()

    chat = client.chats.create( ##chatbot
        model="gemini-flash-latest",
        config={"system_instruction": system_prompt},
    )

    while True:
        user_input = input("You: ").strip()
        if user_input.lower() == "exit":
            break
        if not user_input:
            continue

        print("Assistant is typing...")

        try:
            response = chat.send_message(user_input)
            print(f"\nAssistant: {response.text}\n")
        except Exception as e:
            print(f"\n[Error: {e}]\n")

    pause()


def main_menu():
    while True:
        print_header("MOVIE TICKET BOOKING SYSTEM")
        print("1. View Movies")
        print("2. Book Ticket")
        print("3. View Seat Availability")
        print("4. View All Bookings")
        print("5. Cancel Booking")
        print("6. Chat with Movie Assistant")
        print("7. Exit")

        choice = input("\nEnter your choice: ").strip()

        if choice == "1":
            show_movies()
            pause()
        elif choice == "2":
            book_ticket_flow()
        elif choice == "3":
            view_seat_availability()
        elif choice == "4":
            view_bookings()
        elif choice == "5":
            cancel_booking()
        elif choice == "6":
            chat_with_assistant()
        elif choice == "7":
            print("\nThank you for using the booking system. Goodbye!")
            sys.exit()
        else:
            print("Invalid choice.")
            pause()


if __name__ == "__main__":
    init_db() ## for SQL
    init_chatbot() ## for chatbot
    main_menu()
