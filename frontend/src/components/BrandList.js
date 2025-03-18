import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import API from '../services/api';
import './BrandList.css';

const BrandList = () => {
  const [brands, setBrands] = useState([]);

  useEffect(() => {
    API.get('/brands')
      .then(response => {
        setBrands(response.data);
      })
      .catch(error => {
        console.error('Error fetching brands:', error);
      });
  }, []);

  return (
    <div className="brand-list">
      <h2>Lista de Marcas</h2>
      <ul>
        {brands.map(brand => (
          <li key={brand.id} className="brand-item">
            <span className="brand-name">{brand.name}</span>
            <span className="brand-price">Promedio: {brand.average_price}</span>
            <Link to={`/brands/${brand.id}/models`} className="btn btn-view">
              Ver Modelos
            </Link>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default BrandList;
