import React, { useState, useEffect, useContext } from "react";
import { Marker } from "@react-google-maps/api";
import MapContext from "./MapContext";
import "./LocatorButton.css";

const LocatorButton = ({ handleNearbySearch }) => {
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
    userLocation,
    setUserLocation,
  } = useContext(MapContext);

  // Callback function for getting the user location
  const onLocatorButtonClicked = () => {
    const handleResults = (location) => {
      setCenter(location);

      const service = placesServiceRef.current;
      const filterTypes = Object.keys(checkedFilters).filter(
        (key) => checkedFilters[key]
      );

      let allMarkers = [];

      // Start searching from the first type
      handleNearbySearch(location, service, filterTypes, 0, allMarkers, false);
    };

    handleResults(
      new window.google.maps.LatLng(userLocation["lat"], userLocation["lng"])
    );
  };

  return (
    <>
      <button
        className="locator-button"
        onClick={onLocatorButtonClicked}
        title={"Locate me"}
      >
        <svg
          xmlns="http://www.w3.org/2000/svg"
          width="24"
          height="24"
          fill="none"
          stroke="#5f6368"
          strokeLinecap="round"
          strokeLinejoin="round"
          strokeWidth="2"
          className="feather feather-crosshair"
          viewBox="0 0 24 24"
        >
          <circle cx="12" cy="12" r="11" />
          <line x1="24" x2="18" y1="12" y2="12" />
          <line x1="6" x2="0" y1="12" y2="12" />
          <line x1="12" x2="12" y1="6" y2="0" />
          <line x1="12" x2="12" y1="24" y2="18" />
        </svg>
      </button>
    </>
  );
};

export default LocatorButton;
