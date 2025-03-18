import React, { useState } from 'react';
import API from '../services/api';
import './FilteredModelList.css';

const FilteredModelList = () => {
  const [greater, setGreater] = useState('');
  const [lower, setLower] = useState('');
  const [models, setModels] = useState([]);
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      let url = '/models?';
      if (greater) url += `greater=${greater}&`;
      if (lower) url += `lower=${lower}`;

      const response = await API.get(url);
      setModels(response.data);
      setError('');
    } catch (err) {
      setError('Error al filtrar modelos');
      console.error('Error fetching filtered models:', err);
    }
  };

  return (
    <div className="filtered-model-list">
      <h2>Filtrar Modelos por Precio</h2>

      <form onSubmit={handleSubmit} className="filter-form">
        <label>
          Mayor a:
          <input
            type="number"
            value={greater}
            onChange={(e) => setGreater(e.target.value)}
            placeholder="Ej: 100000"
          />
        </label>

        <label>
          Menor a:
          <input
            type="number"
            value={lower}
            onChange={(e) => setLower(e.target.value)}
            placeholder="Ej: 500000"
          />
        </label>

        <button type="submit" className="btn">Filtrar</button>
      </form>

      {error && <p className="error">{error}</p>}

      {models.length > 0 ? (
        <ul className="model-list">
          {models.map((model) => (
            <li key={model.id} className="model-item">
              <span className="model-name">{model.name}</span>
              <span className="model-price">Precio: {model.average_price}</span>
            </li>
          ))}
        </ul>
      ) : (
        <p>No hay modelos que cumplan con el filtro.</p>
      )}
    </div>
  );
};

export default FilteredModelList;
