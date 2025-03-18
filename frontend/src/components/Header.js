import React from 'react';
import { Link } from 'react-router-dom';
import './Header.css';

function Header() {
  return (
    <header className="header">
      <h1>Nexu Frontend</h1>
      <nav>
        <ul className="nav-links">
          <li>
            <Link to="/">Marcas</Link>
          </li>
          <li>
            <Link to="/add-brand">Agregar Marca</Link>
          </li>
          <li>
            <Link to="/models/filter">Filtrar Modelos</Link>
          </li>
        </ul>
      </nav>
    </header>
  );
}

export default Header;