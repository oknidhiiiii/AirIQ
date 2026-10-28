/**
 * ========================================================================================
 * AirIQ: Multi-City Airbnb Price Intelligence & Predictive Analytics Platform
 * COMPONENT: PricePrediction.jsx — Real-Time Predictive Pricing Interface
 * ========================================================================================
 * Authors:       Aditya Raju Pidurkar (Roll No. 40), Nidhi Singh (Roll No. 15)
 * Course:        Big Data Analytics (BDA) Laboratory Project
 * Institution:   Department of CSE, Ramdeobaba University (RBU), Nagpur
 * Faculty Guide: Dr. Preeti G. Khante
 *
 * KEY RESPONSIBILITIES:
 * 1. User Input Capturing: Collects 6 core property parameters (city, room_type, accommodates,
 *    bedrooms, bathrooms, review_scores_rating) corresponding to PySpark MLlib training features.
 * 2. Ultra-Fast REST Invocation: Dispatches an asynchronous POST request to FastAPI on port 8001.
 * 3. In-Memory ML Feedback (< 15ms): Receives predicted nightly price evaluated across 45
 *    in-memory PySpark decision trees with calibrated confidence intervals.
 * 4. Multi-Currency Visualization: Renders prices formatted in native symbols (₹ INR, ¥ JPY, £ GBP, € EUR).
 * ========================================================================================
 */

import React, { useState } from 'react';
import { TrendingUp, Sparkles, Calculator, Globe, Calendar, Clock, AlertCircle } from 'lucide-react';

