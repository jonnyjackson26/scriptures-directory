import React from "react";
import "./AutoCompleteOptions.css";

const AutocompleteOptions = ({ options, selectedIndex, onHover, onSelect }) => {
  return (
    <ul className="autocomplete-options">
      {options.map((option, index) => (
        <li
          key={option}
          className={`autocomplete-option ${
            index === selectedIndex ? "selected" : ""
          }`}
          onMouseEnter={() => onHover(index)}
          onClick={() => onSelect(option)}
        >
          {option}
        </li>
      ))}
    </ul>
  );
};

export default AutocompleteOptions;
