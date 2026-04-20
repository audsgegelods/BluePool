import UserForm from "../components/UserForm"


function Register() {
    return (
     <div style={{ textAlign: 'center' }}>
            <UserForm route="/user/register/" method="register"/>
        </div>
    )
}

export default Register