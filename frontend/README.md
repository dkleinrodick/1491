# Frontend - Frontier GoWild Flight Finder

Modern React frontend for browsing and searching Frontier Airlines GoWild pass flights.

## Features

- **Clean UI**: Modern, responsive design with TailwindCSS
- **Flight Search**: Filter by origin, destination, and date
- **Real-time Updates**: Trigger new searches directly from the UI
- **GoWild Filtering**: Show only flights available with GoWild pass
- **Bulk Search**: Search all destinations from an origin
- **Mobile Responsive**: Works on all device sizes

## Tech Stack

- **React 18**: Modern React with hooks
- **Vite**: Fast build tool and dev server
- **TailwindCSS**: Utility-first CSS framework
- **Axios**: HTTP client for API calls
- **Lucide React**: Beautiful icon library
- **date-fns**: Modern date utility library

## Setup

### Prerequisites

- Node.js 18+ or Bun
- Backend API running on http://localhost:8000

### Installation

1. Install dependencies:

```bash
npm install
# or
bun install
```

2. Create environment file:

```bash
cp .env.example .env
```

Edit `.env` if your backend is on a different URL:
```env
VITE_API_URL=http://localhost:8000
```

## Running

### Development Server

```bash
npm run dev
# or
bun run dev
```

The app will be available at http://localhost:5173

### Build for Production

```bash
npm run build
# or
bun run build
```

This creates optimized files in the `dist/` directory.

### Preview Production Build

```bash
npm run preview
# or
bun run preview
```

## Usage

### Searching Cached Flights

1. Select filters (origin, destination, date)
2. Check "GoWild Only" to see only GoWild available flights
3. Click "Search Cached Flights"

### Triggering New Searches

If you don't see recent data:

1. Select **both** origin and destination
2. Click "Trigger New Search"
3. Wait 30-60 seconds
4. Click "Search Cached Flights" again

### Bulk Searching

To search all destinations from an airport:

1. Select an origin airport
2. Click "Bulk Search (All Destinations)"
3. Wait several minutes (this searches many routes)
4. Use filters to browse results

## Project Structure

```
frontend/
├── public/          # Static assets
├── src/
│   ├── App.jsx      # Main application component
│   ├── main.jsx     # Application entry point
│   └── index.css    # Global styles (Tailwind)
├── index.html       # HTML template
├── package.json     # Dependencies
├── vite.config.js   # Vite configuration
└── tailwind.config.js
```

## Customization

### Colors

Edit `tailwind.config.js` to change the color scheme:

```js
theme: {
  extend: {
    colors: {
      'frontier-green': '#00a862',  // Main green color
      'frontier-dark': '#003831',   // Dark header color
    }
  }
}
```

### API URL

If deploying to production, update the API URL in `.env`:

```env
VITE_API_URL=https://your-api-domain.com
```

## Components

### App Component

Main application with search form and flight list.

**State Management:**
- `flights`: Current flight results
- `loading`: Loading state
- `error`: Error messages
- `origin`, `destination`, `selectedDate`: Search filters
- `gowildOnly`: Filter toggle

**Functions:**
- `searchFlights()`: Search cached flights from API
- `triggerScrape()`: Trigger new flight search
- `triggerBulkScrape()`: Trigger bulk search
- `loadOrigins()`, `loadDestinations()`: Load filter options

### FlightCard Component

Displays individual flight information.

**Props:**
- `flight`: Flight object from API

**Displays:**
- Origin and destination
- Departure and arrival times
- GoWild availability badge
- Pricing information
- Number of stops
- Duration

## API Integration

The frontend connects to the FastAPI backend:

### Endpoints Used

```
GET  /api/flights         - Get flights with filters
GET  /api/origins         - Get available origins
GET  /api/destinations    - Get available destinations
GET  /api/stats           - Get database statistics
POST /api/scrape/search   - Trigger flight search
POST /api/scrape/bulk     - Trigger bulk scrape
```

### Example API Call

```javascript
const response = await axios.get(`${API_URL}/api/flights`, {
  params: {
    origin: 'DEN',
    destination: 'LAX',
    date: '2025-11-07',
    gowild_only: true,
    limit: 100
  }
})
```

## Deployment

### Vercel

```bash
npm run build
# Deploy dist/ folder to Vercel
```

Add environment variable in Vercel dashboard:
```
VITE_API_URL=https://your-api-domain.com
```

### Netlify

```bash
npm run build
# Deploy dist/ folder to Netlify
```

Add environment variable in Netlify dashboard.

### Static Hosting

Build and upload the `dist/` folder to any static host:

```bash
npm run build
# Upload dist/ to S3, GitHub Pages, etc.
```

## Troubleshooting

### CORS Errors

Make sure your backend allows the frontend origin in `backend/config.py`:

```python
allowed_origins = [
    "http://localhost:5173",
    "https://your-frontend-domain.com"
]
```

### API Not Found

Check that:
1. Backend is running on port 8000
2. `.env` file has correct API URL
3. Vite proxy is configured in `vite.config.js`

### Build Errors

Clear node_modules and reinstall:

```bash
rm -rf node_modules package-lock.json
npm install
```

## Future Enhancements

- [ ] Add date range picker
- [ ] Implement sorting options
- [ ] Add flight comparison feature
- [ ] Save favorite routes
- [ ] Export to calendar
- [ ] Price alerts
- [ ] Multi-city search
- [ ] Interactive map view
- [ ] Dark mode toggle
- [ ] Flight details modal with more info

## Contributing

1. Make changes to components in `src/`
2. Test with `npm run dev`
3. Build with `npm run build`
4. Ensure no console errors

## License

Educational use only. Not affiliated with Frontier Airlines.
