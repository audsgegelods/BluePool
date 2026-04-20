import UserForm from '../components/UserForm'
import { Link } from 'react-router-dom'

function Login() {
    return (
        <div style={{ textAlign: 'center' }}>
            <UserForm route="/user/token/" method="login" />
            <Link to="/user/register/">Don't have an account? Register</Link>
        </div>
    )
}

export default Login