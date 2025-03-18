import React, { useState } from 'react';
import API from '../services/api';
import { useNavigate } from 'react-router-dom';
import './BrandForm.css';

const BrandForm = () => {
  const [name, setName] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await API.post('/brands', { name });
      if (response.status === 201) {
        navigate('/');
      }
    } catch (err) {
      setError(err.response?.data?.detail || 'Error al crear la marca');
    }
  };

  return (
    <div className="brand-form-container">
      <h2>Agregar Nueva Marca</h2>
      <form onSubmit={handleSubmit} className="brand-form">
        <label>
          Nombre de la Marca:
          <input
            type="text"
            value={name}
            onChange={(e) => setName(e.target.value)}
            placeholder="Ingrese el nombre de la marca"
            required
          />
        </label>
        {error && <p className="error">{error}</p>}
        <button type="submit" className="btn">Crear Marca</button>
      </form>
    </div>
  );
};

export default BrandForm;
