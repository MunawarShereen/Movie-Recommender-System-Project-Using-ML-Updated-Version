import React from 'react';
import './MovieCard.css';

export default function MovieCard({ movie, onClick, isRecommendation }) {
  // If we have a poster, show it. Otherwise show a sleek title card.
  return (
    <div className="movie-card" onClick={() => onClick(movie)}>
      {movie.poster ? (
        <img src={movie.poster} alt={movie.title} className="movie-poster" />
      ) : (
        <div className="movie-poster-placeholder">
          <span className="movie-title-large">{movie.title}</span>
        </div>
      )}
      
      <div className="movie-info">
        <h3 className="movie-title">{movie.title}</h3>
        {!isRecommendation && (
          <span className="movie-action">Get Recommendations</span>
        )}
      </div>
    </div>
  );
}
