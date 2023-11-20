import React, { useState, useContext, useEffect } from 'react';

// Create a context for authentication
export const AuthContext = React.createContext();

// Custom hook to access the AuthContext
export const useAuth = () => {
    return useContext(AuthContext);
};

// AuthProvider component to wrap the app with authentication context
export const AuthProvider = (props) => {
    const [token, setToken] = useState(localStorage.getItem('authToken'));
    const [user, setUser] = useState(null);

    useEffect(() => {
        const fetchUser = async () => {
            if (!token) {
                // If the token is not present, don't try to fetch the user data
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
                console.log(data);
                setUser(data);
                localStorage.setItem('user', JSON.stringify(data));
            } else {
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
    };

    return (
        <AuthContext.Provider value={{ token, setToken, user, setUser, login, logout }}>
            {props.children}
        </AuthContext.Provider>
    );
};
