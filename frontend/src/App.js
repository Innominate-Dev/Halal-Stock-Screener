import React, { useState } from "react";

function App() {
  const [ticker, setTicker] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const checkStock = async () => {
    setLoading(true);
    try {
      const res = await fetch(`http://127.0.0.1:8000/screen/${ticker}`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ ticker }),
      });

      const data = await res.json();
      setResult(data);
    } catch (error) {
      console.error("API error:", error);
      setResult({ error: "Something went wrong." });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-6 max-w-lg mx-auto">
      <h1 className="text-2xl font-bold mb-4">Halal Stock Screener</h1>

      <input
        type="text"
        value={ticker}
        onChange={(e) => setTicker(e.target.value)}
        placeholder="Enter stock ticker"
        className="border p-2 w-full mb-4"
      />

      <button
        onClick={checkStock}
        className="bg-blue-500 text-white px-4 py-2 rounded w-full"
        disabled={loading}
      >
        {loading ? "Checking..." : "Check"}
      </button>

      {result && !result.error && (
        <div className="mt-6 text-left border p-4 rounded bg-gray-50 shadow">
          <p><strong>Ticker:</strong> {result.ticker}</p>
          <p><strong>Compliance:</strong> {result.compliance}</p>
          <p><strong>Reason:</strong> {result.reason}</p>
          <p><strong>Industry:</strong> {result.industry}</p>
          <p><strong>Market Cap:</strong> {result.market_cap}</p>
          {/* Add any other fields here */}
        </div>
      )}

      {result?.error && (
        <p className="text-red-500 mt-4">{result.error}</p>
      )}
    </div>
  );
}

export default App;
