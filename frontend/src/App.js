import React, { useState, useRef } from "react";
import "./App.css";
import MapContainer from "./MapContainer";
import Header from "./Header";
import MapContext from "./MapContext";
import ReactModal from "react-modal";
import AddReviewModal from "./AddReviewModal";
import ReviewsModal from "./ReviewsModal";
import NavigationSidebar from "./NavigationSidebar";
import ChatWindow from "./ChatWindow";

const initialCenter = {
  lat: 38.5382,
  lng: -121.7617,
};

const SERVER_URL = process.env.REACT_APP_BACKEND_URL;

// Icon map for markers
const iconMap = {
  parking: "http://maps.gstatic.com/mapfiles/ms2/micons/parkinglot.png",
  restaurant: "http://maps.gstatic.com/mapfiles/ms2/micons/restaurant.png",
  park: "http://maps.gstatic.com/mapfiles/ms2/micons/tree.png",
  hospital: "http://maps.gstatic.com/mapfiles/ms2/micons/hospitals.png",
};

// Bind the modals to the app
ReactModal.setAppElement("#root");

function App() {
  // States used across the app
  const [map, setMap] = useState(null);
  const [center, setCenter] = useState(initialCenter);
  const [markers, setMarkers] = useState([]);
  const [selectedMarker, setSelectedMarker] = useState(null);
  const geocoderRef = useRef(null);
  const placesServiceRef = useRef(null);
  const [userLocation, setUserLocation] = useState(null);
  const [activeSidebarWindow, setActiveSidebarWindow] = useState("");

  // Setting in search bar
  const [checkedFilters, setCheckedFilters] = useState({
    parking: true,
    restaurant: true,
    park: true,
    hospital: true,
  });

  const [showDropdown, setShowDropdown] = useState(false);
  const [distance, setDistance] = useState(1);
  const [searchMode, setSearchMode] = useState("lite");

  const [addReviewModalIsOpen, setAddReviewModalIsOpen] = useState(false);
  const [reviewsModalIsOpen, setReviewsModalIsOpen] = useState(false);
  const [reviews, setReviews] = useState([]);

  const handleOpenAddReviewModal = (marker) => {
    setAddReviewModalIsOpen(true);
  };

  const handleOpenReviewsModal = async (marker) => {
    // Fetch or set reviews for the selected marker here
    // Communicate with backend

    try {
      // Fetch the place details by place_id
      const placeResponse = await fetch(
        `${SERVER_URL}/api/places/${marker.id}`
      );
      if (placeResponse.status === 404) {
        alert("Place not found. No reviews available.");
        setReviews([]);
        return;
      }
      if (!placeResponse.ok) {
        throw new Error("Failed to fetch place details");
      }

      const placeData = await placeResponse.json();

      // Fetch reviews for the found place ID
      const reviewResponse = await fetch(
        `${SERVER_URL}/api/places/${placeData.place_id}/reviews`
      );
      if (reviewResponse.status === 404) {
        alert("No reviews found for this place.");
        setReviews([]);
        return;
      }
      if (!reviewResponse.ok) {
        throw new Error("Failed to fetch reviews");
      }

      const reviewsData = await reviewResponse.json();
      setReviews(reviewsData); // Set the fetched reviews into state
      setReviewsModalIsOpen(true); // Open the reviews modal
    } catch (error) {
      console.error("Error fetching place or reviews:", error);
      alert("Error fetching place or reviews");
    }
  };

  const handleCloseAddReviewModal = () => {
    setAddReviewModalIsOpen(false);
  };

  const handleCloseReviewsModal = () => {
    setReviewsModalIsOpen(false);
  };

  // Function for posting reviews to DB
  const handleAddReviewSubmit = async (reviewData) => {
    try {
      // Check if the place exists or add it
      let placeResponse = await fetch(
        `${SERVER_URL}/api/places/${selectedMarker.id}`
      );

      if (placeResponse.status === 404) {
        // If the place is not found, try to create it
        placeResponse = await fetch(`${SERVER_URL}/api/places`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            name: selectedMarker.title,
            lat: selectedMarker.lat,
            lng: selectedMarker.lng,
            place_id: selectedMarker.id,
            place_type: selectedMarker.type,
          }),
        });

        if (!placeResponse.ok) throw new Error("Failed to create place");
      }

      const placeData = await placeResponse.json();
      const placeId = placeData.place_id;

      // Submit the review
      const reviewResponse = await fetch(
        `${SERVER_URL}/api/places/${placeId}/reviews`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            place: placeId,
            username: reviewData.username,
            wheelchair_rating: reviewData.wheelchairRating,
            restroom_rating: reviewData.restroomRating,
            overall_rating: reviewData.overallRating,
            comment: reviewData.comments,
          }),
        }
      );
      if (reviewResponse.ok) {
        alert("Review successfully added!");
        handleCloseAddReviewModal();
      } else {
        throw new Error("Failed to submit review");
      }
    } catch (error) {
      console.error("Failed to handle review submission:", error);
      alert("Error handling review submission");
    }
  };

  const handleCloseSidebarWindow = () => {
    setActiveSidebarWindow(""); // Clears any active sidebar window to close it
  };

  // Function for searching nearby places with Places API
  // Use recursive function for searching nearby places instead of for-loop to avoid exceeding rate limit
  const searchNearbyPlaces = (
    location,
    service,
    filterTypes,
    index,
    allMarkers,
    showTargetLocation = true
  ) => {
    if (index < filterTypes.length) {
      // Construct a request object
      const request = {
        location: location,
        radius: distance * 1000, // in meters
        type: filterTypes[index],
      };

      // Send the request to the service
      service.nearbySearch(request, (results, status, pagination) => {
        if (status === window.google.maps.places.PlacesServiceStatus.OK) {
          // Map each place object in result to a marker object
          const newMarkers = results.map((place) => ({
            lat: place.geometry.location.lat(),
            lng: place.geometry.location.lng(),
            title: place.name,
            icon: {
              url: iconMap[filterTypes[index]],
              scaledSize: new window.google.maps.Size(40, 40), // Scale the icon
            },
            id: place.place_id,
            googleRating: place.rating || 0,
            googleRatingsCount: place.user_ratings_total || 0,
            type: filterTypes[index],
          }));

          allMarkers.push(...newMarkers);
          // Check if pagination is available and if the next page is available
          // Also use search mode flag to control pagination
          if (searchMode == "full" && pagination && pagination.hasNextPage) {
            // If more results are available, keep fetching
            setTimeout(() => pagination.nextPage(), 200); // respect API limit
          } else {
            // No more results, process next type
            searchNearbyPlaces(
              location,
              service,
              filterTypes,
              index + 1,
              allMarkers,
              showTargetLocation
            ); // Recurse to search next type
          }
        } else {
          // Proceed to next type even if current search fails
          searchNearbyPlaces(
            location,
            service,
            filterTypes,
            index + 1,
            allMarkers,
            showTargetLocation
          );
        }
      });
    } else {
      // Set all the combined markers after searching nearby places
      // Don't use location.lat, location.lng!!!
      if (showTargetLocation) {
        allMarkers.push({
          lat: location.lat(),
          lng: location.lng(),
          title: "Target Location",
          icon: "",
          id: null,
          googleRating: 0,
          googleRatingsCount: 0,
        });
      }
      setMarkers(allMarkers);
    }
  };

  return (
    <MapContext.Provider
      value={{
        map,
        setMap,
        markers,
        setMarkers,
        center,
        setCenter,
        selectedMarker,
        setSelectedMarker,
        checkedFilters,
        setCheckedFilters,
        showDropdown,
        setShowDropdown,
        distance,
        setDistance,
        searchMode,
        setSearchMode,
        geocoderRef,
        placesServiceRef,
        userLocation,
        setUserLocation,
      }}
    >
      <div className="App">
        <NavigationSidebar
          activeSidebarWindow={activeSidebarWindow}
          setActiveSidebarWindow={setActiveSidebarWindow}
        />
        <div className="main-content">
          <Header handleNearbySearch={searchNearbyPlaces} />
          <MapContainer
            onAddReview={handleOpenAddReviewModal}
            onDisplayReviews={handleOpenReviewsModal}
            handleNearbySearch={searchNearbyPlaces}
          />
          <ReviewsModal
            isOpen={reviewsModalIsOpen}
            onRequestClose={handleCloseReviewsModal}
            reviews={reviews} // Pass the reviews for the selected marker
          />
          <AddReviewModal
            isOpen={addReviewModalIsOpen}
            onRequestClose={handleCloseAddReviewModal}
            onReviewSubmit={handleAddReviewSubmit}
          />
        </div>
        {
          <ChatWindow
            handleClose={handleCloseSidebarWindow}
            isActive={activeSidebarWindow === "chat"}
          />
        }
      </div>
    </MapContext.Provider>
  );
}

export default App;
