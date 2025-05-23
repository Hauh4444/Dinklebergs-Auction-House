// External Libraries
import { useEffect, useState } from "react";
import { Button } from "@mui/material";
import axios from "axios";

// Internal Modules
import Header from "@/Components/Header/Header";
import RightNav from "@/Components/Navigation/RightNav/RightNav";

// Stylesheets
import "./Security.scss"


const Security = () => {
    const [user, setUser] = useState({});

    // Fetch user data from the backend API
    useEffect(() => {
        axios.get(`${ import.meta.env.VITE_BACKEND_API_URL }/user/`,
            {
                headers: { "Content-Type": "application/json" },
                withCredentials: true, // Ensures cookies are sent with requests
            })
            .then((res) => setUser(res.data.user)) // Set the user state
            .catch((err) => console.error(err)); // Log errors if any
    }, []);

    const password_reset_request = () => {
        axios.post(`${ import.meta.env.VITE_BACKEND_API_URL }/auth/password_reset_request/`,
                {
                headers: { "Content-Type": "application/json" },
                withCredentials: true,
            })
            .then(() => alert("Password reset request email sent to: " + user["email"]))
            .catch((err) => console.error(err));
    }

    return (
        <div className="securityPage page">
            <div className="mainPage">
                { /* Page Header */ }
                <Header />

                <h1>Login & Security</h1>
                <div className="card">
                    <div className="info">
                        <h2>Username</h2>
                        <p>{ user["username"] }</p>
                    </div>
                    <Button
                        className="editBtn"
                        onClick={ () => {} }
                    >
                        Edit
                    </Button>
                </div>
                <div className="card">
                    <div className="info">
                        <h2>Email</h2>
                        <p>{ user["email"] }</p>
                    </div>
                    <Button
                        className="editBtn"
                        onClick={ () => {} }
                    >
                        Edit
                    </Button>
                </div>
                <div className="card">
                    <div className="info">
                        <h2>Password</h2>
                        <p>********</p>
                    </div>
                    <Button
                        className="editBtn"
                        onClick={ () => password_reset_request() }
                    >
                        Reset
                    </Button>
                </div>
            </div>
            { /* Right-side Navigation */ }
            <RightNav />
        </div>
    )
}

export default Security;