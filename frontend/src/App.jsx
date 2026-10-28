import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Layout from './components/Layout';
import OverviewDashboard from './pages/OverviewDashboard';
import PricePrediction from './pages/PricePrediction';
import GeographicExplorer from './pages/GeographicExplorer';
import ModelEvaluation from './pages/ModelEvaluation';

export default function App() {
  return (
    <BrowserRouter>
      <Layout>
        <Routes>
          <Route path="/" element={<OverviewDashboard />} />
          <Route path="/predict" element={<PricePrediction />} />
          <Route path="/explorer" element={<GeographicExplorer />} />
          <Route path="/evaluation" element={<ModelEvaluation />} />
        </Routes>
      </Layout>
    </BrowserRouter>
  );
}
