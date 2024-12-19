import React from "react";
import OptionRow from "../OptionRow/OptionRow";
import "./AutoCompleteOptions.css";


// Mapping of books to categories (Book of Mormon, New Testament, etc.)
const bookCategories = {
  "1 Nephi": "Book of Mormon",
  "2 Nephi": "Book of Mormon",
  "Alma": "Book of Mormon",
  "Matthew": "New Testament",
  "Mark": "New Testament",
  "Luke": "New Testament",
  "Genesis": "Old Testament",
  "Exodus": "Old Testament",
  "Psalms": "Old Testament",
  "Doctrine and Covenants": "Doctrine and Covenants",
  "Moses": "Pearl of Great Price",
  "Abraham": "Pearl of Great Price",
  // Continue for other books
};

const AutocompleteOptions = ({ options, selectedIndex, onHover, onSelect }) => {
  return (
    <ul className="autocomplete-options">
      {options.map((option, index) => {
        const category = bookCategories[option] || "Unknown Category"; // Default if category is not found
        return (
          <OptionRow
            key={option}
            option={option}
            isSelected={index === selectedIndex}
            onHover={onHover}
            onSelect={onSelect}
            index={index}
            category={category}
          />
        );
      })}
    </ul>
  );
};

export default AutocompleteOptions;
