import AppBar from "@mui/material/AppBar";
import Container from "@mui/material/Container";
import Toolbar from "@mui/material/Toolbar";
import Menu from "@mui/material/Menu";
import Button from "@mui/material/Button";

import {Link} from 'react-router';

function NavBar() {
    return (
        <div>
        <AppBar position="static" >
            <Container maxWidth="x1">
                <Toolbar disableGutters>
                    <Button
                            variant='contained'
                            size="small"
                            component={Link}
                            to={'/logout/'}
                            sx={{ backgroundColor: 'red'}}
                            >
                            Logout
                    </Button>
                    <Button
                            variant='contained'
                            size="small"
                            component={Link}
                            to={'/rides/create'}
                            sx={{ backgroundColor: 'black'}}
                            >
                            Post a Ride
                    </Button>
                </Toolbar>
            </Container>
        </AppBar>
        </div>
    )
}

export default NavBar