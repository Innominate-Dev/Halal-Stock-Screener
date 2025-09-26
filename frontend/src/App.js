import React, { useState, useEffect } from "react";
import axios from "axios";

const SCREENERS = [
  { id: "stocks", label: "Stocks Screener" },
  { id: "news", label: "News Screener" },
  { id: "etf", label: "ETF Screener" },
];

function App() {
  const [activeScreener, setActiveScreener] = useState("stocks");
  const [search, setSearch] = useState("");
  const [stockData, setStockData] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // Load all stocks on default or when reload
  useEffect(() => {
    if (activeScreener === "stocks") {
      fetchAllStocks();
    }
  }, [activeScreener]);

  const fetchAllStocks = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await axios.get(`/stocks-screener`);
      setStockData(response.data.halal);
    } catch (err) {
      setError("Failed to load stocks.");
    } finally {
      setLoading(false);
    }
  };

  const handleSearch = () => {
    // Optionally: filter locally or hit backend with search param
    if (!search) {
      fetchAllStocks();
      return;
    }
    const filtered = stockData.filter(stock =>
      stock.ticker.toLowerCase().includes(search.toLowerCase())
    );
    setStockData(filtered);
  };

  return (
    <div className="min-h-screen flex bg-background font-poppins text-textPrimary">
      {/* Sidebar */}
      <aside className="w-64 bg-white shadow-md p-6 flex flex-col">
        <h2 className="text-2xl font-bold mb-8 text-primary">Screeners</h2>
        {SCREENERS.map(({ id, label }) => (
          <button
            key={id}
            onClick={() => setActiveScreener(id)}
            className={`mb-4 text-left px-4 py-2 rounded-lg font-semibold transition
              ${activeScreener === id ? "bg-primary text-white" : "hover:bg-primary/20"}`}
          >
            {label}
          </button>
        ))}
      </aside>

      {/* Main content */}
      <main className="flex-1 p-8">
        {/* Search bar */}
        <div className="mb-6 flex">
          <input
            type="text"
            placeholder="Search ticker..."
            value={search}
            onChange={(e) => setSearch(e.target.value.toUpperCase())}
            className="flex-grow border border-gray-300 rounded-xl px-4 py-3 text-lg focus:outline-none focus:ring-2 focus:ring-primary"
          />
          <button
            onClick={handleSearch}
            disabled={!search}
            className="ml-4 bg-primary text-white px-6 py-3 rounded-xl font-semibold hover:bg-secondary transition disabled:opacity-50"
          >
            Search
          </button>
        </div>

        {activeScreener === "stocks" && (
          <>
            {loading && <p>Loading stocks...</p>}
            {error && <p className="text-red-600">{error}</p>}
            {!loading && !error && stockData.length > 0 && (
              <div className="overflow-x-auto">
                <table className="w-full text-left border-collapse">
                  <thead className="bg-primary text-white">
                    <tr>
                      <th className="py-3 px-4">Ticker</th>
                      <th className="py-3 px-4">Company Name</th>
                      <th className="py-3 px-4">Halal / Haraam</th>
                      <th className="py-3 px-4">Sector</th>
                      <th className="py-3 px-4">Price</th>
                      <th className="py-3 px-4">RVOL</th>
                      <th className="py-3 px-4">Volume</th>
                      <th className="py-3 px-4">Change</th>
                    </tr>
                  </thead>
                  <tbody>
                    {stockData.map((stock) => (
                      <tr key={stock.ticker} className="border-b border-gray-200 hover:bg-gray-50">
                        <td className="py-3 px-4 font-mono">{stock.ticker}</td>
                        <td className="py-3 px-4">{stock.companyName}</td>
                        <td className={`py-3 px-4 font-semibold ${
                          stock.status.toLowerCase().includes("haram") ? "text-red-600" :
                          stock.status.toLowerCase().includes("doubtful") ? "text-yellow-500" :
                          "text-green-600"
                        }`}>{stock.status}</td>
                        <td className="py-3 px-4">{stock.sector || "N/A"}</td>
                        <td className="py-3 px-4">{stock.price ? `$${stock.price.toFixed(2)}` : "N/A"}</td>
                        <td className="py-3 px-4">{stock.rvol || "N/A"}</td>
                        <td className="py-3 px-4">{stock.volume || "N/A"}</td>
                        <td className={`py-3 px-4 ${
                          stock.change > 0 ? "text-green-600" :
                          stock.change < 0 ? "text-red-600" :
                          ""
                        }`}>
                          {stock.change ? `${stock.change > 0 ? "+" : ""}${stock.change.toFixed(2)}%` : "N/A"}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}
            {!loading && !error && stockData.length === 0 && (
              <p>No stocks found.</p>
            )}
          </>
        )}

        {activeScreener !== "stocks" && (
          <div className="text-center text-gray-600 mt-20 text-xl">
            <p>{SCREENERS.find(s => s.id === activeScreener)?.label} coming soon!</p>
          </div>
        )}
      </main>
    </div>
  );
}

export default App;
