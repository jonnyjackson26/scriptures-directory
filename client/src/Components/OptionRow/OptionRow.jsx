import React from "react";
import "./OptionRow.css";

const OptionRow = ({ option, isSelected, onHover, onSelect, index, category }) => {
  return (
    <li
      className={`autocomplete-option ${isSelected ? "selected" : ""}`}
      onMouseEnter={() => onHover(index)}
      onClick={() => onSelect(option)}
    >
      <div className="option-text">
        {option}
      </div>
      <div className="option-category">
        {category}
      </div>
    </li>
  );
};

export default OptionRow;
