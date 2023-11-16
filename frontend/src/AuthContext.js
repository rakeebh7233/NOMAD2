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
            const requestOptions = {
                method: 'GET',
                headers: {
                    "Content-Type": "application/json",
                    Authorization: `Bearer ${token}`,
                },
            };

            const response = await fetch("users/me", requestOptions);

            if (!response.ok) {
                setToken(null);
            }
            localStorage.setItem('authToken', token);
        };
        fetchUser();
    }, [token]);

    const login = (userData) => {
        // Simulate logging in by setting user data in state and localStorage
        setUser(userData);
        localStorage.setItem('user', JSON.stringify(userData));
    };

    const logout = () => {
        // Simulate logging out by removing user data from state and localStorage
        setUser(null);
        localStorage.removeItem('user');
    };

    return (
        <AuthContext.Provider value={[token, setToken]}>
            {props.children}
        </AuthContext.Provider>
    );
};
