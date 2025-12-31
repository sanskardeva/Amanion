import React, { useState } from "react";
import "./App.css";
import { FiSearch } from "react-icons/fi";

// A simple reusable Card component for displaying items
const ItemCard = ({ item }) => {
  return (
    <div className="card">
      <div className="card-image">
        {/* Placeholder image logic if none exists */}
        <img
          src={item.image || "https://via.placeholder.com/150"}
          alt={item.title}
        />
      </div>
      <div className="card-content">
        <h3
          className="card-title"
          title={item.title}
        >
          {item.title}
        </h3>
        <div className="card-details">
          <span className="card-price">${item.price}</span>
          <span className="card-rating">★ {item.rating}</span>
        </div>
        <a
          href={item.url}
          target="_blank"
          rel="noopener noreferrer"
          className="card-btn"
        >
          View on Amazon
        </a>
      </div>
    </div>
  );
};

function App() {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState([]); // State to store items
  const [loading, setLoading] = useState(false); // State for loading status

  const handleSearch = () => {
    if (query.trim() === "") return;

    setLoading(true);
    setResults([]); // Clear previous results

    console.log("Searching for:", query);

    // SIMULATION: Mocking a delay and data response
    setTimeout(() => {
      const mockData = [
        {
          id: 1,
          title: "Sony WH-1000XM5 Wireless Noise Canceling Headphones",
          price: "348.00",
          rating: "4.5",
          image: "https://m.media-amazon.com/images/I/51SKmu2G9FL._AC_SL1000_.jpg",
          url: "#",
        },
        {
          id: 2,
          title: "Apple AirPods Pro (2nd Generation)",
          price: "199.00",
          rating: "4.8",
          image: "https://m.media-amazon.com/images/I/61SUj2aKoEL._AC_SL1500_.jpg",
          url: "#",
        },
        {
          id: 3,
          title: "Bose QuietComfort 45 Bluetooth Wireless",
          price: "279.00",
          rating: "4.6",
          image: "https://m.media-amazon.com/images/I/51JbsHSktkL._AC_SL1500_.jpg",
          url: "#",
        },
        // Add more items to test grid layout...
      ];
      setResults(mockData);
      setLoading(false);
    }, 1500);
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
              placeholder="Ask me (e.g. Headphones)"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              onKeyDown={handleKeyDown}
            />
            <button
              onClick={handleSearch}
              disabled={loading}
            >
              <FiSearch />
            </button>
          </div>
        </div>
      </div>

      {/* Results Section */}
      <div className="results-container">
        {loading && <p className="loading-text">Scraping Amazon...</p>}

        {!loading && results.length > 0 && (
          <div className="cards-grid">
            {results.map((item) => (
              <ItemCard
                key={item.id}
                item={item}
              />
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
