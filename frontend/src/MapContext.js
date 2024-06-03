import React, { createContext } from "react";

// Define a context for holding the map instances
const MapContext = createContext({
  map: null,
  setMap: () => {},
  markers: null,
  setMarkers: () => {},
  center: null,
  setCenter: () => {},
  selectedMarker: null,
  setSelectedMarker: () => {},
  checkedFilters: null,
  setCheckedFilters: () => {},
  showDropdown: null,
  setShowDropdown: () => {},
  distance: null,
  setDistance: () => {},
  searchMode: null,
  setSearchMode: () => {},
  geocoderRef: null,
  placesServiceRef: null,
  userLocation: null,
  setUserLocation: () => {},
});

export default MapContext;
