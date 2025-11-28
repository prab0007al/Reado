import React from 'react';
import './LoadingSpinner.css';

const LoadingSpinner = () => {
  return (
    <div className="loading-container">
      <div className="spinner"></div>
      <p>Finding your perfect books...</p>
    </div>
  );
};

export default LoadingSpinner;
