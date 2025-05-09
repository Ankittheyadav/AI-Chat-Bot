// Replace this with your Google Maps API key
const apiKey = 'API_KEY'; // Keep this secure

// Default user location (can be changed dynamically)
const userLocation = { lat: 19.126575, lng: 72.844345 }; // Mumbai coordinates as default

function initMap() {
    const map = new google.maps.Map(document.getElementById('map'), {
        center: userLocation,
        zoom: 14,
        disableDefaultUI: true,
    });

    const userMarker = new google.maps.Marker({
        position: userLocation,
        map: map,
        icon: 'https://img.icons8.com/color/48/000000/marker.png',
    });

    // Fetch washroom locations from the server
    fetchWashroomLocations(userLocation.lat, userLocation.lng).then(washroomLocations => {
        washroomLocations.forEach(location => {
            const marker = new google.maps.Marker({
                position: { lat: location.latitude, lng: location.longitude },
                map: map,
                title: location.name,
                icon: 'https://img.icons8.com/color/48/000000/toilet.png',
            });

            // Add click event to each marker to show route
            marker.addListener('click', () => {
                showRoute(userLocation, { lat: location.latitude, lng: location.longitude }, map);
            });
        });
    });

    // Read origin and destination from URL parameters
    const origin = getQueryParameter('origin');
    const destination = getQueryParameter('destination');

    if (origin && destination) {
        const originCoords = {
            lat: parseFloat(origin.split(',')[0]),
            lng: parseFloat(origin.split(',')[1]),
        };
        const destinationCoords = {
            lat: parseFloat(destination.split(',')[0]),
            lng: parseFloat(destination.split(',')[1]),
        };

        // Plot the route on the map
        showRoute(originCoords, destinationCoords, map);
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
        return []; // Return an empty array in case of error
    }
}

// Function to show route from user location to selected Woloo location
function showRoute(origin, destination, map) {
    const directionsService = new google.maps.DirectionsService();
    const directionsRenderer = new google.maps.DirectionsRenderer({
        suppressMarkers: true
    });

    directionsRenderer.setMap(map);

    const request = {
        origin: origin,
        destination: destination,
        travelMode: google.maps.TravelMode.WALKING,
    };

    directionsService.route(request, (result, status) => {
        if (status === 'OK') {
            directionsRenderer.setDirections(result);
        } else {
            console.error('Directions request failed due to ' + status);
        }
    });
}

// Function to get URL parameters by name
function getQueryParameter(name) {
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get(name);
}



// Initialize the map once the page loads
window.onload = initMap;
