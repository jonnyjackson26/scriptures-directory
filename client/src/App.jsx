import React from "react";
import { BrowserRouter as Router, Routes, Route, useNavigate } from "react-router-dom";
import SearchBar from "./Components/SearchBar.jsx/SearchBar/SearchBar";
import { books } from "./assets/books";

function App() {
  const navigate = useNavigate();

  const handleNavigate = (book, chapter) => {
    // This is a mock navigation. You can replace it with actual routing logic.
    alert(`Navigating to: ${book} chapter ${chapter}`);
  };

  return (
    <div className="container">
      <h1>Scripture Search</h1>
      <SearchBar options={books} onNavigate={handleNavigate} />
    </div>
  );
}

export default function AppWrapper() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<App />} />
      </Routes>
    </Router>
  );
}
