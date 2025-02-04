import React, { useState } from 'react';

function SearchBar({ onSearch }) {
  const [query, setQuery] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    onSearch(query);
  };

  return (
    <form onSubmit={handleSubmit} style={{ marginTop: '10px' }}>
      <label>Task Finder:</label>
      <br />
      <input
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        style={{ width: '200px', marginRight: '10px' }}
      />
      <button type="submit">Find</button>
    </form>
  );
}

export default SearchBar;
