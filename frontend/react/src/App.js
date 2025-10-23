import React, { useEffect, useRef, useState } from "react";
import "./App.css";
import { FiSearch } from "react-icons/fi";

function App() {
  const [query, setQuery] = useState("");
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);
  const [err, setErr] = useState("");
  const bottomRef = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

  const handleSearch = async () => {
    const q = query.trim();
    if (!q || loading) return;

    const userMsg = { id: crypto.randomUUID(), role: "user", content: q };
    setMessages((m) => [...m, userMsg]);
    setQuery("");
    setErr("");
    setLoading(true);

    try {
      const res = await fetch("http://127.0.0.1:8000/api/ask", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query: q }),
      });
      if (!res.ok) throw new Error(await res.text());
      const data = await res.json();

      const botMsg = {
        id: crypto.randomUUID(),
        role: "assistant",
        content: (data.answer || "").trim(),
      };
      setMessages((m) => [...m, botMsg]);
    } catch (e) {
      setErr(String(e));
    } finally {
      setLoading(false);
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === "Enter") handleSearch();
  };

  const titleText = "Amazon Web Scraper";

  return (
    <div className="App">
      <div className="App-header">
        {/* Title: rainbow letters + fade */}
        <h1 className="App-title">
          {titleText.split("").map((ch, i) => (
            <span className="rletter" key={i}>
              {ch === " " ? "\u00A0" : ch}
            </span>
          ))}
        </h1>

        <h2 className="App-cta">
          <i>What are you looking for?</i>
        </h2>

        <div className="App-body">
        
          {/* Full-height chat shell */}
          <div className="chat-shell">
            <div className="chat-log">
              {messages.map((m) => (
                <div key={m.id} className={`msg ${m.role}`}>
                  <div className="bubble">{m.content}</div>
                </div>
              ))}

              {loading && (
                <div className="msg assistant">
                  <div className="bubble typing">
                    <span className="dot" />
                    <span className="dot" />
                    <span className="dot" />
                  </div>
                </div>
              )}

              <div ref={bottomRef} />
            </div>

            {/* Composer (Ask me input) */}
            <div className="composer">
              <div className="search-box">
                <input
                  type="text"
                  placeholder="Ask me"
                  value={query}
                  onChange={(e) => setQuery(e.target.value)}
                  onKeyDown={handleKeyDown}
                  disabled={loading}
                />
                <button
                  onClick={handleSearch}
                  disabled={loading || !query.trim()}
                >
                  <FiSearch />
                </button>
              </div>

              {err && <p className="error-text">{err}</p>}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;
