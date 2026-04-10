import { useState } from "react"
import api from "../api"
import { UNSAFE_NavigationContext, useNavigate } from "react-router-dom"
import { ACCESS_TOKEN, REFRESH_TOKEN } from "../constants"
import "../styles/userForm.css"

import Container from "@mui/material/Container"
import Button from "@mui/material/Button"
import TextField from "@mui/material/TextField"
import Stack from "@mui/material/Stack"
import Box from "@mui/material/Box"

function UserForm({route, method}) {
    const [firstName, setFirstName] = useState("")
    const [lastName, setLastName] = useState("")
    const [username, setUsername] = useState("")
    const [email, setEmail] = useState("")
    const [password, setPassword] = useState("")
    const [loading, setLoading] = useState(false)
    const nav = useNavigate()

    const handleSubmit = async (e) => {
        setLoading(true);
        e.preventDefault();
        


        try {
            const form_input = 
                method === "login" ? {username, password} :
                    {
                        first_name: firstName,
                        last_name: lastName,
                        username,
                        email,
                        password
                    }
            const res = await api.post(route, form_input)
            
            if (method === "login") {
                console.log("burger")
                localStorage.setItem(ACCESS_TOKEN, res.data.access);
                localStorage.setItem(REFRESH_TOKEN, res.data.refresh);
                nav("/")
            }
            else {
                nav("/login")
            }
        }
        catch (error) {
            alert(error)
            console.log(error)
            alert("Error: " + error.response?.data?.detail || error.message)
        }
        finally {
            setLoading(false)
        }
    }

    return <Container maxWidth="sm"
                sx={{paddingTop:'50px'}}>
        <Box sx={{  borderRadius:"3",
                    border: '3px solid #0a1a3a',
                     background: '#0a1a3a',
                     width: '100',
                     height: '100',
                     padding: "30px",
                     }}> 
        <form onSubmit={handleSubmit} className="form-container">
        <h1 className="method-name"> {method === "login" ? "Login" : "Register"} </h1>
        {method === "login" && (
            <Stack spacing={2}>
                <TextField
                    id="outlinedBasic" 
                    className="form-input"
                    type="text"
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                    placeholder="Username"
                />
                <TextField
                    id="outinedBasic" 
                    className="form-input"
                    type="text"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    placeholder="Password"
                />
                <Button variant="contained" className="form-button" type="submit">
                    {method === "login" ? "Login" : "Register"}
                </Button>
            </Stack> )}
        {method === "register" && (
            <Stack spacing={2}>
                <TextField
                    id="outlinedBasic" 
                    className="form-input"
                    type="text"
                    value={firstName}
                    onChange={(e) => setFirstName(e.target.value)}
                    placeholder="First Name"
                />
                <TextField
                    id="outlinedBasic" 
                    className="form-input"
                    type="text"
                    value={lastName}
                    onChange={(e) => setLastName(e.target.value)}
                    placeholder="Last Name"
                />
                <TextField
                    id="outlinedBasic" 
                    className="form-input"
                    type="text"
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                    placeholder="Username"
                />
                <TextField
                    id="outlinedBasic" 
                    className="form-input"
                    type="text"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    placeholder="Email Address"
                />
                <TextField
                    id="outinedBasic" 
                    className="form-input"
                    type="text"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    placeholder="Password"
                />
                <Button variant="contained" className="form-button" type="submit">
                    {method === "login" ? "Login" : "Register"}
                </Button>
            </Stack>
        )}
        </form>
    </Box>
    </Container>
}

export default UserForm