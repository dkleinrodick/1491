import { useState, useEffect } from 'react'
import { Plane, Search, Calendar, MapPin, DollarSign, Clock, RefreshCw } from 'lucide-react'
import axios from 'axios'
import { format, addDays } from 'date-fns'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

function App() {
  const [flights, setFlights] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [stats, setStats] = useState(null)

  // Filters
  const [origin, setOrigin] = useState('')
  const [destination, setDestination] = useState('')
  const [selectedDate, setSelectedDate] = useState('today')
  const [gowildOnly, setGowildOnly] = useState(true)

  // Available options
  const [origins, setOrigins] = useState([])
  const [destinations, setDestinations] = useState([])

  // Load initial data
  useEffect(() => {
    loadStats()
    loadOrigins()
  }, [])

  // Load destinations when origin changes
  useEffect(() => {
    if (origin) {
      loadDestinations(origin)
    }
  }, [origin])

  const loadStats = async () => {
    try {
      const response = await axios.get(`${API_URL}/api/stats`)
      setStats(response.data)
    } catch (err) {
      console.error('Error loading stats:', err)
    }
  }

  const loadOrigins = async () => {
    try {
      const response = await axios.get(`${API_URL}/api/origins`)
      setOrigins(response.data)
    } catch (err) {
      console.error('Error loading origins:', err)
    }
  }

  const loadDestinations = async (originCode) => {
    try {
      const response = await axios.get(`${API_URL}/api/destinations`, {
        params: { origin: originCode }
      })
      setDestinations(response.data)
    } catch (err) {
      console.error('Error loading destinations:', err)
    }
  }

  const searchFlights = async () => {
    setLoading(true)
    setError(null)

    try {
      const params = {
        gowild_only: gowildOnly,
        limit: 100
      }

      if (origin) params.origin = origin
      if (destination) params.destination = destination

      // Calculate date
      if (selectedDate === 'today') {
        params.date = format(new Date(), 'yyyy-MM-dd')
      } else if (selectedDate === 'tomorrow') {
        params.date = format(addDays(new Date(), 1), 'yyyy-MM-dd')
      }

      const response = await axios.get(`${API_URL}/api/flights`, { params })
      setFlights(response.data)

      if (response.data.length === 0) {
        setError('No flights found. Try triggering a new search below.')
      }
    } catch (err) {
      setError('Failed to load flights. Please try again.')
      console.error('Error searching flights:', err)
    } finally {
      setLoading(false)
    }
  }

  const triggerScrape = async () => {
    if (!origin || !destination) {
      alert('Please select both origin and destination')
      return
    }

    setLoading(true)
    setError(null)

    try {
      const date = selectedDate === 'today'
        ? format(new Date(), 'yyyy-MM-dd')
        : format(addDays(new Date(), 1), 'yyyy-MM-dd')

      await axios.post(`${API_URL}/api/scrape/search`, null, {
        params: { origin, destination, date }
      })

      alert('Flight search triggered! Results will appear in 30-60 seconds.')

      // Refresh after delay
      setTimeout(() => {
        searchFlights()
      }, 10000)
    } catch (err) {
      setError('Failed to trigger search. Please try again.')
      console.error('Error triggering scrape:', err)
    } finally {
      setLoading(false)
    }
  }

  const triggerBulkScrape = async () => {
    if (!origin) {
      alert('Please select an origin airport')
      return
    }

    setLoading(true)

    try {
      await axios.post(`${API_URL}/api/scrape/bulk`, null, {
        params: { origin, days: 2 }
      })

      alert('Bulk search triggered! This may take several minutes. Check back soon.')
    } catch (err) {
      alert('Failed to trigger bulk search.')
      console.error('Error triggering bulk scrape:', err)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-green-50">
      {/* Header */}
      <header className="bg-frontier-dark text-white shadow-lg">
        <div className="container mx-auto px-4 py-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <Plane className="w-10 h-10" />
              <div>
                <h1 className="text-3xl font-bold">Frontier GoWild Finder</h1>
                <p className="text-green-200 text-sm">Find the best GoWild pass flights</p>
              </div>
            </div>
            {stats && (
              <div className="hidden md:flex space-x-6 text-sm">
                <div className="text-center">
                  <div className="text-2xl font-bold text-frontier-green">{stats.total_flights}</div>
                  <div className="text-gray-300">Total Flights</div>
                </div>
                <div className="text-center">
                  <div className="text-2xl font-bold text-frontier-green">{stats.gowild_available}</div>
                  <div className="text-gray-300">GoWild Available</div>
                </div>
              </div>
            )}
          </div>
        </div>
      </header>

      <main className="container mx-auto px-4 py-8">
        {/* Search Form */}
        <div className="bg-white rounded-lg shadow-xl p-6 mb-8">
          <h2 className="text-2xl font-bold mb-4 flex items-center">
            <Search className="w-6 h-6 mr-2 text-frontier-green" />
            Search Flights
          </h2>

          <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-4">
            {/* Origin */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                <MapPin className="w-4 h-4 inline mr-1" />
                Origin
              </label>
              <select
                value={origin}
                onChange={(e) => setOrigin(e.target.value)}
                className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-frontier-green focus:border-transparent"
              >
                <option value="">All Origins</option>
                {origins.map(o => (
                  <option key={o} value={o}>{o}</option>
                ))}
              </select>
            </div>

            {/* Destination */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                <MapPin className="w-4 h-4 inline mr-1" />
                Destination
              </label>
              <select
                value={destination}
                onChange={(e) => setDestination(e.target.value)}
                className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-frontier-green focus:border-transparent"
              >
                <option value="">All Destinations</option>
                {destinations.map(d => (
                  <option key={d} value={d}>{d}</option>
                ))}
              </select>
            </div>

            {/* Date */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                <Calendar className="w-4 h-4 inline mr-1" />
                Date
              </label>
              <select
                value={selectedDate}
                onChange={(e) => setSelectedDate(e.target.value)}
                className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-frontier-green focus:border-transparent"
              >
                <option value="today">Today</option>
                <option value="tomorrow">Tomorrow</option>
              </select>
            </div>

            {/* GoWild Only */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Filter
              </label>
              <label className="flex items-center space-x-2 mt-2">
                <input
                  type="checkbox"
                  checked={gowildOnly}
                  onChange={(e) => setGowildOnly(e.target.checked)}
                  className="w-5 h-5 text-frontier-green focus:ring-frontier-green rounded"
                />
                <span className="text-sm">GoWild Only</span>
              </label>
            </div>
          </div>

          <div className="flex flex-wrap gap-3">
            <button
              onClick={searchFlights}
              disabled={loading}
              className="bg-frontier-green text-white px-6 py-2 rounded-lg font-semibold hover:bg-green-600 disabled:opacity-50 disabled:cursor-not-allowed flex items-center"
            >
              <Search className="w-4 h-4 mr-2" />
              Search Cached Flights
            </button>

            <button
              onClick={triggerScrape}
              disabled={loading || !origin || !destination}
              className="bg-blue-600 text-white px-6 py-2 rounded-lg font-semibold hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed flex items-center"
            >
              <RefreshCw className="w-4 h-4 mr-2" />
              Trigger New Search
            </button>

            <button
              onClick={triggerBulkScrape}
              disabled={loading || !origin}
              className="bg-purple-600 text-white px-6 py-2 rounded-lg font-semibold hover:bg-purple-700 disabled:opacity-50 disabled:cursor-not-allowed flex items-center"
            >
              <RefreshCw className="w-4 h-4 mr-2" />
              Bulk Search (All Destinations)
            </button>
          </div>

          {error && (
            <div className="mt-4 p-4 bg-yellow-50 border-l-4 border-yellow-400 text-yellow-700">
              {error}
            </div>
          )}
        </div>

        {/* Loading State */}
        {loading && (
          <div className="text-center py-12">
            <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-frontier-green mx-auto"></div>
            <p className="mt-4 text-gray-600">Loading flights...</p>
          </div>
        )}

        {/* Flights List */}
        {!loading && flights.length > 0 && (
          <div>
            <h2 className="text-2xl font-bold mb-4">
              Found {flights.length} flight{flights.length !== 1 ? 's' : ''}
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {flights.map((flight) => (
                <FlightCard key={flight.id} flight={flight} />
              ))}
            </div>
          </div>
        )}

        {/* Empty State */}
        {!loading && flights.length === 0 && !error && (
          <div className="text-center py-12 bg-white rounded-lg shadow">
            <Plane className="w-16 h-16 text-gray-300 mx-auto mb-4" />
            <p className="text-gray-600 text-lg">No flights to display</p>
            <p className="text-gray-400 mt-2">Select filters and search to get started</p>
          </div>
        )}
      </main>

      {/* Footer */}
      <footer className="bg-frontier-dark text-white mt-12 py-6">
        <div className="container mx-auto px-4 text-center">
          <p className="text-sm text-gray-300">
            Built for educational purposes. Please respect Frontier Airlines' Terms of Service.
          </p>
          <p className="text-xs text-gray-400 mt-2">
            Not affiliated with Frontier Airlines
          </p>
        </div>
      </footer>
    </div>
  )
}

function FlightCard({ flight }) {
  return (
    <div className="bg-white rounded-lg shadow-lg p-6 hover:shadow-xl transition-shadow">
      {/* Header */}
      <div className="flex justify-between items-start mb-4">
        <div>
          <div className="flex items-center space-x-2">
            <MapPin className="w-4 h-4 text-gray-500" />
            <span className="text-2xl font-bold">{flight.origin}</span>
            <span className="text-gray-400">→</span>
            <span className="text-2xl font-bold">{flight.destination}</span>
          </div>
          <div className="text-sm text-gray-500 mt-1">
            Flight {flight.flight_number}
          </div>
        </div>

        {flight.is_gowild_available && (
          <span className="bg-frontier-green text-white text-xs font-semibold px-3 py-1 rounded-full">
            GoWild
          </span>
        )}
      </div>

      {/* Time Info */}
      <div className="space-y-2 mb-4">
        <div className="flex items-center text-sm">
          <Clock className="w-4 h-4 text-gray-400 mr-2" />
          <span className="text-gray-600">
            Departs: {flight.departure_date} at {flight.departure_time}
          </span>
        </div>
        <div className="flex items-center text-sm">
          <Clock className="w-4 h-4 text-gray-400 mr-2" />
          <span className="text-gray-600">
            Arrives: {flight.arrival_date} at {flight.arrival_time}
          </span>
        </div>
        {flight.duration && (
          <div className="text-sm text-gray-500">
            Duration: {flight.duration}
          </div>
        )}
        {flight.stops > 0 && (
          <div className="text-sm text-orange-600 font-medium">
            {flight.stops} stop{flight.stops > 1 ? 's' : ''}
          </div>
        )}
      </div>

      {/* Pricing */}
      <div className="border-t pt-4">
        {flight.is_gowild_available && flight.gowild_price && (
          <div className="flex items-center justify-between">
            <span className="text-gray-600">GoWild Price:</span>
            <span className="text-2xl font-bold text-frontier-green flex items-center">
              <DollarSign className="w-5 h-5" />
              {flight.gowild_price.toFixed(2)}
            </span>
          </div>
        )}
        {flight.regular_price && (
          <div className="flex items-center justify-between text-sm text-gray-500 mt-1">
            <span>Regular Price:</span>
            <span className="line-through">
              ${flight.regular_price.toFixed(2)}
            </span>
          </div>
        )}
      </div>
    </div>
  )
}

export default App
