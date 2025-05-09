from flask import Flask, request, render_template, jsonify
from twilio.twiml.messaging_response import MessagingResponse
import mysql.connector
import math
from flask_cors import CORS
import markdown 

app = Flask(__name__)
CORS(app)

# Step 1: Define welcome message
WELCOME_MESSAGE = (
    "Hello! Welcome to Woloo. I can help you find the nearest Woloo's locations around you. "
    "How can I assist you today?\n\n"
    "1. Find Nearest Woloo’s\n"
    "2. Learn More About Woloo\n"
    "3. Download the App\n"
    "4. Contact Support"
)
@app.route('/')  # Home route for rendering index.html
def index():
    return render_template('index.html')


LOCATION_REQUEST_MESSAGE = (
    "Please share your location so I can show you the nearest Woloo's.\n\n"
    "To share your live location on WhatsApp:\n"
    "1. Tap the attach (paperclip) icon next to the message input.\n"
    "2. Select 'Location'.\n"
    "3. Choose 'Share live location' or send your current location."
)

# Database connection function
def connect_db():
    try:
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="ankit",
            database="chatbot"
        )
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

# Haversine formula to calculate distance between two points (lat1, lon1) and (lat2, lon2)
def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # Earth radius in kilometers
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat / 2) ** 2 +
         math.cos(math.radians(lat1)) *
         math.cos(math.radians(lat2)) *
         math.sin(dlon / 2) ** 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c  # Distance in kilometers

# Calculate time to reach a location based on distance and a constant speed (e.g., walking speed = 5 km/h)
def calculate_time_to_reach(distance_km, speed_kmh=5):
    return distance_km / speed_kmh * 60  # Time in minutes

# Function to get Woloo locations from the database
def get_woloo_locations():
    connection = connect_db()
    cursor = connection.cursor(dictionary=True)

    # Query to fetch all Woloo locations
    cursor.execute("SELECT name, latitude, longitude, rating FROM woloo_rooms")
    locations = cursor.fetchall()
    cursor.close()
    connection.close()
    return locations

# Function to get the n nearest Woloo rooms
def get_nearest_woloo_rooms(user_lat, user_lon, n=4):
    woloo_locations = get_woloo_locations()
    print("Fetched Woloo Locations: ", woloo_locations)  # Debugging statement

    distances = []
    for location in woloo_locations:
        try:
            lat = float(location['latitude'])
            lon = float(location['longitude'])

            # Calculate the distance using the haversine formula
            distance = haversine(user_lat, user_lon, lat, lon)
            time_to_reach = calculate_time_to_reach(distance)  # Calculate estimated time to reach
            distances.append({
                "name": location['name'],
                "distance": distance,
                "rating": location['rating'],  # Assuming this is an INT
                "time_to_reach": time_to_reach,
                "latitude": lat,  # Save the latitude for Google Maps link
                "longitude": lon  # Save the longitude for Google Maps link
            })
            print(f"Processed location: {location['name']}, Distance: {distance:.2f} km, Time to reach: {time_to_reach:.2f} minutes")
        except Exception as e:
            print(f"Error processing location {location['name']}: {e}")  # Error handling for invalid data

    # Sort by distance and return the nearest n locations
    sorted_locations = sorted(distances, key=lambda x: x['distance'])
    print("Sorted Locations: ", sorted_locations)  # Debugging statement
    return sorted_locations[:n]

# New API endpoint for fetching Woloo locations
@app.route("/api/woloo-locations", methods=['GET'])
def get_woloo_locations_api():
    # Get latitude and longitude from query parameters
    user_lat = request.args.get('lat')
    user_lon = request.args.get('lon')
     # Validate the latitude and longitude
    try:
        nearest_rooms = get_nearest_woloo_rooms(float(user_lat), float(user_lon))
        locations = [{"name": room['name'], "latitude": room['latitude'], "longitude": room['longitude'], "rating": room['rating'], "distance": room['distance'], "time_to_reach": room['time_to_reach']} for room in nearest_rooms]
        return jsonify({"locations": locations})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


    # Prepare the response
    locations = []
    for room in nearest_rooms:
        locations.append({
            "name": room['name'],
            "latitude": room['latitude'],
            "longitude": room['longitude'],
            "rating": room['rating'],
            "distance": room['distance'],
            "time_to_reach": room['time_to_reach']
        })

    return {"locations": locations}  # Return as JSON response

