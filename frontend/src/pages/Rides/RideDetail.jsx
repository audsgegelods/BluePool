import { useEffect, useState } from 'react'
import { useParams, useNavigate, Link } from 'react-router-dom'
import api from '../../api'
import { ACCESS_TOKEN } from '../../constants'
import ChatBox from '../../components/ChatBox'


import Container from '@mui/material/Container'
import Button from '@mui/material/Button'
import Box from '@mui/material/Box'
import Stack from '@mui/material/Stack'
import CircularProgress from '@mui/material/CircularProgress'

const getUserIdFromToken = () => {
    const token = localStorage.getItem(ACCESS_TOKEN)
    if (!token) return null
    try {
        const payload = JSON.parse(atob(token.split('.')[1]))
        return payload.user_id ? parseInt(payload.user_id) : null
    } catch (e) {
        console.error('Failed to decode token', e)
        return null
    }
}

function RideDetail() {
    const { id } = useParams()
    const navigate = useNavigate()
    const [ride, setRide] = useState(null)
    const [loading, setLoading] = useState(true)
    const [error, setError] = useState(null)
    const [actionLoading, setActionLoading] = useState(false)

    const [messsages, setMessages] = useState([])
    const [messageForm, setMessageForm] = useState(null)

    const currentUserId = getUserIdFromToken()

    useEffect(() => {
        fetchRide()
    }, [id])

    const fetchRide = async () => {
        setLoading(true)
        setError(null)
        try {
            const res = await api.get(`/rideposting/api/ride/${id}/`)
            setRide(res.data)
        } catch (err) {
            console.error(err)
            setError('Failed to load ride details.')
        } finally {
            setLoading(false)
        }
    }


    const handleJoin = async () => {
        setActionLoading(true)
        try {
            await api.post(`/rideposting/api/ride/${id}/join/`)
            await fetchRide()
        } catch (err) {
            alert(err.response?.data?.error || 'Failed to join ride')
        } finally {
            setActionLoading(false)
        }
    }

    const handleRequestAction = async (requestId, action) => {
        setActionLoading(true)
        try {
            await api.post('/rideposting/api/handle-request/', {
                request_id: requestId,
                action: action
            })
            await fetchRide()
        } catch (err) {
            alert(err.response?.data?.error || 'Action failed')
        } finally {
            setActionLoading(false)
        }
    }



    if (loading) {
        return (
            <Container sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '80vh' }}>
                <CircularProgress />
            </Container>
        )
    }

    if (error || !ride) {
        return (
            <Container sx={{ textAlign: 'center', py: 5 }}>
                <p style={{ color: 'red' }}>{error || 'Ride not found'}</p>
                <Button component={Link} to="/rides" sx={{ mt: 2 }}>
                    Back to Rides
                </Button>
            </Container>
        )
    }

    const isDriver = ride.driver?.id === currentUserId
    const userRequest = ride.requests?.find(r => r.passenger?.id === currentUserId)
    const pendingRequests = ride.requests?.filter(r => r.status === 'pending') || []
    const acceptedPassengers = ride.accepted_passengers || []

    const GOOGLE_API_KEY = import.meta.env.VITE_GOOGLE_API_KEY || ''
    const mapsEmbedUrl = GOOGLE_API_KEY
        ? `https://www.google.com/maps/embed/v1/directions?key=${GOOGLE_API_KEY}&origin=${encodeURIComponent(ride.pick_up_location)}&destination=${encodeURIComponent(ride.drop_off_location)}&mode=driving`
        : ''

    return (
        <Container maxWidth="md" sx={{ paddingTop: '50px', paddingBottom: '50px' }}>
            <Box sx={{
                borderRadius: '3',
                border: '3px solid #0a1a3a',
                background: '#0a1a3a',
                padding: '30px',
            }}>
                <h1 style={{ color: 'white', textAlign: 'center', marginBottom: '20px' }}>
                    Ride Information
                </h1>

                <div style={{ backgroundColor: '#1a2a4a', color: 'white', padding: '16px', borderRadius: '4px', marginBottom: '24px' }}>
                    <h3 style={{ marginTop: 0, marginBottom: '8px' }}>
                        {ride.pick_up_location} → {ride.drop_off_location}
                    </h3>
                    <hr style={{ backgroundColor: 'rgba(255,255,255,0.2)', margin: '12px 0' }} />
                    <p><strong>Pickup Time:</strong> {new Date(ride.pick_up_time).toLocaleString()}</p>
                    <p><strong>Pickup Location:</strong> {ride.pick_up_location}</p>
                    <p><strong>Dropoff Location:</strong> {ride.drop_off_location}</p>
                    <p><strong>Route info:</strong> {ride.route || 'Not specified'}</p>
                </div>

                {/* Google Maps */}
                {GOOGLE_API_KEY && (
                    <div style={{ marginBottom: '24px', textAlign: 'center' }}>
                        <iframe
                            title="directions"
                            width="100%"
                            height="450"
                            style={{ border: 0, borderRadius: '4px' }}
                            loading="lazy"
                            allowFullScreen
                            referrerPolicy="no-referrer-when-downgrade"
                            src={mapsEmbedUrl}
                        />
                    </div>
                )}

                {/* passenger  */}
                {!isDriver && (
                    <div style={{ marginBottom: '24px' }}>
                        {!userRequest && (
                            <Button
                                variant="contained"
                                color="success"
                                fullWidth
                                onClick={handleJoin}
                                disabled={actionLoading}
                            >
                                {actionLoading ? 'Processing...' : 'Request to Join'}
                            </Button>
                        )}
                        {userRequest && userRequest.status === 'pending' && (
                            <div style={{ backgroundColor: '#ed6c02', color: 'white', padding: '12px', borderRadius: '4px', textAlign: 'center' }}>
                                Your request is pending approval
                            </div>
                        )}
                        {userRequest && userRequest.status === 'accepted' && (
                            <div style={{ backgroundColor: '#2e7d32', color: 'white', padding: '12px', borderRadius: '4px', textAlign: 'center' }}>
                                You have been accepted to this ride!
                            </div>
                        )}
                        {userRequest && userRequest.status === 'rejected' && (
                            <div style={{ backgroundColor: '#d32f2f', color: 'white', padding: '12px', borderRadius: '4px', textAlign: 'center' }}>
                                Your request was rejected.
                            </div>
                        )}
                    </div>
                )}

                {/* driver */}
                {isDriver && (
                    <>
                        <h2 style={{ color: 'white', marginTop: '16px', marginBottom: '8px' }}>
                            Pending Requests ({pendingRequests.length})
                        </h2>
                        {pendingRequests.length === 0 ? (
                            <p style={{ color: 'gray', marginBottom: '16px' }}>No pending requests.</p>
                        ) : (
                            <Stack spacing={2} sx={{ mb: 3 }}>
                                {pendingRequests.map((req) => (
                                    <div key={req.id} style={{ backgroundColor: '#2a3a5a', padding: '12px', borderRadius: '4px', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                                        <span style={{ color: 'white' }}>{req.passenger?.username} wants to join</span>
                                        <div style={{ display: 'flex', gap: '8px' }}>
                                            <Button
                                                size="small"
                                                variant="contained"
                                                color="success"
                                                onClick={() => handleRequestAction(req.id, 'accept')}
                                                disabled={actionLoading}
                                            >
                                                Accept
                                            </Button>
                                            <Button
                                                size="small"
                                                variant="contained"
                                                color="error"
                                                onClick={() => handleRequestAction(req.id, 'reject')}
                                                disabled={actionLoading}
                                            >
                                                Reject
                                            </Button>
                                        </div>
                                    </div>
                                ))}
                            </Stack>
                        )}

                        <h2 style={{ color: 'white', marginBottom: '8px' }}>
                            Passengers on board
                        </h2>
                        {acceptedPassengers.length === 0 ? (
                            <p style={{ color: 'gray', marginBottom: '16px' }}>No passengers yet.</p>
                        ) : (
                            <div style={{ display: 'flex', flexWrap: 'wrap', gap: '8px', marginBottom: '16px' }}>
                                {acceptedPassengers.map((p) => (
                                    <span key={p.id} style={{ backgroundColor: '#0288d1', color: 'white', padding: '6px 12px', borderRadius: '16px', fontSize: '0.875rem' }}>
                                        {p.username}
                                    </span>
                                ))}
                            </div>
                        )}
                    </>
                )}
                
                {/* chat */}
                <ChatBox rideId={ride.id} currentUserId={currentUserId} />

                <div style={{ marginTop: '24px', textAlign: 'center' }}>
                    <Button component={Link} to="/rides" variant="text" sx={{ color: 'white' }}>
                        ← Back to all rides
                    </Button>
                </div>

                <div>

                </div>
            </Box>
        </Container>
    )
}

export default RideDetail