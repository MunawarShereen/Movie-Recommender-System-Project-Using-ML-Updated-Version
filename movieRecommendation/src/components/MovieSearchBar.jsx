import React from 'react';
import './MovieSearchBar.css';

export default function MovieSearchBar({ movies, searchQuery, setSearchQuery, onRecommend, loading }) {
  return (
    <div className="search-bar-container">
      <div className="input-wrapper">
        <input
          type="text"
          className="glass-input"
          placeholder="Search or select a movie..."
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          list="movie-datalist"
        />
        <datalist id="movie-datalist">
          {movies.map((movie) => (
            <option key={movie.movie_id} value={movie.title} />
          ))}
        </datalist>
        {searchQuery && (
          <button 
            className="clear-btn" 
            onClick={() => setSearchQuery('')}
            title="Clear search"
          >
            ✕
          </button>
        )}
      </div>
      <button 
        className="recommend-btn" 
        onClick={onRecommend}
        disabled={loading || !searchQuery}
      >
        {loading ? "Analyzing..." : "Recommend"}
      </button>
    </div>
  );
}
