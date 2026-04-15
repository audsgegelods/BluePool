import AppBar from "@mui/material/AppBar"
import Toolbar from "@mui/material/Toolbar"
import Container from "@mui/material/Container"

function Home() {
    return ( 
    <AppBar position='static' color="rgba(161, 168, 168, 0.96)">
        <Container maxWidth="x1">
             <Toolbar disableGutters>
            <h1>yo</h1>
            </Toolbar>
        </Container>
    </AppBar>
    )
}

export default Home