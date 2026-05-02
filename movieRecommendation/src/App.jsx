import { useState, useEffect } from 'react';
import axios from 'axios';
import MovieSearchBar from './components/MovieSearchBar';
import MovieGrid from './components/MovieGrid';
import './App.css'; 

const TMDB_API_KEY = "2202712fdba3ed542b48ee46424588ae"; 

function App() {
  const [allMovies, setAllMovies] = useState([]);
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedMovie, setSelectedMovie] = useState(null);
  const [recommendations, setRecommendations] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // 1. Fetch initial movie dictionary from backend
  useEffect(() => {
    axios.get('http://127.0.0.1:8000/movies')
      .then(res => setAllMovies(res.data))
      .catch(err => {
        console.error(err);
        setError("Failed to connect to the recommendation engine.");
      });
  }, []);

  // 2. Fetch TMDB Poster
  const getPosterUrl = async (id) => {
    try {
      const response = await axios.get(`https://api.themoviedb.org/3/movie/${id}?api_key=${TMDB_API_KEY}`);
      if (response.data.poster_path) {
        return `https://image.tmdb.org/t/p/w500/${response.data.poster_path}`;
      }
      return null;
    } catch (err) {
      console.error(`Failed to fetch poster for ${id}`);
      return null;
    }
  };

  // 3. Handle movie selection / Recommend button click
  const handleRecommendClick = async () => {
    if (loading || !searchQuery) return;
    
    // Find the actual movie object from the search string
    const movie = allMovies.find(m => m.title.toLowerCase() === searchQuery.toLowerCase());
    
    if (!movie) {
      setError("Please select a valid movie from the list.");
      return;
    }
    
    setSelectedMovie(movie);
    setLoading(true);
    setError(null);
    setRecommendations([]);

    try {
      const res = await axios.post(`http://127.0.0.1:8000/recommend`, { movie_title: movie.title });
      
      if (res.data.error) {
        setError(res.data.error);
        setLoading(false);
        return;
      }

      // Fetch posters for recommended movies
      const dataWithPosters = await Promise.all(
        res.data.recommendations.map(async (recMovie) => ({
          ...recMovie,
          poster: await getPosterUrl(recMovie.movie_id)
        }))
      );
      
      setRecommendations(dataWithPosters);
    } catch (err) {
      console.error(err);
      setError("Failed to fetch recommendations.");
    }
    
    setLoading(false);
  };

  const handleClearSelection = () => {
    setSelectedMovie(null);
    setRecommendations([]);
    setSearchQuery('');
  };

  return (
    <div className="app-container">
      <header className="app-header">
        <h1 className="cinematic-title">
          <span className="accent">AI</span> Movie Recommender
        </h1>
        <p className="subtitle">Discover your next favorite cinematic experience.</p>
      </header>

      <main className="main-content">
        {/* Dynamic Search Bar & Recommend Button */}
        <MovieSearchBar 
          movies={allMovies}
          searchQuery={searchQuery} 
          setSearchQuery={(query) => {
            setSearchQuery(query);
            // Hide previous recommendations if user starts searching for a new movie
            if (selectedMovie && query !== selectedMovie.title) {
               setSelectedMovie(null);
               setRecommendations([]);
            }
          }} 
          onRecommend={handleRecommendClick}
          loading={loading}
        />

        {/* Status Indicators */}
        {error && <div className="error-message">{error}</div>}
        {loading && <div className="loading-spinner">Analyzing User Vectors...</div>}

        {/* Section Header */}
        {!loading && !error && selectedMovie && recommendations.length > 0 && (
          <div className="section-header">
            <div className="recommendation-header">
              <h2>Because you selected <span>"{selectedMovie.title}"</span></h2>
              <button className="back-btn" onClick={handleClearSelection}>Clear</button>
            </div>
          </div>
        )}

        {/* Filtered Grid Rendering (Only shows recommendations now) */}
        {!loading && !error && recommendations.length > 0 && (
          <MovieGrid 
            movies={recommendations} 
            onMovieSelect={() => {}} 
            isRecommendation={true}
          />
        )}
      </main>
    </div>
  );
}

export default App;