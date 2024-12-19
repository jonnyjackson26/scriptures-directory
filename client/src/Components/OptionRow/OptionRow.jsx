import React from "react";
import "./OptionRow.css";

const OptionRow = ({ option, isSelected, onHover, onSelect, index }) => {
  return (
    <li
      className={`autocomplete-option ${isSelected ? "selected" : ""}`}
      onMouseEnter={() => onHover(index)}
      onClick={() => onSelect(option)}
    >
      <div className="option-text">
        {option.book} {option.chapter && ` ${option.chapter}`}
      </div>
      <div className="option-category">
        {option.category}
      </div>
    </li>
  );
};
export default OptionRow;
