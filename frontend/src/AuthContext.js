import React, { useState, useContext, useEffect } from 'react';
// import { useHistory } from 'react-router-dom';

// Create a context for authentication
export const AuthContext = React.createContext();

// Custom hook to access the AuthContext
export const useAuth = () => {
    return useContext(AuthContext);
};

// AuthProvider component to wrap the app with authentication context
export const AuthProvider = (props) => {
    const [token, setToken] = useState(localStorage.getItem('authToken'));
    const [user, setUser] = useState(localStorage.getItem('user'));
    // const history = useHistory();

    useEffect(() => {
        const fetchUser = async () => {
            if (!token) {
                // If the token is not present, clear the user data
                setUser(null);
                localStorage.removeItem('user');
                return;
            }

            const requestOptions = {
                method: 'GET',
                headers: {
                    "Content-Type": "application/json",
                    Authorization: `Bearer ${token}`,
                },
            };

            const response = await fetch("http://localhost:8000/users/me", requestOptions);

            if (response.ok) {
                const data = await response.json();
                setUser(data);
                localStorage.setItem('user', JSON.stringify(data));
            } else {
                const errorData = await response.json();
                if (errorData.detail === 'Token has expired') {
                    // If the token has expired, clear the user data and token
                    setUser(null);
                    setToken(null);
                    localStorage.removeItem('user');
                    localStorage.removeItem('authToken');

                    // Redirect to the home page
                    window.location.href = '/';
                }
                setToken(null);
            }
        };
        fetchUser();
    }, [token]);

    const login = (userData) => {
        // Simulate logging in by setting user data in state and localStorage
        setToken(userData.access_token);
        localStorage.setItem('authToken', userData.access_token);
    };

    const logout = () => {
        // Simulate logging out by removing user data from state and localStorage
        setUser(null);
        localStorage.removeItem('user');

        // Remove the authToken from local storage
        setToken(null);
        localStorage.removeItem('authToken');

        // Redirect to the home page
        window.location.href = '/';
    };

    return (
        <AuthContext.Provider value={{ token, setToken, user, setUser, login, logout }}>
            {props.children}
        </AuthContext.Provider>
    );
};
