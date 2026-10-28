/**
 * ========================================================================================
 * AirIQ: Multi-City Airbnb Price Intelligence & Predictive Analytics Platform
 * COMPONENT: GeographicExplorer.jsx — Geospatial Map & Marker Clustering Module
 * ========================================================================================
 * Authors:       Aditya Raju Pidurkar (Roll No. 40), Nidhi Singh (Roll No. 15)
 * Course:        Big Data Analytics (BDA) Laboratory Project
 * Institution:   Department of CSE, Ramdeobaba University (RBU), Nagpur
 * Faculty Guide: Dr. Preeti G. Khante
 *
 * KEY RESPONSIBILITIES:
 * 1. Big Data Geospatial Rendering: Connects to Apache Cassandra on port 9042 via FastAPI
 *    to retrieve WGS84 spatial listings (latitude, longitude, price, rating).
 * 2. Zero-Lag Marker Clustering: Solves DOM performance bottlenecks. Rendering thousands
 *    of individual SVG/HTML marker nodes causes browser stutter and memory lag.
 *    Using `MarkerClusterGroup` aggregates dense coordinates into clickable clusters.
 * 3. Land Boundary Precision: Displays geocoded properties strictly within municipal
 *    boundaries (zero underwater pins).
 * 4. Multi-Currency Pin Popups: Formats nightly prices in authentic native currency symbols.
 * ========================================================================================
 */

import React, { useEffect, useState } from 'react';
import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';
import MarkerClusterGroup from 'react-leaflet-cluster';
import { Filter } from 'lucide-react';

export default function GeographicExplorer() {
  // Current active city filter
  const [city, setCity] = useState('Mumbai');
  const [listings, setListings] = useState([]);
  const [loading, setLoading] = useState(false);

  // ------------------------------------------------------------------------------------
  // METROPOLITAN CENTROID COORDINATES: Center points for the 9 analyzed markets
  // ------------------------------------------------------------------------------------
  const cityCoordinates = {
    Mumbai: [19.0760, 72.8777],
    Bengaluru: [12.9716, 77.5946],
    Tokyo: [35.6762, 139.6503],
    London: [51.5074, -0.1278],
    Paris: [48.8566, 2.3522],
    Rome: [41.9028, 12.4964],
    Amsterdam: [52.3676, 4.9041],
    Sydney: [-33.8688, 151.2093],
    "New York City": [40.7128, -74.0060]
  };

  // ------------------------------------------------------------------------------------
  // DATA FETCHING: Retrieves spatial listings from Cassandra via FastAPI
  // ------------------------------------------------------------------------------------
  const fetchListings = async (targetCity) => {
    setLoading(true);
    try {
      // Calls FastAPI endpoint which queries Cassandra's partitioned listings_by_city table
      const res = await fetch(`http://127.0.0.1:8001/api/v1/listings?city=${encodeURIComponent(targetCity)}&limit=300`);
      const data = await res.json();
      if (data?.listings) {
        setListings(data.listings);
      }
    } catch (e) {
      console.error('Error fetching spatial listings:', e);
    } finally {
      setLoading(false);
    }
  };

  // Re-fetch listings whenever the user selects a new city
  useEffect(() => {
    fetchListings(city);
  }, [city]);

  return (
    <div className="space-y-6">
      {/* Module Header & City Selector */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between border-b border-slate-100 pb-4 gap-3">
        <div>
          <h2 className="text-xl font-bold text-slate-900">Geographic Explorer</h2>
          <p className="text-sm text-slate-500">
            Spatial distribution with local native pricing from Inside Airbnb, DoorstepAnalytics &amp; Apache Cassandra
          </p>
        </div>

        {/* City Filter Dropdown */}
        <div className="flex items-center space-x-2">
          <Filter className="w-4 h-4 text-slate-500" />
          <select
            value={city}
            onChange={(e) => setCity(e.target.value)}
            className="border border-slate-300 rounded-md px-3 py-1.5 text-xs font-semibold bg-white shadow-xs focus:ring-2 focus:ring-slate-900"
          >
            <option value="Mumbai">Mumbai (India) — INR (₹)</option>
            <option value="Bengaluru">Bengaluru (India) — INR (₹)</option>
            <option value="Tokyo">Tokyo (Japan) — JPY (¥)</option>
            <option value="London">London (United Kingdom) — GBP (£)</option>
            <option value="Paris">Paris (France) — EUR (€)</option>
            <option value="Rome">Rome (Italy) — EUR (€)</option>
            <option value="Amsterdam">Amsterdam (Netherlands) — EUR (€)</option>
            <option value="Sydney">Sydney (Australia) — AUD (A$)</option>
            <option value="New York City">New York City (USA) — USD ($)</option>
          </select>
          
          {/* Active pin counter */}
          <span className="text-xs bg-slate-100 px-2.5 py-1 rounded text-slate-700 font-mono flex items-center space-x-1">
            <span className="w-2 h-2 rounded-full bg-rose-500 mr-1"></span>
            <span>{listings.length} Clustered Pins</span>
          </span>
        </div>
      </div>

      {/* --------------------------------------------------------------------------------
          LEAFLET MAP CONTAINER WITH DYNAMIC MARKER CLUSTERING
          -------------------------------------------------------------------------------- */}
      <div className="w-full h-[540px] rounded-lg overflow-hidden border border-slate-200 shadow-xs relative">
        <MapContainer
          key={city}
          center={cityCoordinates[city] || [35.6762, 139.6503]}
          zoom={12}
          scrollWheelZoom={true}
          className="w-full h-full"
        >
          {/* Base OpenStreetMap Vector Tile Layer */}
          <TileLayer
            attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          />

          {/* MarkerClusterGroup: Prevents DOM lag by clustering nearby pins into numeric badges */}
          <MarkerClusterGroup
            chunkedLoading
            maxClusterRadius={45}
            spiderfyOnMaxZoom={true}
            showCoverageOnHover={false}
          >
            {listings.map((l) => (
              <Marker key={l.id} position={[l.latitude, l.longitude]}>
                {/* Popup displaying property info on pin click */}
                <Popup>
                  <div className="p-1 space-y-1 text-slate-800">
                    <h4 className="font-bold text-sm leading-tight text-slate-900">{l.name || "Airbnb Listing"}</h4>
                    <p className="text-xs text-slate-500 font-medium">{l.neighbourhood || l.city} • {l.room_type}</p>
                    <div className="flex justify-between items-center pt-1 border-t border-slate-100 text-xs">
                      {/* Price in authentic native currency */}
                      <span className="font-extrabold text-slate-900 text-sm font-mono">
                        {l.currency_symbol}{l.price.toLocaleString()} {l.currency}
                        <span className="font-normal text-slate-500 text-xs"> / night</span>
                      </span>
                      {/* Host review rating */}
                      <span className="bg-emerald-100 text-emerald-800 px-1.5 py-0.5 rounded font-mono font-semibold">★ {l.rating}</span>
                    </div>
                  </div>
                </Popup>
              </Marker>
            ))}
          </MarkerClusterGroup>
        </MapContainer>
      </div>
    </div>
  );
}
