import React from 'react';
import MovieCard from './MovieCard';
import './MovieGrid.css';

export default function MovieGrid({ movies, onMovieSelect, isRecommendation }) {
  if (!movies || movies.length === 0) {
    return (
      <div className="empty-state">
        <p>No movies found.</p>
      </div>
    );
  }

  return (
    <div className="movie-grid-container">
      {movies.map((movie, index) => (
        <div 
          key={movie.movie_id || index} 
          className="grid-item-animate"
          style={{ animationDelay: `${index * 0.05}s` }}
        >
          <MovieCard 
            movie={movie} 
            onClick={onMovieSelect} 
            isRecommendation={isRecommendation}
          />
        </div>
      ))}
    </div>
  );
}
