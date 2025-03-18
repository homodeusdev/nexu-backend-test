import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Header from './components/Header';
import BrandList from './components/BrandList';
import BrandForm from './components/BrandForm';
import ModelList from './components/ModelList';
import ModelForm from './components/ModelForm';
import FilteredModelList from './components/FilteredModelList';
import './App.css';

function App() {
  return (
    <Router>
      <div className="app-container">
        <Header />
        <main className="main-content">
          <Routes>
            <Route path="/" element={<BrandList />} />
            <Route path="/add-brand" element={<BrandForm />} />
            <Route path="/brands/:brandId/models" element={<ModelList />} />
            <Route path="/brands/:brandId/add-model" element={<ModelForm />} />
            <Route path="/models/filter" element={<FilteredModelList />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;
