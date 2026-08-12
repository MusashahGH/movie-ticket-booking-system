# 🎬 Movie Ticket Booking System

A comprehensive command-line movie ticket booking system with real-time seat availability tracking and persistent data storage.

## ✨ Features

- **Browse Movies** - View all currently showing movies with language and pricing information
- **Book Tickets** - Interactive seat selection with visual seat map
- **View Seat Availability** - Check available seats for any showtime
- **Manage Bookings** - View all bookings and cancel reservations
- **Persistent Storage** - SQLite database for storing booking records
- **Multiple Showtimes** - Each movie has multiple showtimes throughout the day
- **Seat Management** - Visual seat map with real-time availability updates

## 🗂️ Movie Database

| ID | Movie Title | Language | Price (Rs.) |
|----|-------------|----------|-------------|
| 1 | The Super Mario Galaxy Movie | English | 800 |
| 2 | Spider-Man: Brand New Day | English | 800 |
| 3 | Michael | English | 700 |
| 4 | The Devil Wears Prada 2 | English | 700 |
| 5 | The Odyssey | English | 800 |
| 6 | Jawani Phir Nahi Ani 3 | Urdu | 600 |
| 7 | Quaid-e-Azam Zindabad | Urdu | 600 |
| 8 | Teefa in Trouble | Urdu | 550 |
| 9 | Bhooth Bangla | Urdu | 550 |
| 10 | Parey Hut Love | Urdu | 500 |

## 🎫 Showtimes

Each movie has multiple showtimes throughout the day:
- Morning shows (10:00 AM - 12:00 PM)
- Afternoon shows (1:00 PM - 5:30 PM)
- Evening shows (6:00 PM - 10:30 PM)

## 📊 Seat Layout

- **8 Rows** (A-H)
- **10 Columns** (1-10)
- **Total Seats**: 80 per show

### Seat Legend
- `O` = Available
- `X` = Booked

### Seat Labels
- Format: `[Row Letter][Column Number]`
- Examples: `A1`, `B5`, `H10`

## 🚀 Installation & Setup

### Prerequisites
- Python 3.x
- SQLite3 (built-in with Python)

### Steps

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/movie-ticket-booking-system.git
cd movie-ticket-booking-system
```

2. **Run the application**
```bash
python movie_ticket_code.py
```

## 💻 How to Use

### Main Menu Options

1. **View Movies**
   - Display all available movies with details

2. **Book Ticket**
   - Select a movie by ID
   - Choose a showtime
   - Enter seat numbers (e.g., `A1,A2,B5`)
   - Confirm booking with your name

3. **View Seat Availability**
   - Select a movie and showtime
   - View the current seat map

4. **View All Bookings**
   - Display all booking records from the database

5. **Cancel Booking**
   - Enter the Booking ID to cancel
   - Seats will be released automatically

6. **Exit**
   - Close the application

### Booking Process

1. **Select Movie** → Choose from the movie list
2. **Select Showtime** → Pick from available showtimes
3. **Select Seats** → Enter seat numbers (e.g., `A1,B2,C3`)
4. **Enter Name** → Provide your name for the booking
5. **Confirm** → Review and confirm your booking

## 💾 Database Structure

The system uses SQLite with the following table structure:

```sql
CREATE TABLE bookings (
    booking_id TEXT PRIMARY KEY,
    name TEXT,
    movie TEXT,
    show_time TEXT,
    seats TEXT,
    total INTEGER,
    timestamp TEXT
)
```

## 🎯 Example Workflow

```bash
1. Run the program
2. Select "2. Book Ticket"
3. Enter Movie ID: 1
4. Select show number: 1 (for 10:00 AM)
5. Enter seats: A1,A2
6. Enter name: John Doe
7. Confirm: y
8. Booking confirmed with ID: BK1001
```

## 📝 Booking ID Format

- Format: `BK[Number]`
- Example: `BK1001`, `BK1002`
- Auto-increments with each booking

## 🛡️ Error Handling

The system handles various error cases:
- Invalid movie IDs
- Already booked seats
- Out-of-range seat selection
- Invalid seat formats
- Non-existent booking IDs for cancellation

## 🔧 Technical Details

### Dependencies
- `os` - For screen clearing
- `sys` - For system operations
- `sqlite3` - For database management
- `datetime` - For timestamp generation

### Key Functions
- `init_db()` - Initialize SQLite database
- `book_ticket_flow()` - Main booking workflow
- `view_bookings()` - Display all bookings
- `cancel_booking()` - Cancel existing bookings
- `print_seat_map()` - Display visual seat layout

## 🔄 Data Persistence

- All bookings are stored in `movie_tickets.db`
- The database persists between program runs
- Seat availability is maintained across sessions

## 📌 Notes

- The system uses in-memory seat maps initialized at startup
- Bookings are saved to SQLite for permanent storage
- The seat map resets when the program restarts
- Booking history is preserved in the database

## 🤝 Contributing

Feel free to fork this repository and submit pull requests for improvements or bug fixes.

## 📄 License

This project is open source and available for educational purposes.

---

**Happy Movie Watching! 🍿**
