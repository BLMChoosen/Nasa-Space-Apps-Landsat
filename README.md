# Landsat Satellite Tracker

## Overview

A real-time satellite tracking and imagery visualization system designed for NASA's Landsat program. This application allows users to track Landsat 8 and Landsat 9 satellites, predict when they pass over specific locations, and retrieve satellite imagery filtered by cloud coverage thresholds.

The system combines interactive mapping with orbital mechanics calculations and cloud coverage analysis to help researchers, environmental scientists, and space enthusiasts identify optimal times for satellite observation.

## Why This Project Exists

Satellite imagery is invaluable for environmental monitoring, urban planning, and disaster response. However, finding usable imagery requires knowing:
- When a satellite will pass over your location of interest
- Whether cloud cover will obscure the view
- How to access and visualize the data efficiently

This project started as a NASA Space Apps Challenge submission and evolved into a functional tool for satellite tracking and image acquisition. It addresses the real-world problem of coordinating satellite overpasses with acceptable weather conditions.

## Tech Stack

**Backend:**
- Python 3.x
- Flask (web framework)
- Folium (interactive mapping)
- GeoPy (geospatial calculations)

**Frontend:**
- Leaflet.js (map interface)
- jQuery
- HTML5/CSS3

**APIs & Services:**
- N2YO Satellite Tracking API
- NASA GIBS (Global Imagery Browse Services)
- Meteomatics Weather API
- OWSLib (WMS client)

**Additional Libraries:**
- Matplotlib (visualization)
- Scikit-image (image processing)
- Cartopy (cartographic projections)
- NumPy (numerical computation)

## Features

- **Interactive Location Selection**: Click on a map to define target coordinates or manually input latitude/longitude
- **Real-time Satellite Tracking**: Visualizes current positions and orbital paths of Landsat 8 and Landsat 9
- **Overpass Prediction**: Calculates when satellites will pass within viewing range (±92.5 km) of target location
- **Cloud Coverage Filtering**: Queries weather data to filter observations by cloud cover percentage
- **Automatic Map Updates**: Refreshes satellite positions every 14 seconds
- **Satellite Imagery Retrieval**: Downloads Landsat imagery for specific dates and locations via NASA GIBS
- **Average Color Analysis**: Calculates mean RGB values from retrieved images

## Architecture

The application uses a multi-component architecture:

1. **Location Definition Module** (`Mapa define local.py`): Flask server that handles user location input via an interactive Leaflet map. Stores coordinates to local files for processing.

2. **Orbital Tracking Module** (`Mapa calcula órbita.py`): Fetches satellite position data from N2YO API, calculates complete orbital paths (~99 minutes), and generates real-time visualization using Folium. Implements threading for continuous updates.

3. **Cloud Coverage Module** (`octas_nuvens.py`): Queries Meteomatics API to retrieve cloud cover data measured in octas (1 octa = 12.5% coverage). Filters locations based on configurable thresholds.

4. **Imagery Acquisition Module** (`apinasa.py`): Connects to NASA GIBS WMS service to retrieve Landsat imagery for specific coordinates and dates. Processes images using Cartopy projections and calculates statistical color data.

The system follows an event-driven model where user input triggers coordinate storage, orbital calculations determine satellite proximity, and cloud data filters observation windows.

## Getting Started

### Prerequisites

```bash
pip install flask folium geopy requests owslib matplotlib scikit-image cartopy numpy
```

### API Keys Required

1. **N2YO API**: Register at [n2yo.com](https://www.n2yo.com/api/) for satellite tracking
2. **Meteomatics API**: Sign up at [meteomatics.com](https://www.meteomatics.com/) for weather data

### Configuration

Update API credentials in the respective files:
- `Mapa calcula órbita.py`: Replace `YOUR_API_KEY` with your N2YO key
- `octas_nuvens.py`: Update authentication credentials (currently hardcoded)

### Running the Application

**Option 1: Location Selection Interface**
```bash
python "Mapa define local.py"
```
Access at `http://localhost:5000` to select target coordinates.

**Option 2: Satellite Tracking Interface**
```bash
python "Mapa calcula órbita.py"
```
View real-time satellite positions and orbital paths at `http://localhost:5000`.

**Option 3: Retrieve Satellite Imagery**
```bash
python apinasa.py
```
Generates `landsat_image.png` for the coordinates stored in `latitude.txt` and `longitude.txt`.

## Example Usage

1. Launch the location selection interface
2. Click on the map to mark your target location (e.g., a forest area for deforestation monitoring)
3. Confirm the coordinates
4. Run the orbital tracking module to see when Landsat will pass overhead
5. Check cloud coverage using the weather API
6. If conditions are favorable, retrieve historical or near-real-time imagery

## Performance & Engineering Highlights

- **Orbital Path Calculation**: Computes ~99-minute Landsat orbits using 5,940 seconds of position data
- **Coverage Area Detection**: Uses geodesic distance calculations with a 92.5 km radius to match Landsat's 185×180 km imaging swath
- **Automatic Updates**: Thread-based architecture updates satellite positions every 14 seconds without blocking the main application
- **Invalid Coordinate Filtering**: Validates latitude (-90° to 90°) and longitude (-180° to 180°) to prevent rendering errors
- **Multi-satellite Support**: Simultaneously tracks both Landsat 8 and 9 with distinct visual representations

## What I Learned

- **Orbital Mechanics**: Understanding satellite ground tracks, revisit times, and Earth observation patterns
- **Geospatial APIs**: Working with WMS protocols and NASA's geospatial infrastructure
- **Asynchronous Python**: Implementing background threads for real-time data updates in Flask
- **Coordinate Systems**: Managing different projection systems (EPSG:4326) for map visualization
- **API Integration**: Coordinating multiple third-party services with different authentication and data formats

## Future Improvements

- Add database persistence instead of flat file storage
- Implement user authentication and location history
- Support additional satellite constellations (Sentinel-2, MODIS)
- Create notification system for upcoming favorable passes
- Add time-lapse generation from historical imagery
- Implement client-side caching to reduce API calls
- Develop mobile-responsive interface
- Add export functionality for orbital prediction data
