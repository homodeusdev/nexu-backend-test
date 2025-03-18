import React, { useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import API from '../services/api';
import './ModelForm.css';

const ModelForm = () => {
  const { brandId } = useParams();
  const [name, setName] = useState('');
  const [averagePrice, setAveragePrice] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const payload = {
        name,
        average_price: parseFloat(averagePrice),
      };
      const response = await API.post(`/brands/${brandId}/models`, payload);
      if (response.status === 201) {
        navigate(`/brands/${brandId}/models`);
      }
    } catch (err) {
      setError(err.response?.data?.detail || 'Error al crear el modelo');
    }
  };

  return (
    <div className="model-form-container">
      <h2>Agregar Modelo a la Marca {brandId}</h2>
      <form onSubmit={handleSubmit} className="model-form">
        <label>
          Nombre del Modelo:
          <input
            type="text"
            value={name}
            onChange={(e) => setName(e.target.value)}
            placeholder="Ingrese el nombre del modelo"
            required
          />
        </label>

        <label>
          Precio Promedio:
          <input
            type="number"
            value={averagePrice}
            onChange={(e) => setAveragePrice(e.target.value)}
            placeholder="Ejemplo: 350000"
            required
          />
        </label>

        {error && <p className="error">{error}</p>}

        <button type="submit" className="btn btn-submit">Crear Modelo</button>
      </form>
    </div>
  );
};

export default ModelForm;
