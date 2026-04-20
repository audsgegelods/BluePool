import { useState } from 'react' 
import api from '../api'

import Container from '@mui/material/Container' 
import Button from '@mui/material/Button' 
import TextField from '@mui/material/TextField' 
import Stack from '@mui/material/Stack' 
import Box from '@mui/material/Box' 

function RideForm({ route, onSuccess }) {
    const [pick_up_location, setPickUpLocation] = useState("") 
    const [drop_off_location, setDropOffLocation] = useState("") 
    const [pick_up_time, setPickUpTime] = useState("") 
    const [routeInfo, setRouteInfo] = useState("") 
    const [loading, setLoading] = useState(false) 

    const handleSubmit = async (e) => {
        setLoading(true) 
        e.preventDefault() 
        
        try {
            const formData = {
                pick_up_location,
                drop_off_location,
                pick_up_time,
                route: routeInfo
            } 
            await api.post(route, formData) 
            if (onSuccess) onSuccess() 
        } 
        catch (error) {
            alert(error)
            console.log(error)
            alert("Error: " + (error.response?.data?.detail || error.message)) 
        } 
        finally {
            setLoading(false) 
        }
    } 

    return (
        <Container maxWidth='sm' sx={{ paddingTop: '50px' }}>
            <Box sx={{
                borderRadius: '3',
                border: '3px solid #0a1a3a',
                background: '#0a1a3a',
                width: '100',
                height: '100',
                padding: "30px",
            }}>
                <form onSubmit={handleSubmit}>
                    <h1 style={{ color: "white", textAlign: "center" }}>Create a Ride</h1>
                    <Stack spacing={2}>
                        <TextField
                            fullWidth
                            name="pick_up_location"
                            label="Pick-up location"
                            value={pick_up_location}
                            onChange={(e) => setPickUpLocation(e.target.value)}
                            required
                            variant="outlined"
                            sx={{ bgcolor: "white", borderRadius: 1 }}
                        />
                        <TextField
                            fullWidth
                            name="drop_off_location"
                            label="Drop-off location"
                            value={drop_off_location}
                            onChange={(e) => setDropOffLocation(e.target.value)}
                            required
                            variant="outlined"
                            sx={{ bgcolor: "white", borderRadius: 1 }}
                        />
                        <TextField
                            fullWidth
                            type="datetime-local"
                            name="pick_up_time"
                            value={pick_up_time}
                            onChange={(e) => setPickUpTime(e.target.value)}
                            required
                            variant="outlined"
                            sx={{ bgcolor: "white", borderRadius: 1 }}

                        />
                        <TextField
                            fullWidth
                            name="route"
                            label="Route / additional info"
                            value={routeInfo}
                            onChange={(e) => setRouteInfo(e.target.value)}
                            multiline
                            rows={3}
                            variant="outlined"
                            sx={{ bgcolor: "white", borderRadius: 1 }}
                        />
                        <Button variant="contained" type="submit" disabled={loading}>
                            {loading ? "Processing..." : "Create Ride"}
                        </Button>
                    </Stack>
                </form>
            </Box>
        </Container>
    ) 
}

export default RideForm 