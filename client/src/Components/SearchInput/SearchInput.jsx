import React from "react";
import "./SearchInput.css";

const SearchInput = ({ value, onChange, onKeyDown }) => {
  return (
    <input
      type="text"
      value={value}
      onChange={(e) => onChange(e.target.value)}
      onKeyDown={onKeyDown}
      placeholder="Search..."
      className="search-input"
    />
  );
};

export default SearchInput;
