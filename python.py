from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

class Hotel:
    def __init__(self, hotelId, name, location, roomsAvailable, pricePerNight):
        self.hotelId = hotelId
        self.name = name
        self.location = location
        self.roomsAvailable = roomsAvailable
        self.pricePerNight = pricePerNight

class User:
    def __init__(self, userId, name, bookings=None):
        if bookings is None:
            bookings = []
        self.userId = userId
        self.name = name
        self.bookings = bookings

hotels = []
users = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_hotel', methods=['POST'])
def add_hotel():
    data = request.json
    hotel = Hotel(data['hotelId'], data['name'], data['location'], data['roomsAvailable'], data['pricePerNight'])
    hotels.append(hotel)
    return jsonify({'status': 'success'})

@app.route('/add_user', methods=['POST'])
def add_user():
    data = request.json
    user = User(data['userId'], data['name'])
    users.append(user)
    return jsonify({'status': 'success'})

@app.route('/filter_hotels', methods=['GET'])
def filter_hotels():
    location = request.args.get('location').lower()
    filtered_hotels = [hotel.__dict__ for hotel in hotels if hotel.location.lower() == location]
    return jsonify(filtered_hotels)

@app.route('/book_hotel', methods=['POST'])
def book_hotel():
    data = request.json
    userId = data['userId']
    hotelId = data['hotelId']
    user = next((u for u in users if u.userId == userId), None)
    hotel = next((h for h in hotels if h.hotelId == hotelId), None)
    if user and hotel and hotel.roomsAvailable > 0:
        user.bookings.append(hotelId)
        hotel.roomsAvailable -= 1
        return jsonify({'status': 'success'})
    return jsonify({'status': 'failure'})

@app.route('/user_bookings', methods=['GET'])
def user_bookings():
    userId = int(request.args.get('userId'))
    user = next((u for u in users if u.userId == userId), None)
    if user:
        bookings = [hotel.__dict__ for hotelId in user.bookings for hotel in hotels if hotel.hotelId == hotelId]
        return jsonify(bookings)
    return jsonify([])

@app.route('/all_hotels', methods=['GET'])
def all_hotels():
    return jsonify([hotel.__dict__ for hotel in hotels])

if __name__ == '__main__':
    app.run(debug=True)
