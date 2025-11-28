import React, { useState } from 'react';
import SearchBar from './components/SearchBar/SearchBar';
import FilterPanel from './components/FilterPanel/FilterPanel';
import BookCard from './components/BookCard/BookCard';
import LoadingSpinner from './components/LoadingSpinner/LoadingSpinner';
import { getRecommendations } from './services/api';
import './App.css';

function App() {
  // State management
  const [books, setBooks] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [searchQuery, setSearchQuery] = useState('');
  const [filters, setFilters] = useState({
    category: 'All',
    tone: 'All'
  });

  // Handle search submission
  const handleSearch = async (query) => {
    setLoading(true);
    setError(null);
    setSearchQuery(query);
    
    try {
      const data = await getRecommendations(
        query, 
        filters.category, 
        filters.tone
      );
      setBooks(data.books);
    } catch (err) {
      setError('Failed to fetch recommendations. Please try again.');
      console.error('Search error:', err);
    } finally {
      setLoading(false);
    }
  };

  // Handle filter changes
  const handleFilterChange = async (newFilters) => {
    setFilters(newFilters);
    
    // Re-search with new filters if there's an active search
    if (searchQuery) {
      setLoading(true);
      setError(null);
      
      try {
        const data = await getRecommendations(
          searchQuery, 
          newFilters.category, 
          newFilters.tone
        );
        setBooks(data.books);
      } catch (err) {
        setError('Failed to apply filters. Please try again.');
        console.error('Filter error:', err);
      } finally {
        setLoading(false);
      }
    }
  };

  return (
    <div className="app">
      {/* Header Section */}
      <header className="app-header">
        <h1>Reado</h1>
        <p>AI-Powered Book Recommendations</p>
      </header>

      {/* Main Content */}
      <main className="app-main">
        {/* Search and Filter Section */}
        <div className="search-section">
          <SearchBar onSearch={handleSearch} isLoading={loading} />
          <FilterPanel 
            onFilterChange={handleFilterChange}
            currentFilters={filters}
          />
        </div>

        {/* Error Message */}
        {error && (
          <div className="error-message">
            ⚠️ {error}
          </div>
        )}

        {/* Loading State */}
        {loading && <LoadingSpinner />}

        {/* Results Section */}
        {!loading && books.length > 0 && (
          <div className="results-section">
            <h2 className="results-title">
              Found {books.length} recommendations
            </h2>
            <div className="books-grid">
              {books.map((book) => (
                <BookCard key={book.isbn13} book={book} />
              ))}
            </div>
          </div>
        )}

        {/* No Results */}
        {!loading && !error && books.length === 0 && searchQuery && (
          <div className="no-results">
            <p>No books found. Try a different search query or filters.</p>
          </div>
        )}

        {/* Welcome Message */}
{!loading && !searchQuery && (
  <div className="welcome-message">
    <div className="welcome-icon">📚</div>
    <h2>Welcome to Reado!</h2>
    <p className="welcome-subtitle">
      Discover your next favorite book using AI-powered semantic search
    </p>
    
    <div className="features-grid">
      <div className="feature-card">
        <div className="feature-icon">🔍</div>
        <h4>Semantic Search</h4>
        <p>Describe what you're looking for in natural language</p>
      </div>
      <div className="feature-card">
        <div className="feature-icon">🎭</div>
        <h4>Emotion Detection</h4>
        <p>Find books matching your mood and emotional tone</p>
      </div>
      <div className="feature-card">
        <div className="feature-icon">⚡</div>
        <h4>Smart Filtering</h4>
        <p>Filter by category and emotional atmosphere</p>
      </div>
    </div>
    
    <div className="examples">
      <h3>✨ Try these example searches:</h3>
      <ul>
        <li onClick={() => handleSearch("A thrilling mystery with unexpected twists")}>
          <span className="example-icon">🔎</span>
          <span className="example-text">"A thrilling mystery with unexpected twists"</span>
        </li>
        <li onClick={() => handleSearch("Heartwarming story about friendship and growth")}>
          <span className="example-icon">💖</span>
          <span className="example-text">"Heartwarming story about friendship and growth"</span>
        </li>
        <li onClick={() => handleSearch("Epic fantasy adventure with magic")}>
          <span className="example-icon">🏰</span>
          <span className="example-text">"Epic fantasy adventure with magic"</span>
        </li>
        <li onClick={() => handleSearch("Science fiction exploring AI and consciousness")}>
          <span className="example-icon">🤖</span>
          <span className="example-text">"Science fiction exploring AI and consciousness"</span>
        </li>
      </ul>
    </div>
  </div>
)}

      </main>

      {/* Footer */}
      <footer className="app-footer">
        <p>Powered by semantic search and sentiment analysis</p>
      </footer>
    </div>
  );
}

export default App;
