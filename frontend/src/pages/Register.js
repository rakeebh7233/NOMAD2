import "../styles/Register.css";
import { useState, useContext } from "react";
import { AuthContext } from "../AuthContext";
import ErrorMessage from "../shared/ErrorMessage";
import { useNavigate } from "react-router-dom";

const Register = () => {
  const [firstName, setFirstName] = useState("");
  const [lastName, setLastName] = useState("");
  const [userName, setUserName] = useState("")
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmationPassword, setConfirmationPassword] = useState("");
  const [errorMessage, setErrorMessage] = useState("");
  const { login } = useContext(AuthContext);

  const navigate = useNavigate();

  const submitRegistration = async () => {
    const requestOptions = {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ "username": userName, "firstName": firstName, "lastName": lastName, "email_address": email, "hashed_password": password }),
    };

    const response = await fetch("http://localhost:8000/register", requestOptions);
    const data = await response.json();

    if (!response.ok) {
      console.log(data.detail);
      setErrorMessage(data.detail);
    } else {
      // Log in the user with the access token
      const loginRequestOptions = {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body: JSON.stringify(JSON.stringify(`grant_type=&username=${email}&password=${password}&scope=&client_id=&client_secret=`)),
      };

      const loginResponse = await fetch("http://localhost:8000/login", loginRequestOptions);
      const loginData = await loginResponse.json();

      if (!loginResponse.ok) {
        console.log(loginData.detail);
        setErrorMessage(loginData.detail);
      } else {
        // Log in the user with the access token
        login(loginData);
        setErrorMessage('');
        navigate("/");
      }
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (password === confirmationPassword && password.length >= 5) {
      submitRegistration();
    } else {
      setErrorMessage("Passwords do not match or are too short (min 5 characters)");
    }
  };

  return (
    <section class="text-center text-lg-start">
      <div class="container py-4">
        <div class="row g-0 align-items-center">
          <div class="col-lg-6 mb-5 mb-lg-0">
            <div class="card cascading-right" >
              <div class="card-body p-5 shadow-5 text-center">
                <h2 class="fw-bold mb-5">Sign up now</h2>
                <form onSubmit={handleSubmit}>
                  <div class="row">
                    <div class="col-md-6 mb-4">
                      <div class="form-floating">
                        <input
                          type="text"
                          id="form3Example1"
                          value={firstName}
                          onChange={(e) => setFirstName(e.target.value)}
                          class="form-control" />
                        <label class="form-label" for="form3Example1">First name</label>
                      </div>
                    </div>
                    <div class="col-md-6 mb-4">
                      <div class="form-floating">
                        <input
                          type="text"
                          id="form3Example2"
                          value={lastName}
                          onChange={(e) => setLastName(e.target.value)}
                          class="form-control" />
                        <label class="form-label" for="form3Example2">Last name</label>
                      </div>
                    </div>
                  </div>

                  <div class="form-floating mb-4">
                    <input
                      type="text"
                      id="userNameForm"
                      value={userName}
                      onChange={(e) => setUserName(e.target.value)}
                      class="form-control" />
                    <label class="form-label" for="form3Example3">Username</label>
                  </div>

                  <div class="form-floating mb-4">
                    <input
                      type="email"
                      id="form3Example3"
                      value={email}
                      onChange={(e) => setEmail(e.target.value)}
                      class="form-control" />
                    <label class="form-label" for="form3Example3">Email address</label>
                  </div>

                  <div class="form-floating mb-4">
                    <input
                      type="password"
                      id="form3Example4"
                      value={password}
                      onChange={(e) => setPassword(e.target.value)}
                      class="form-control" />
                    <label class="form-label" for="form3Example4">Password</label>
                  </div>

                  <div class="form-floating mb-4">
                    <input
                      type="password"
                      id="form3Example5"
                      value={confirmationPassword}
                      onChange={(e) => setConfirmationPassword(e.target.value)}
                      class="form-control" />
                    <label class="form-label" for="form3Example4">Confirm Password</label>
                  </div>
                  {errorMessage && <ErrorMessage message={errorMessage} />}
                  <button type="submit" class="btn btn-primary btn-block mb-4">
                    Sign up
                  </button>

                  {/* <div class="text-center">
                    <p>or sign up with:</p>
                    <button type="button" class="btn btn-link btn-floating mx-1">
                      <i class="fab fa-facebook-f"></i>
                    </button>

                    <button type="button" class="btn btn-link btn-floating mx-1">
                      <i class="fab fa-google"></i>
                    </button>

                    <button type="button" class="btn btn-link btn-floating mx-1">
                      <i class="fab fa-twitter"></i>
                    </button>

                    <button type="button" class="btn btn-link btn-floating mx-1">
                      <i class="fab fa-github"></i>
                    </button>
                  </div> */}
                </form>
              </div>
            </div>
          </div>

          <div class="col-lg-6 mb-5 mb-lg-0">
            <img src="https://images.unsplash.com/photo-1500835556837-99ac94a94552?auto=format&fit=crop&q=80&w=1887&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D" class="w-100 rounded-4 shadow-4" height="625" alt="Plane" />
          </div>
        </div>
      </div>
    </section>
  )
}

export default Register;