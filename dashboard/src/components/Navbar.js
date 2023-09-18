import React from 'react';
import { useNavigate } from 'react-router-dom';
import Button from '@mui/material/Button';
import { useInfo } from '../containers/hooks/useInfo';
import { GoogleLogin, GoogleLogout } from 'react-google-login';

const CLIENT_ID = process.env.REACT_APP_CLIENT_ID

const Navbar = () => {
    const navigate = useNavigate()
    const { logged_in, onFailure, onLogoutSuccess, onSuccess } = useInfo();

    return (
        <div style={{ display: 'flex', flexDirection: 'row', flexWrap: 'wrap', justifyContent: 'space-between', alignItems: 'center' }}>
            <h1 onClick={() => { navigate("/"); }} style={{ marginLeft: '2%', cursor: "pointer" }}>世朋電影院</h1>
            <div style={{display: 'flex', width: 300, flexDirection: 'row', alignItems: 'center'}}>
                <Button onClick={() => {navigate('/users/reservation')}} sx={{ marginRight: '2%', marginTop: '1%', fontSize: "1.5rem", color: "#00BFFF" }}>
                    Reservation
                </Button>
                {
                    !logged_in
                        ?
                        <div>
                            <GoogleLogin
                                clientId={CLIENT_ID}
                                buttonText="Login"
                                onSuccess={onSuccess}
                                onFailure={onFailure}
                                cookiePolicy={'single_host_origin'}
                            />
                        </div>
                        :
                        <div>
                            <GoogleLogout
                                clientId={CLIENT_ID}
                                buttonText="Logout"
                                onLogoutSuccess={onLogoutSuccess}
                            />
                        </div>
                }
            </div>
        </div>
    );
}



export default Navbar