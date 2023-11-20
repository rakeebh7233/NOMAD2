import React from 'react';
import { useContext, useState } from "react";
import CloseButton from 'react-bootstrap/CloseButton';
import { AuthContext } from "../AuthContext";
import ErrorMessage from "../shared/ErrorMessage";

const LoginForm = ({ isLoginVisible, closeLogin }) => {
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [errorMessage, setErrorMessage] = useState("");
    const {login} = useContext(AuthContext);

    const submitLogin = async () => {  
        const requestOptions = {
            method: "POST",
            headers: { "Content-Type": "application/x-www-form-urlencoded" },
            body: JSON.stringify(`grant_type=&username=${email}&password=${password}&scope=&client_id=&client_secret=`),
        };

        const response = await fetch("http://localhost:8000/login", requestOptions);
        const data = await response.json();

        if (!response.ok) {
            setErrorMessage(data.detail);
        }
        else {
            login(data);
            closeLogin();
            setErrorMessage('');
        }
    }

    const handleSubmit = (e) => {
        e.preventDefault();
        submitLogin();
    };

        return (
            <section className={`${isLoginVisible ? "active" : ""} loginShow`} class="vh-100 loginShow">
                <div class="container py-5 h-100">
                    <div class="row d-flex justify-content-center align-items-center h-100">
                        <div class="col-12 col-md-8 col-lg-6 col-xl-5">
                            <div class="card shadow-5-strong" style={{ borderRadius: "1rem", top: "-30px" }}>
                                <div id="closeLogin" onClick={closeLogin}>
                                    <CloseButton />
                                </div>
                                <div class="card-body p-5 text-center">

                                    <h3 class="mb-5">Sign in</h3>

                                    <div class="form-floating mb-4">
                                        <input 
                                            type="email"
                                            id="typeEmailX-2"
                                            value={email}
                                            onChange={(e) => setEmail(e.target.value)}
                                            class="form-control form-control-lg"
                                            required />
                                        <label id="formLabel" class="form-label" for="typeEmailX-2">Email</label>
                                    </div>

                                    <div class="form-floating mb-4">
                                        <input 
                                            type="password" 
                                            id="typePasswordX-2" 
                                            value={password}
                                            onChange={(e) => setPassword(e.target.value)}
                                            class="form-control form-control-lg" />
                                        <label class="form-label" for="typePasswordX-2">Password</label>
                                    </div>

                                    <div class="form-check d-flex justify-content-start mb-4">
                                        <input class="form-check-input" type="checkbox" value="" id="form1Example3" />
                                        <label class="form-check-label" for="form1Example3"> Remember password </label>
                                    </div>
                                    {errorMessage && <ErrorMessage message={errorMessage} />}
                                    <button class="btn btn-primary btn-lg btn-block" type="submit" onClick={handleSubmit}>
                                        Login
                                    </button>
                                    <button class="btn btn-info btn-lg btn-block" type="button">
                                        <a class="nav-link text-light" href="/register">Register</a>
                                    </button>


                                    <hr class="my-4"></hr>

                                    <button class="btn btn-lg btn-block btn-primary" style={{ backgroundColor: "#dd4b39" }}
                                        type="submit"><i class="fab fa-google me-2"></i> Sign in with google</button>
                                    <button class="btn btn-lg btn-block btn-primary mb-2" style={{ backgroundColor: "#3b5998" }}
                                        type="submit"><i class="fab fa-facebook-f me-2"></i>Sign in with facebook</button>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </section>
        )
    }


    export default LoginForm;