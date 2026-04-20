import { useNavigate } from 'react-router-dom'
import RideForm from '../../components/RideForm'

function RideCreate() {
    const navigate = useNavigate()
    return (
        <div style={{ textAlign: 'center' }}>
            <RideForm
                route="/rideposting/api/ride/add/"
                onSuccess={() => navigate("/rides")}
            />
        </div>
    )
}

export default RideCreate