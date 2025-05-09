// Replace this with your Google Maps API key
const apiKey = 'AIzaSyCkPmUz4UlRdzcKG9gniW9Qfrgzsjhnb_4';

// Default user location (can be changed dynamically)
let userLocation = { lat: 19.0760, lng: 72.8777 }; // Mumbai coordinates as default

// Function to get URL parameters by name
function getQueryParameter(name) {
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get(name);
}

function initMap() {
    // Extracting the user's latitude and longitude from URL parameters
    const userLat = parseFloat(getQueryParameter('user_lat')) || userLocation.lat;
    const userLon = parseFloat(getQueryParameter('user_lon')) || userLocation.lng;
    userLocation = { lat: userLat, lng: userLon };

    // Define custom map styles
    const customStyle = [
        {
            "featureType": "road.highway",
            "elementType": "geometry.stroke",
            "stylers": [
                { "color": "#ffa500" }, // Orange border for highways
                { "weight": 2 } // Slightly thicker stroke
            ]
        },
        {
            "featureType": "road.highway",
            "elementType": "geometry.fill",
            "stylers": [
                { "color": "#ffff4d" } // Yellow fill for highways
            ]
        },
        {
            "featureType": "road.highway",
            "elementType": "labels.text.fill",
            "stylers": [
                { "color": "#000000" } // Dark text for highway labels
            ]
        }
    ];

    // Initialize the Google Map with custom styles
    const map = new google.maps.Map(document.getElementById('map'), {
        center: userLocation,
        zoom: 14,
        disableDefaultUI: true, // Disable default map controls
        styles: customStyle
    });

    // Add a marker for the user's location
    const userMarker = new google.maps.Marker({
        position: userLocation,
        map: map,
        icon: 'https://img.icons8.com/color/48/000000/marker.png' // Customize marker icon
    });

    // Fetch Woloo washroom locations and plot them
    fetchWashroomLocations(userLocation.lat, userLocation.lng).then(washroomLocations => {
        // Add markers for each Woloo washroom location
        washroomLocations.forEach(location => {
            const marker = new google.maps.Marker({
                position: { lat: location.latitude, lng: location.longitude },
                map: map,
                title: location.name,
                icon: 'https://img.icons8.com/color/48/000000/toilet.png' // Custom icon for washrooms
            });

            // Add click event to each marker to show route from the user's location to this Woloo location
            marker.addListener('click', () => {
                showRoute(userLocation, marker.getPosition(), map);
            });
        });
    });

    // Get visited Woloo room coordinates from URL and plot the route
    const visitedLat = parseFloat(getQueryParameter('room_lat'));
    const visitedLon = parseFloat(getQueryParameter('room_lon'));

    if (visitedLat && visitedLon) {
        const visitedLocation = { lat: visitedLat, lng: visitedLon };

        // Plot the route to the visited Woloo room
        showRoute(userLocation, visitedLocation, map);
    } else {
        console.log('No specific Woloo room visited.');
    }
}

// Function to fetch washroom locations from Flask backend
async function fetchWashroomLocations(lat, lon) {
    try {
        const response = await fetch(`/get_woloo_locations?lat=${lat}&lon=${lon}`);
        if (!response.ok) {
            throw new Error('Error fetching washroom locations: ' + response.statusText);
        }
        return await response.json(); // Assuming the response is in JSON format
    } catch (error) {
        console.error(error);
        return []; // Return an empty array on error
    }
}

// Function to show route from user location to selected Woloo location
function showRoute(origin, destination, map) {
    const directionsService = new google.maps.DirectionsService();
    const directionsRenderer = new google.maps.DirectionsRenderer();

    directionsRenderer.setMap(map);

    const request = {
        origin: origin,
        destination: destination,
        travelMode: google.maps.TravelMode.WALKING // You can also use DRIVING, BICYCLING, etc.
    };

    directionsService.route(request, (result, status) => {
        if (status === 'OK') {
            directionsRenderer.setDirections(result);
        } else {
            console.error('Directions request failed due to ' + status);
        }
    });
}

// Initialize the map when the page loads
window.onload = initMap;
