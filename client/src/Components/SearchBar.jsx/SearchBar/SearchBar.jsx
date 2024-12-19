import React, { useState, useEffect } from "react";
import "./SearchBar.css";
import SearchInput from "../../SearchInput/SearchInput";
import AutocompleteOptions from "../../AutoCompleteOptions/AutoCompleteOptions";


function SearchBar({ options, onNavigate }) {
  const [query, setQuery] = useState("");
  const [filteredOptions, setFilteredOptions] = useState([]);
  const [selectedIndex, setSelectedIndex] = useState(0); // Default to the first option

  const handleInputChange = (value) => {
    setQuery(value);
    setFilteredOptions(getFilteredOptions(value));
    setSelectedIndex(0); // Reset to highlight the first option
  };

  // Function to fetch filtered options from the backend
  const getFilteredOptions = async (query) => {
    try {
      const response = await fetch("http://localhost:5000/filter-options", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ query }),
      });
      const data = await response.json();
      setFilteredOptions(data); // Update state with filtered options
    } catch (error) {
      console.error("Error fetching filtered options:", error);
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === "ArrowDown") {
      // Navigate down
      setSelectedIndex((prevIndex) =>
        prevIndex < filteredOptions.length - 1 ? prevIndex + 1 : 0
      );
    } else if (e.key === "ArrowUp") {
      // Navigate up
      setSelectedIndex((prevIndex) =>
        prevIndex > 0 ? prevIndex - 1 : filteredOptions.length - 1
      );
    } else if (e.key === "Enter") {
      // Trigger navigation for the selected option
      if (filteredOptions.length > 0) {
        const selectedOption = filteredOptions[selectedIndex];
        onNavigate(selectedOption);
        setQuery(selectedOption);
        setFilteredOptions([]);
      }
    }
  };

  const handleOptionSelect = (option) => {
    onNavigate(option);
    setQuery(option);
    setFilteredOptions([]);
  };

  const handleOptionHover = (index) => {
    setSelectedIndex(index);
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (filteredOptions.length > 0) {
      const selectedOption = filteredOptions[selectedIndex];
      onNavigate(selectedOption);
      setQuery(selectedOption);
      setFilteredOptions([]);
    }
  };

  useEffect(() => {
    // Automatically highlight the first option if the list updates
    if (filteredOptions.length > 0) {
      setSelectedIndex(0);
    }
  }, [filteredOptions]);

  return (
    <form className="search-bar" onSubmit={handleSubmit}>
      <SearchInput
        value={query}
        onChange={handleInputChange}
        onKeyDown={handleKeyDown}
      />
      <button className="submit-btn" type="submit" disabled={!query.trim()}>
        Submit
      </button>
      {filteredOptions.length > 0 && (
        <AutocompleteOptions
          options={filteredOptions}
          selectedIndex={selectedIndex}
          onHover={handleOptionHover}
          onSelect={handleOptionSelect}
        />
      )}
    </form>
  );
}

export default SearchBar;
