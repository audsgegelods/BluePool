import UserForm from "../components/UserForm"

function Login() {
    return <UserForm route="/user/token/" method="login" />
}

export default Login