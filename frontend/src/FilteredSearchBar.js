import React, { useState, useContext } from "react";
import "./FilteredSearchBar.css";
import MapContext from "./MapContext";

function FilteredSearchBar({ handleNearbySearch }) {
  const {
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
  } = useContext(MapContext);

  const [locationFormat, setLocationFormat] = useState("addr");
  const [searchText, setSearchText] = useState("");

  const onFilterChange = (event) => {
    const { value, checked } = event.target;

    // Update the state
    setCheckedFilters((prevState) => ({
      ...prevState,
      [value]: checked, // Computed property name
    }));
  };

  const onDistanceChange = (event) => {
    setDistance(event.target.value);
  };

  const onSearchModeChange = (event) => {
    setSearchMode(event.target.value);
  };

  const onLocationFormatChange = (event) => {
    setLocationFormat(event.target.value);
  };

  const onSearchTextChange = (event) => {
    setSearchText(event.target.value);
  };

  const toggleDropdown = () => {
    setShowDropdown(!showDropdown);
  };

  const onSearch = () => {
    // Stop displaying the filters
    setShowDropdown(false);

    // Check if the map is loaded
    if (!map) return;

    const geocoder = geocoderRef.current;
    const handleResults = (location) => {
      setCenter(location);

      const service = placesServiceRef.current;
      const filterTypes = Object.keys(checkedFilters).filter(
        (key) => checkedFilters[key]
      );

      let allMarkers = [];

      // Start searching from the first type
      handleNearbySearch(location, service, filterTypes, 0, allMarkers);
    };

    if (locationFormat === "latlng") {
      const latLng = searchText.split(",").map(Number);
      if (latLng.length === 2 && !isNaN(latLng[0]) && !isNaN(latLng[1])) {
        handleResults(new window.google.maps.LatLng(latLng[0], latLng[1]));
      } else {
        alert("Invalid latitude and longitude format.");
      }
    } else {
      geocoder.geocode({ address: searchText }, (results, status) => {
        if (status === "OK" && results[0]) {
          handleResults(results[0].geometry.location);
        } else {
          alert("Geocoding failed due to: " + status);
        }
      });
    }
  };

  return (
    <div className="search-bar">
      <button onClick={toggleDropdown} className="dropdown-button">
        Filters
      </button>
      <select
        onChange={onDistanceChange}
        value={distance}
        className="distance-toggle"
      >
        <option value="1">1 km</option>
        <option value="5">5 km</option>
        <option value="10">10 km</option>
      </select>
      <select onChange={onLocationFormatChange} value={locationFormat}>
        <option value="latlng">Coordinate</option>
        <option value="addr">Address</option>
      </select>
      <input
        type="text"
        placeholder="Target Location"
        className="search-input"
        onChange={onSearchTextChange}
        value={searchText}
      />
      <select
        onChange={onSearchModeChange}
        value={searchMode}
        className="search-mode-toggle"
      >
        <option value="lite">Lite</option>
        <option value="full">Full</option>
      </select>
      <button onClick={onSearch} className="search-button">
        Search
      </button>
      {showDropdown && (
        <div className="dropdown-content">
          <label>
            <input
              type="checkbox"
              onChange={onFilterChange}
              value="parking"
              checked={checkedFilters.parking}
            />{" "}
            Parking Spot
          </label>
          <label>
            <input
              type="checkbox"
              onChange={onFilterChange}
              value="restaurant"
              checked={checkedFilters.restaurant}
            />{" "}
            Restaurant
          </label>
          <label>
            <input
              type="checkbox"
              onChange={onFilterChange}
              value="park"
              checked={checkedFilters.park}
            />{" "}
            Park
          </label>
          <label>
            <input
              type="checkbox"
              onChange={onFilterChange}
              value="hospital"
              checked={checkedFilters.hospital}
            />{" "}
            Hospital
          </label>
        </div>
      )}
    </div>
  );
}

export default FilteredSearchBar;