@app.route("/twilio-webhook", methods=['POST'])
def whatsapp_reply():
    incoming_msg = request.values.get('Body', '').lower()
    incoming_latitude = request.values.get('Latitude')
    incoming_longitude = request.values.get('Longitude')

    response = MessagingResponse()

    # Log incoming message and location data for debugging
    print(f"Incoming message: {incoming_msg}")  
    print(f"Incoming latitude: {incoming_latitude}, Incoming longitude: {incoming_longitude}") 

    if incoming_latitude and incoming_longitude:
        try:
            user_lat = float(incoming_latitude)
            user_lon = float(incoming_longitude)

            # Fetch nearest Woloo rooms
            nearest_rooms = get_nearest_woloo_rooms(user_lat, user_lon, n=4)

            # Initialize the response message
            response_message = ""

            # Check if there are nearby rooms to show
            if nearest_rooms:
                response_message = "Here are the nearest Woloo's locations:\n\n"
                for i, room in enumerate(nearest_rooms, 1):
                    # Create a URL for each room name
                    room_coordinates = ','.join([f"{r['latitude']},{r['longitude']}" for r in nearest_rooms])
                    room_link = (
                        f"http://127.0.0.1:3000/user_lat={user_lat}&user_lon={user_lon}"
                        f"&rooms={room_coordinates}"
                    )

                    # Format the response message with clickable URLs using Markdown format
                    response_message += (
                        f"{i}. {room['name']} - {room['distance']:.2f} km away\n"
                        f"   Rating: {room['rating']}/5\n"
                        f"   Estimated time to reach: {room['time_to_reach']:.2f} minutes walk\n"
                        f"   [Visit this location]({room_link})\n\n"
                    )

                    
            else:
                 response_message = "Sorry, no nearby Woloo's locations found."
    

            # Add download links for Apple Store and Google Play Store
            response_message += "\nDownload the Woloo app:\n"
            response_message += "Apple Store: https://apps.apple.com/app/id123456789\n"
            response_message += "Google Play Store: https://play.google.com/store/apps/details?id=in.woloo.www&hl=en\n"
            
            # Add contact support option
            response_message += "\nNeed help? Contact Woloo support:\n"
            response_message += "Email: support@woloo.in\n"
            response_message += "Phone: +91-XXXXXXXXXX"

            # Map screenshot image URL (replace with your actual URL)
            custom_image_url = "https://res.cloudinary.com/dpkpnj7fo/image/upload/v1727343886/WhatsApp_Image_2024-09-25_at_01.05.18_074bc305_mmghs3.jpg"

            print(f"Response message: {response_message}")  # Log the final response message

            # Send the response message along with the image
            msg = response.message(response_message)
            msg.media(custom_image_url)  # Send message with media

        except ValueError as e:
            response_message = "There was an error processing your location. Please try again."
            response.message(response_message)
    else:
        # Handle text-based input and return appropriate messages
        if "hi" in incoming_msg or "hello" in incoming_msg or "help" in incoming_msg:
            response_message = WELCOME_MESSAGE
        elif "1" in incoming_msg or "find nearest" in incoming_msg:
            response_message = LOCATION_REQUEST_MESSAGE
        elif "2" in incoming_msg or "learn more" in incoming_msg:
            response_message = "Woloo provides access to hygienic washrooms across India. Find out more at our website: https://woloo.in/."
        elif "3" in incoming_msg or "download" in incoming_msg:
            response_message = "Download the Woloo app:\n" \
                              "Apple Store: https://apps.apple.com/app/id123456789\n" \
                              "Google Play Store: https://play.google.com/store/apps/details?id=in.woloo.www&hl=en"
        elif "4" in incoming_msg or "contact" in incoming_msg:
            response_message = "Need help? Contact Woloo support:\n" \
                              "Email: support@woloo.in\n" \
                              "Phone: +91-XXXXXXXXXX"
        else:
            response_message = "Sorry, I didn't understand that. Please reply with 'Help' to see the available options."

        response.message(response_message)

    return str(response)

# Start the Flask server
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)