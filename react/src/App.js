import logo from "./logo.svg";
import React, { useState } from "react";
import "./App.css";
import { FiSearch } from "react-icons/fi";

function App() {
  const [query, setQuery] = useState("");

  const handleSearch = () => {
    if (query.trim() === "") return;
    console.log("Searching for:", query);
  };

  const handleKeyDown = (e) => {
    if (e.key === "Enter") {
      handleSearch();
    }
  };

  return (
    <div className="App">
      <div className="App-header">
        <h1 className="App-title">Amazon Web Scraper</h1>
        <div className="App-body">
          <h2 className="App-cta">
            <i>What are you looking for?</i>
          </h2>

          <div className="search-box">
            <input
              type="text"
              placeholder="Ask me"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              onKeyDown={handleKeyDown}
            />
            <button onClick={handleSearch}>
              <FiSearch />
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;
