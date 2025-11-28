import React, { useEffect, useState } from 'react';
import { getCategories, getTones } from '../../services/api';
import './FilterPanel.css';

const FilterPanel = ({ onFilterChange, currentFilters }) => {
  const [categories, setCategories] = useState([]);
  const [tones, setTones] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchFilters = async () => {
      try {
        const [cats, tos] = await Promise.all([
          getCategories(),
          getTones()
        ]);
        setCategories(['All', ...cats]);
        setTones(['All', ...tos]);
      } catch (error) {
        console.error('Error fetching filters:', error);
      } finally {
        setLoading(false);
      }
    };
    
    fetchFilters();
  }, []);

  const handleCategoryChange = (e) => {
    onFilterChange({
      ...currentFilters,
      category: e.target.value
    });
  };

  const handleToneChange = (e) => {
    onFilterChange({
      ...currentFilters,
      tone: e.target.value
    });
  };

  if (loading) {
    return <div className="filter-panel-loading">Loading filters...</div>;
  }

  return (
    <div className="filter-panel">
      <div className="filter-group">
        <label htmlFor="category">Category:</label>
        <select
          id="category"
          value={currentFilters.category}
          onChange={handleCategoryChange}
          className="filter-select"
        >
          {categories.map((cat) => (
            <option key={cat} value={cat}>
              {cat}
            </option>
          ))}
        </select>
      </div>

      <div className="filter-group">
        <label htmlFor="tone">Emotional Tone:</label>
        <select
          id="tone"
          value={currentFilters.tone}
          onChange={handleToneChange}
          className="filter-select"
        >
          {tones.map((tone) => (
            <option key={tone} value={tone}>
              {tone}
            </option>
          ))}
        </select>
      </div>
    </div>
  );
};

export default FilterPanel;
