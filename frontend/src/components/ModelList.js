import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import API from '../services/api';
import './ModelList.css';

const ModelList = () => {
  const { brandId } = useParams();
  const [models, setModels] = useState([]);
  const [brandName, setBrandName] = useState('');

  useEffect(() => {
    API.get(`/brands/${brandId}/models`)
      .then(response => {
        setModels(response.data);
      })
      .catch(error => console.error('Error al obtener modelos:', error));

    API.get('/brands')
      .then(response => {
        const foundBrand = response.data.find(
          (brand) => brand.id === parseInt(brandId, 10)
        );
        if (foundBrand) {
          setBrandName(foundBrand.name);
        }
      })
      .catch(error => console.error('Error al obtener detalles de la marca:', error));
  }, [brandId]);

  return (
    <div className="model-list">
      <h2>Modelos de la Marca: {brandName || brandId}</h2>
      {models.length > 0 ? (
        <ul>
          {models.map((model) => (
            <li key={model.id} className="model-item">
              <span className="model-name">{model.name}</span>
              <span className="model-price">Precio Promedio: {model.average_price}</span>
            </li>
          ))}
        </ul>
      ) : (
        <p>No hay modelos disponibles para esta marca.</p>
      )}
      <Link to={`/brands/${brandId}/add-model`} className="btn btn-add">
        Agregar Modelo
      </Link>
    </div>
  );
};

export default ModelList;
