import React, { useState } from "react";
import "./App.css";
import { FiSearch } from "react-icons/fi";

function App() {
  const [query, setQuery] = useState("");
  const [answer, setAnswer] = useState("");
  const [loading, setLoading] = useState(false);
  const [err, setErr] = useState("");

  const handleSearch = async () => {
    const q = query.trim();
    if (!q) return;
    setLoading(true);
    setErr("");
    setAnswer("");

    try {
      const res = await fetch("http://127.0.0.1:8000/api/ask", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query: q })
      });
      if (!res.ok) throw new Error(await res.text());
      const data = await res.json();
      setAnswer(data.answer);
    } catch (e) {
      setErr(String(e));
    } finally {
      setLoading(false);
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === "Enter") handleSearch();
  };

  return (
    <div className="App">
      <div className="App-header">
        <h1 className="App-title">Amazon Web Scraper</h1>
        <div className="App-body">
          <h2 className="App-cta"><i>What are you looking for?</i></h2>

          <div className="search-box">
            <input
              type="text"
              placeholder="Ask me"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              onKeyDown={handleKeyDown}
            />
            <button onClick={handleSearch}><FiSearch /></button>
          </div>

          {loading && <p style={{marginTop: "1rem"}}>Thinking…</p>}
          {err && <p style={{marginTop: "1rem", color: "crimson"}}>{err}</p>}
          {answer && (
            <div style={{marginTop: "1.25rem", maxWidth: 800, textAlign: "left", whiteSpace: "pre-wrap"}}>
              {answer}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default App;
