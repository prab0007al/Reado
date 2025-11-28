import React from 'react';
import './BookCard.css';

const BookCard = ({ book }) => {
  // Find dominant emotion
  const getEmotionalTone = () => {
    const emotions = {
      joy: book.joy || 0,
      surprise: book.surprise || 0,
      anger: book.anger || 0,
      fear: book.fear || 0,
      sadness: book.sadness || 0
    };
    
    const dominant = Object.entries(emotions).reduce((a, b) => 
      a[1] > b[1] ? a : b
    );
    
    return dominant[1] > 0 ? dominant[0] : null;
  };

  // Color mapping for emotions
  const emotionColors = {
    joy: '#FFD700',
    surprise: '#FF6B6B',
    anger: '#FF4444',
    fear: '#9370DB',
    sadness: '#4169E1'
  };

  const dominantEmotion = getEmotionalTone();

  return (
    <div className="book-card">
      <div className="book-image">
        <img 
          src={book.thumbnail} 
          alt={book.title}
          onError={(e) => {
            e.target.src = 'https://via.placeholder.com/128x192?text=No+Image';
          }}
        />
        {dominantEmotion && (
          <span 
            className="emotion-badge"
            style={{ backgroundColor: emotionColors[dominantEmotion] }}
          >
            {dominantEmotion}
          </span>
        )}
      </div>
      
      <div className="book-details">
        <h3 className="book-title">{book.title}</h3>
        <p className="book-author">{book.authors}</p>
        <p className="book-category">{book.category}</p>
        
        <div className="book-meta">
          <span className="rating">
            ⭐ {book.average_rating.toFixed(1)}
          </span>
          {book.published_year && (
            <span className="year">
              📅 {Math.floor(book.published_year)}
            </span>
          )}
          {book.num_pages && (
            <span className="pages">
              📖 {Math.floor(book.num_pages)} pages
            </span>
          )}
        </div>
        
        <p className="book-description">
          {book.description.length > 150 
            ? `${book.description.substring(0, 150)}...` 
            : book.description}
        </p>
      </div>
    </div>
  );
};

export default BookCard;
