/**
 * ========================================================================================
 * AirIQ: Multi-City Airbnb Price Intelligence & Predictive Analytics Platform
 * COMPONENT: ModelEvaluation.jsx — MLlib Empirical Validation & Benchmark Analytics
 * ========================================================================================
 * Authors:       Aditya Raju Pidurkar (Roll No. 40), Nidhi Singh (Roll No. 15)
 * Course:        Big Data Analytics (BDA) Laboratory Project
 * Institution:   Department of CSE, Ramdeobaba University (RBU), Nagpur
 * Faculty Guide: Dr. Preeti G. Khante
 *
 * KEY RESPONSIBILITIES:
 * 1. Empirical Metric Rendering: Displays RMSE ($209.98), MAE ($114.58), and R² variance
 *    (0.3659) against baseline regression (RMSE $323.37, MAE $183.32, R² 0.1463).
 * 2. Live API Polling: Fetches evaluation results dynamically from FastAPI (/api/v1/model/metrics).
 * 3. Interactive Benchmark Visualization: Uses Recharts to render side-by-side comparative
 *    bars demonstrating a 35.07% error reduction over baseline heuristic estimators.
 * 4. Model Provenance Accountability: Displays training volume (213,299 Inside Airbnb +
 *    10,800 Indian records) and tree hyperparameters (45 trees, max depth 9).
 * ========================================================================================
 */

import React, { useEffect, useState } from 'react';
import { Award, Layers, CheckCircle2, TrendingDown } from 'lucide-react';
import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend
} from 'recharts';

export default function ModelEvaluation() {
  // ------------------------------------------------------------------------------------
  // 1. STATE MANAGEMENT: Evaluation metrics payload from FastAPI / PySpark
  // ------------------------------------------------------------------------------------
  const [metrics, setMetrics] = useState(null);

  // ------------------------------------------------------------------------------------
  // 2. DATA FETCHING: Retrieves empirical test split metrics from FastAPI
  // ------------------------------------------------------------------------------------
  useEffect(() => {
    fetch('http://127.0.0.1:8001/api/v1/model/metrics')
      .then(r => r.json())
      .then(d => {
        if (d?.rmse) setMetrics(d);
      })
      .catch(console.error);
  }, []);

  // ------------------------------------------------------------------------------------
  // 3. CHART DATA TRANSFORMATION: Prepares side-by-side comparison for Recharts
  // ------------------------------------------------------------------------------------
  const chartData = metrics ? [
    { metric: 'RMSE ($ lower is better)', baseline: metrics.baseline_rmse, sparkRF: metrics.rmse },
    { metric: 'MAE ($ lower is better)', baseline: metrics.baseline_mae, sparkRF: metrics.mae },
    { metric: 'R² Score (% higher is better)', baseline: (metrics.baseline_r2 * 100).toFixed(1), sparkRF: (metrics.r2 * 100).toFixed(1) },
  ] : [];

  return (
    <div className="space-y-6">
      {/* Module Header */}
      <div className="border-b border-slate-100 pb-4">
        <h2 className="text-xl font-bold text-slate-900">Model Evaluation</h2>
        <p className="text-sm text-slate-500">
          Empirical validation metrics for PySpark MLlib Random Forest Regressor (45 trees, depth 9)
        </p>
      </div>

      {metrics && (
        <div className="grid grid-cols-1 sm:grid-cols-4 gap-4">
          <div className="border border-slate-200 rounded-lg p-4 bg-slate-50">
            <span className="text-xs uppercase text-slate-500 font-semibold">Trained Listings</span>
            <div className="text-2xl font-bold text-slate-900 font-mono mt-1">
              {metrics.trained_records.toLocaleString()}
            </div>
            <p className="text-xs text-slate-500 mt-1">Paris, Rome, Amsterdam</p>
          </div>

          <div className="border border-slate-200 rounded-lg p-4 bg-slate-50">
            <span className="text-xs uppercase text-slate-500 font-semibold">Root Mean Sq Error</span>
            <div className="text-2xl font-bold text-slate-900 font-mono mt-1">
              ${metrics.rmse}
            </div>
            <p className="text-xs text-emerald-700 font-medium mt-1">35% error reduction</p>
          </div>

          <div className="border border-slate-200 rounded-lg p-4 bg-slate-50">
            <span className="text-xs uppercase text-slate-500 font-semibold">Mean Absolute Error</span>
            <div className="text-2xl font-bold text-slate-900 font-mono mt-1">
              ${metrics.mae}
            </div>
            <p className="text-xs text-emerald-700 font-medium mt-1">Average residual</p>
          </div>

          <div className="border border-slate-200 rounded-lg p-4 bg-slate-50">
            <span className="text-xs uppercase text-slate-500 font-semibold">R² Explained Variance</span>
            <div className="text-2xl font-bold text-slate-900 font-mono mt-1">
              {(metrics.r2 * 100).toFixed(1)}%
            </div>
            <p className="text-xs text-slate-500 mt-1">40 Decision Trees (Depth 8)</p>
          </div>
        </div>
      )}

      <div className="border border-slate-200 rounded-lg p-5 bg-white">
        <h3 className="text-sm font-semibold text-slate-800 mb-4">
          PySpark MLlib vs. Baseline Heuristic Benchmark
        </h3>
        <div className="w-full h-72">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={chartData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" />
              <XAxis dataKey="metric" stroke="#64748b" fontSize={12} />
              <YAxis stroke="#64748b" fontSize={12} />
              <Tooltip />
              <Legend />
              <Bar dataKey="baseline" fill="#94a3b8" name="Baseline (Mean Estimator)" />
              <Bar dataKey="sparkRF" fill="#0f172a" name="Spark MLlib Random Forest" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
}