export default function PricePrediction() {
  const todayStr = new Date().toISOString().split('T')[0];

  // ------------------------------------------------------------------------------------
  // 1. STATE MANAGEMENT: Form inputs corresponding to PySpark MLlib features + Calendar Date
  // ------------------------------------------------------------------------------------
  const [formData, setFormData] = useState({
    city: 'Mumbai',                // Maps to city_idx in PySpark StringIndexer
    room_type: 'Entire home/apt',   // Maps to room_idx in PySpark StringIndexer
    accommodates: 2,               // Continuous integer (1 to 16 guests)
    bedrooms: 1,                   // Continuous float (1.0 to 10.0)
    bathrooms: 1,                  // Continuous float (0.5 to 8.0)
    review_scores_rating: 4.8,     // Continuous float (1.0 to 5.0)
    check_in_date: todayStr        // ISO YYYY-MM-DD Date for dynamic seasonal/weekend prediction
  });

  // State to hold prediction result payload from FastAPI
  const [prediction, setPrediction] = useState(null);
  const [loading, setLoading] = useState(false);

  // Helper to set quick date scenarios (Today, Weekend, New Year, Summer)
  const setQuickDate = (type) => {
    const d = new Date();
    if (type === 'today') {
      setFormData({ ...formData, check_in_date: todayStr });
    } else if (type === 'weekend') {
      // Find upcoming Friday
      const day = d.getDay();
      const diff = (5 - day + 7) % 7 || 7;
      d.setDate(d.getDate() + diff);
      setFormData({ ...formData, check_in_date: d.toISOString().split('T')[0] });
    } else if (type === 'newyear') {
      setFormData({ ...formData, check_in_date: '2026-12-31' });
    } else if (type === 'summer') {
      setFormData({ ...formData, check_in_date: '2027-07-15' });
    }
  };

  // ------------------------------------------------------------------------------------
  // 2. SUBMIT HANDLER: Dispatches prediction request to FastAPI (/api/v1/predict)
  // ------------------------------------------------------------------------------------
  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      // Calls FastAPI microservice running on port 8001
      const res = await fetch('http://127.0.0.1:8001/api/v1/predict', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData)
      });
      const data = await res.json();
      setPrediction(data);
    } catch (err) {
      console.error('Error fetching prediction from backend:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      {/* Module Header */}
      <div className="border-b border-slate-100 pb-4">
        <h2 className="text-xl font-bold text-slate-900">Price Prediction</h2>
        <p className="text-sm text-slate-500">
          Inference module calibrated per local market currency using PySpark MLlib (224,098 listings across 9 global &amp; Indian markets)
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Form Container */}
        <div className="lg:col-span-2 bg-slate-50 border border-slate-200 rounded-lg p-6">
          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              
              {/* Feature 1: Destination City (StringIndexer: city -> city_idx) */}
              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1">Target Market</label>
                <select
                  value={formData.city}
                  onChange={(e) => setFormData({ ...formData, city: e.target.value })}
                  className="w-full border border-slate-300 rounded px-3 py-2 text-sm bg-white focus:ring-2 focus:ring-slate-900 font-medium"
                >
                  <option value="Mumbai">Mumbai (India) — INR (₹)</option>
                  <option value="Bengaluru">Bengaluru (India) — INR (₹)</option>
                  <option value="Tokyo">Tokyo (Japan) — JPY (¥)</option>
                  <option value="London">London (UK) — GBP (£)</option>
                  <option value="Paris">Paris (France) — EUR (€)</option>
                  <option value="Rome">Rome (Italy) — EUR (€)</option>
                  <option value="Amsterdam">Amsterdam (Netherlands) — EUR (€)</option>
                  <option value="Sydney">Sydney (Australia) — AUD (A$)</option>
                  <option value="New York City">New York City (USA) — USD ($)</option>
                </select>
              </div>

              {/* Feature 2: Privacy Room Type (StringIndexer: room_type -> room_idx) */}
              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1">Room Type</label>
                <select
                  value={formData.room_type}
                  onChange={(e) => setFormData({ ...formData, room_type: e.target.value })}
                  className="w-full border border-slate-300 rounded px-3 py-2 text-sm bg-white focus:ring-2 focus:ring-slate-900"
                >
                  <option value="Entire home/apt">Entire home/apt</option>
                  <option value="Private room">Private room</option>
                  <option value="Hotel room">Hotel room</option>
                  <option value="Shared room">Shared room</option>
                </select>
              </div>

              {/* Feature 3: Guest Capacity (Top Predictive Feature: 31.41% Importance) */}
              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1">Guest Capacity (Accommodates)</label>
                <input
                  type="number"
                  min="1"
                  max="16"
                  value={formData.accommodates}
                  onChange={(e) => setFormData({ ...formData, accommodates: parseInt(e.target.value) || 1 })}
                  className="w-full border border-slate-300 rounded px-3 py-2 text-sm bg-white"
                />
              </div>

              {/* Feature 4: Bedrooms Count (21.98% Importance) */}
              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1">Bedrooms</label>
                <input
                  type="number"
                  min="1"
                  max="10"
                  step="1"
                  value={formData.bedrooms}
                  onChange={(e) => setFormData({ ...formData, bedrooms: parseFloat(e.target.value) || 1.0 })}
                  className="w-full border border-slate-300 rounded px-3 py-2 text-sm bg-white"
                />
              </div>

              {/* Feature 5: Bathrooms Count (8.85% Importance) */}
              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1">Bathrooms</label>
                <input
                  type="number"
                  min="1"
                  max="8"
                  step="0.5"
                  value={formData.bathrooms}
                  onChange={(e) => setFormData({ ...formData, bathrooms: parseFloat(e.target.value) || 1.0 })}
                  className="w-full border border-slate-300 rounded px-3 py-2 text-sm bg-white"
                />
              </div>

              {/* Feature 6: Review Rating (3.88% Importance) */}
              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1">Review Rating (1.0 - 5.0)</label>
                <input
                  type="number"
                  min="1.0"
                  max="5.0"
                  step="0.1"
                  value={formData.review_scores_rating}
                  onChange={(e) => setFormData({ ...formData, review_scores_rating: parseFloat(e.target.value) || 4.5 })}
                  className="w-full border border-slate-300 rounded px-3 py-2 text-sm bg-white"
                />
              </div>

              {/* Feature 7: Check-in Date & Temporal Dynamic Pricing */}
              <div className="md:col-span-2 border-t border-slate-200 pt-3">
                <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-1 mb-1.5">
                  <label className="block text-xs font-semibold text-slate-700 flex items-center space-x-1">
                    <Calendar className="w-3.5 h-3.5 text-slate-500" />
                    <span>Check-in Date (Temporal &amp; Dynamic Calendar Pricing)</span>
                  </label>
                  <div className="flex flex-wrap gap-1 text-[11px]">
                    <button
                      type="button"
                      onClick={() => setQuickDate('today')}
                      className="px-2 py-0.5 rounded bg-slate-200 hover:bg-slate-300 text-slate-700 font-medium transition"
                    >
                      Today (Base)
                    </button>
                    <button
                      type="button"
                      onClick={() => setQuickDate('weekend')}
                      className="px-2 py-0.5 rounded bg-amber-100 hover:bg-amber-200 text-amber-800 font-medium transition"
                    >
                      Weekend (+18%)
                    </button>
                    <button
                      type="button"
                      onClick={() => setQuickDate('newyear')}
                      className="px-2 py-0.5 rounded bg-rose-100 hover:bg-rose-200 text-rose-800 font-medium transition"
                    >
                      New Year (+35%)
                    </button>
                    <button
                      type="button"
                      onClick={() => setQuickDate('summer')}
                      className="px-2 py-0.5 rounded bg-sky-100 hover:bg-sky-200 text-sky-800 font-medium transition"
                    >
                      Summer (+25%)
                    </button>
                  </div>
                </div>
                <input
                  type="date"
                  value={formData.check_in_date}
                  onChange={(e) => setFormData({ ...formData, check_in_date: e.target.value })}
                  className="w-full border border-slate-300 rounded px-3 py-2 text-sm bg-white font-mono"
                />
                <p className="text-[11px] text-slate-500 mt-1">
                  Evaluates date elasticity across 365-day calendar: weekend surges, seasonal tourism curves, and holiday peaks.
                </p>
              </div>
            </div>

            {/* Calculate Button */}
            <div className="pt-2">
              <button
                type="submit"
                disabled={loading}
                className="w-full sm:w-auto px-6 py-2.5 bg-slate-900 hover:bg-slate-800 text-white text-sm font-semibold rounded-md shadow-xs transition flex items-center justify-center space-x-2"
              >
                <Calculator className="w-4 h-4" />
                <span>{loading ? 'Evaluating Spark RF + Calendar Engine...' : 'Calculate Dynamic Nightly Price'}</span>
              </button>
            </div>
          </form>
        </div>

        {/* Prediction Output Card: Renders Dynamic Local Price + Temporal Breakdown */}
        <div className="border border-slate-200 rounded-lg p-6 bg-white flex flex-col justify-center items-center text-center">
          {prediction ? (
            <div className="space-y-4 w-full">
              {/* Dynamic Status Pill */}
              {prediction.temporal?.is_holiday ? (
                <span className="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-medium bg-rose-100 text-rose-800">
                  <Sparkles className="w-3.5 h-3.5 mr-1" />
                  {prediction.temporal.holiday_name} (+{prediction.temporal.holiday_premium_pct}%)
                </span>
              ) : prediction.temporal?.is_weekend ? (
                <span className="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-medium bg-amber-100 text-amber-800">
                  <Clock className="w-3.5 h-3.5 mr-1" />
                  Weekend Night Surge (+{prediction.temporal.weekend_premium_pct}%)
                </span>
              ) : (
                <span className="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-medium bg-emerald-100 text-emerald-800">
                  <Sparkles className="w-3.5 h-3.5 mr-1" />
                  {prediction.temporal?.season || 'Standard Calendar Rate'}
                </span>
              )}

              {/* Main Price Display */}
              <div>
                <span className="text-xs uppercase tracking-wider text-slate-500 font-semibold">Dynamic Nightly Rate</span>
                <div className="text-4xl font-extrabold text-slate-900 mt-1 font-mono">
                  {prediction.currency_symbol}{prediction.predicted_price.toLocaleString()}
                  <span className="text-sm font-semibold text-slate-600"> {prediction.currency} / night</span>
                </div>
              </div>

              {/* Detailed Breakdown Card */}
              <div className="border-t border-slate-100 pt-3 text-xs text-slate-600 space-y-1.5 text-left bg-slate-50 p-3 rounded">
                <div className="flex justify-between">
                  <span>Base Structural Price:</span>
                  <span className="font-semibold text-slate-800 font-mono">
                    {prediction.currency_symbol}{prediction.base_price?.toLocaleString() || prediction.predicted_price.toLocaleString()} {prediction.currency}
                  </span>
                </div>
                {prediction.temporal && (
                  <>
                    <div className="flex justify-between">
                      <span>Check-in Day:</span>
                      <span className="font-semibold text-slate-800">
                        {prediction.temporal.day_name} ({prediction.temporal.check_in_date})
                      </span>
                    </div>
                    <div className="flex justify-between">
                      <span>Date Demand Elasticity:</span>
                      <span className="font-bold text-slate-900 font-mono">
                        {prediction.temporal.multiplier}x
                        <span className="text-[11px] font-normal text-slate-500 ml-1">
                          ({prediction.temporal.multiplier > 1.0 ? `+${Math.round((prediction.temporal.multiplier - 1.0) * 100)}% surge` : `${Math.round((prediction.temporal.multiplier - 1.0) * 100)}% off`})
                        </span>
                      </span>
                    </div>
                  </>
                )}
                <div className="flex justify-between">
                  <span>Confidence Range:</span>
                  <span className="font-semibold text-slate-800 font-mono">
                    {prediction.currency_symbol}{prediction.confidence_interval.lower_bound.toLocaleString()} – {prediction.currency_symbol}{prediction.confidence_interval.upper_bound.toLocaleString()}
                  </span>
                </div>
                <div className="flex justify-between border-t border-slate-200/60 pt-1.5">
                  <span>Model Engine:</span>
                  <span className="font-semibold text-slate-800">PySpark MLlib + Calendar</span>
                </div>
              </div>
            </div>
          ) : (
            <div className="text-slate-400 space-y-2">
              <TrendingUp className="w-10 h-10 mx-auto stroke-1" />
              <p className="text-xs">Adjust accommodation attributes and check-in date to estimate fair dynamic pricing in the local currency.</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
