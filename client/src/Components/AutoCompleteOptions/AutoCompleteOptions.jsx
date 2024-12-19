import React from "react";
import OptionRow from "../OptionRow/OptionRow";
import "./AutoCompleteOptions.css";


const AutocompleteOptions = ({ options, selectedIndex, onHover, onSelect }) => {
  return (
    <ul className="autocomplete-options">
      {options.map((item, index) => (
        <OptionRow
          key={item.book}
          option={item.book}
          category={item.category} // Pass category along with book
          isSelected={index === selectedIndex}
          onHover={onHover}
          onSelect={onSelect}
          index={index}
        />
      ))}
    </ul>
  );
};

export default AutocompleteOptions;
