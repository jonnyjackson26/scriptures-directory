import React, { useState, useEffect } from "react";
import "./SearchBar.css";
import SearchInput from "../../SearchInput/SearchInput";
import AutocompleteOptions from "../../AutoCompleteOptions/AutoCompleteOptions";


function SearchBar({ options, onNavigate }) {
  const [query, setQuery] = useState("");
  const [filteredOptions, setFilteredOptions] = useState([]);
  const [selectedIndex, setSelectedIndex] = useState(0); // Default to the first option
  const [isLoading, setIsLoading] = useState(false);

  // Cache to avoid fetching data again if query is repeated
  const [cache, setCache] = useState({});




  const handleInputChange = (value) => {
    setQuery(value);
    setFilteredOptions(getFilteredOptions(value));
    setSelectedIndex(0); // Reset to highlight the first option
  };

  const getFilteredOptions = async (query) => {
    if (cache[query]) {
      setFilteredOptions(cache[query]); // Use cached data if available
      return;
    }

    setIsLoading(true);

    try {
      const response = await fetch("http://localhost:5000/filter-options", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ query }),
      });
      const data = await response.json();
      setCache((prevCache) => ({ ...prevCache, [query]: data })); // Cache the result
      setFilteredOptions(data); // Update state with filtered options
    } catch (error) {
      console.error("Error fetching filtered options:", error);
    }

    setIsLoading(false);
  };

  // Debounce the search to prevent excessive requests
  useEffect(() => {
    const timer = setTimeout(() => {
      if (query) {
        getFilteredOptions(query);
      } else {
        setFilteredOptions([]); // Clear options when query is empty
      }
    }, 300); // Adjust delay as needed (e.g., 300ms)

    return () => clearTimeout(timer); // Cleanup the previous timeout
  }, [query]);

  const handleKeyDown = (e) => {
    if (e.key === "ArrowDown") {
      setSelectedIndex((prevIndex) =>
        prevIndex < filteredOptions.length - 1 ? prevIndex + 1 : 0
      );
    } else if (e.key === "ArrowUp") {
      setSelectedIndex((prevIndex) =>
        prevIndex > 0 ? prevIndex - 1 : filteredOptions.length - 1
      );
    } else if (e.key === "Enter") {
      if (filteredOptions.length > 0) {
        const selectedOption = filteredOptions[selectedIndex];
        handleOptionSelect(selectedOption);
      }
    }
  };

  const handleOptionSelect = (option) => {
    onNavigate(option.book, option.chapter);
    setQuery(option.book + (option.chapter ? " " + option.chapter : ""));
    setFilteredOptions([]);
  };

  const handleOptionHover = (index) => {
    setSelectedIndex(index);
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (filteredOptions.length > 0) {
      const selectedOption = filteredOptions[selectedIndex];
      handleOptionSelect(selectedOption);
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
