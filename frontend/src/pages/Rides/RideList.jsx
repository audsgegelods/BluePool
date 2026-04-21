import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import api from '../../api'
import Container from '@mui/material/Container'
import Button from '@mui/material/Button'
import TextField from '@mui/material/TextField'
import Stack from '@mui/material/Stack'
import Box from '@mui/material/Box'

import NavBar from '../../components/NavBar'

function RideList() {
    const [rides, setRides] = useState([])
    const [loading, setLoading] = useState(false)
    const [filters, setFilters] = useState({
        pick_up_location: '',
        drop_off_location: ''
    })

    const fetchRides = async (filterParams = {}) => {
        setLoading(true)
        try {
            const params = new URLSearchParams()
            if (filterParams.pick_up_location) params.append('pick_up_location', filterParams.pick_up_location)
            if (filterParams.drop_off_location) params.append('drop_off_location', filterParams.drop_off_location)
            
            const url = `/rideposting/api/rides/${params.toString() ? `?${params}` : ''}`
            const response = await api.get(url)
            
            if (Array.isArray(response.data)) {
                setRides(response.data)
            } else {
                console.error('Expected array, got:', response.data)
                setRides([])
            }
        } catch (error) {
            console.error(error)
            alert("Error fetching rides: " + (error.response?.data?.detail || error.message))
        } finally {
            setLoading(false)
        }
    }

    useEffect(() => {
        fetchRides()
    }, [])

    const handleFilterChange = (e) => {
        setFilters({
            ...filters,
            [e.target.name]: e.target.value
        })
    }

    const handleFilterSubmit = (e) => {
        e.preventDefault()
        const activeFilters = {}
        if (filters.pick_up_location) activeFilters.pick_up_location = filters.pick_up_location
        if (filters.drop_off_location) activeFilters.drop_off_location = filters.drop_off_location
        fetchRides(activeFilters)
    }

    return (
        <>
        <NavBar></NavBar>
        <Container maxWidth="lg" sx={{ paddingTop: '50px' }}>
            <Box sx={{
                borderRadius: "3",
                border: '3px solid #0a1a3a',
                background: '#0a1a3a',
                padding: "30px",
            }}>
                <h1 style={{ color: "white", textAlign: "center" }}>Available Rides</h1>

                <form onSubmit={handleFilterSubmit}>
                    <Stack spacing={2} sx={{ mb: 4 }}>
                        <TextField
                            fullWidth
                            name="pick_up_location"
                            label="Pick-up location"
                            value={filters.pick_up_location}
                            onChange={handleFilterChange}
                            variant="outlined"
                            sx={{ bgcolor: "white", borderRadius: 1 }}
                        />
                        <TextField
                            fullWidth
                            name="drop_off_location"
                            label="Drop-off location"
                            value={filters.drop_off_location}
                            onChange={handleFilterChange}
                            variant="outlined"
                            sx={{ bgcolor: "white", borderRadius: 1 }}
                        />
                        <Button variant="contained" type="submit">
                            Filter
                        </Button>
                    </Stack>
                </form>

                {loading ? (
                    <p style={{ color: "white", textAlign: "center" }}>Loading rides...</p>
                ) : rides.length === 0 ? (
                    <p style={{ color: "white", textAlign: "center" }}>No rides found.</p>
                ) : (
                    <div style={{ display: 'flex', flexWrap: 'wrap', gap: '24px', justifyContent: 'flex-start' }}>
                        {rides.map((ride) => (
                            <div key={ride.id} style={{
                                flex: '1 1 300px',
                                maxWidth: 'calc(33% - 24px)',
                                backgroundColor: '#1a2a4a',
                                borderRadius: '4px',
                                display: 'flex',
                                flexDirection: 'column',
                                boxSizing: 'border-box'
                            }}>
                                <div style={{ padding: '16px', color: 'white' }}>
                                    <h3 style={{ marginTop: 0, marginBottom: '8px' }}>
                                        {ride.pick_up_location} → {ride.drop_off_location}
                                    </h3>
                                    <p style={{ margin: '4px 0', fontSize: '0.875rem', color: '#ccc' }}>
                                        Departure: {new Date(ride.pick_up_time).toLocaleString()}
                                    </p>
                                    <p style={{ margin: '4px 0', fontSize: '0.875rem', color: '#ccc' }}>
                                        Driver: {ride.driver?.username || "Unknown"}
                                    </p>
                                    <Button
                                        variant="outlined"
                                        size="small"
                                        component={Link}
                                        to={`/rides/${ride.id}`}
                                        fullWidth
                                        sx={{ color: 'white', borderColor: 'white' }}
                                    >
                                        View Details
                                    </Button>
                                </div>
                            </div>
                        ))}
                    </div>
                )}
            </Box>
        </Container>
        </>
    )
}

export default RideList