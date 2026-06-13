from flask import Flask, render_template, request, redirect
import json
import os

app = Flask(__name__)

ROOM_FILE = "rooms.json"

# Create 100 rooms automatically if file doesn't exist
if not os.path.exists(ROOM_FILE):
    rooms = {}
    for i in range(101, 201):
        rooms[str(i)] = None

    with open(ROOM_FILE, "w") as f:
        json.dump(rooms, f, indent=4)


def load_rooms():
    with open(ROOM_FILE, "r") as f:
        return json.load(f)


def save_rooms(data):
    with open(ROOM_FILE, "w") as f:
        json.dump(data, f, indent=4)


@app.route('/')
def home():

    rooms = load_rooms()

    total_rooms = len(rooms)

    occupied_rooms = 0

    for student in rooms.values():
        if student is not None:
            occupied_rooms += 1

    available_rooms = total_rooms - occupied_rooms

    occupancy_percentage = round(
        (occupied_rooms / total_rooms) * 100, 2
    )

    return render_template(
        "index.html",
        rooms=rooms,
        total_rooms=total_rooms,
        occupied_rooms=occupied_rooms,
        available_rooms=available_rooms,
        occupancy_percentage=occupancy_percentage
    )

@app.route('/allocate', methods=['POST'])
def allocate():

    name = request.form['name']
    room = request.form['room']

    rooms = load_rooms()

    if rooms[room] is None:
        rooms[room] = name
        save_rooms(rooms)

    return redirect('/')


@app.route('/vacate/<room>')
def vacate(room):

    rooms = load_rooms()

    rooms[room] = None

    save_rooms(rooms)

    return redirect('/')

@app.route('/ask_ai', methods=['POST'])
def ask_ai():

    question = request.form['question'].lower().strip()

    rooms = load_rooms()

    available = []
    occupied = []

    for room, student in rooms.items():
        if student is None:
            available.append(room)
        else:
            occupied.append((room, student))

    if question in ["hi", "hello", "hey"]:
        answer = "👋 Hello! I'm your Hostel Assistant. How can I help you today?"

    elif "good morning" in question:
        answer = "🌞 Good Morning! Hope you have a wonderful day."

    elif "good night" in question:
        answer = "🌙 Good Night! Take care."

    elif "thank" in question:
        answer = "😊 You're welcome! Happy to help."

    elif "bye" in question:
        answer = "👋 Goodbye! Have a great day."

    elif "who are you" in question:
        answer = "🤖 I am the Hostel Room Assistant developed using Python and Flask."

    elif "available" in question or "vacant" in question:
        answer = f"🏠 Available Rooms Count: {len(available)}"

    elif "occupied" in question:
        answer = f"👥 Occupied Rooms Count: {len(occupied)}"

    elif "total rooms" in question:
        answer = f"🏢 Total Rooms in Hostel: {len(rooms)}"

    elif "occupancy" in question:
        answer = f"📊 Occupancy Rate: {round((len(occupied)/len(rooms))*100,2)}%"

    else:
        answer = """
🤖 I can help with:
• Available Rooms
• Occupied Rooms
• Total Rooms
• Occupancy Rate
• Greetings
• Hostel Statistics
"""

    return {"answer": answer}

@app.route('/search_student', methods=['POST'])
def search_student():

    student_name = request.form['student_name'].lower().strip()

    rooms = load_rooms()

    for room, student in rooms.items():

        if student and student.lower() == student_name:

            return {
                "result": f"🎓 {student} is staying in Room {room}"
            }

    return {
        "result": "❌ Student not found."
    }


if __name__ == "__main__":
    app.run(debug=True)
    