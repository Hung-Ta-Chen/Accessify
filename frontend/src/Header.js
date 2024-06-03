import React from "react";
import "./Header.css";
import FilteredSearchBar from "./FilteredSearchBar";

function Header({ handleNearbySearch }) {
  return (
    <header className="site-header">
      <h1>Accessify</h1>
      <FilteredSearchBar handleNearbySearch={handleNearbySearch} />
    </header>
  );
}

export default Header;
