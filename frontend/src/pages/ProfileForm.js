import React from "react";
import "../styles/UserProfileForm.css";
import { useContext, useState, useEffect } from "react";
import { AuthContext } from "../AuthContext";
import { Navigate } from "react-router-dom";
import { useNavigate } from "react-router-dom";

function Form() {
    const { user } = useContext(AuthContext);
    const [formData, setFormData] = useState({});
    const navigate = useNavigate();

    useEffect(() => {
        if (user) {
            setFormData({
                email_address: user.email_address,
                travel_budget: "",
                goal: "",
                period: "weekly",
                goal_per_period: 0,
                progress_per_period: 0,
                start_date: "",
                travel_date: "",
            });
        }
    }, [user]);

    if (!user) {
        return <Navigate to="/register" />;
    }

    const submitForm = async (event) => {
        event.preventDefault();

        const requestOptions = {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(formData),
        };

        const response = await fetch("http://localhost:8000/savings/new_savings", requestOptions);
        const data = await response.json();

        if (!response.ok) {
            console.log(data.detail);
        } else {
            console.log('Form submitted successfully');
            navigate("/financedashboard");
        }
    };

    return (
        <div className="form">
            <div className="form-container">
                <div className="header">
                    <h1>Welcome! Set Your Financial Goals</h1>
                </div>
                <form onSubmit={submitForm} className="body">
                    <div className="financial-info-container">
                        <label>
                            Savings Goal: <input
                                type="number"
                                placeholder="$$$$..."
                                value={formData.goal}
                                onChange={(event) =>
                                    setFormData({ ...formData, goal: event.target.value })
                                }
                            />
                        </label>
                        <label>
                            Travel Budget: <input
                                type="number"
                                placeholder="$$$$..."
                                value={formData.travel_budget}
                                onChange={(event) =>
                                    setFormData({ ...formData, travel_budget: event.target.value })
                                }
                            />
                        </label>
                        <label>
                            Goal Breakdown:
                            <select
                                value={formData.period}
                                onChange={(event) =>
                                    setFormData({ ...formData, period: event.target.value })
                                }
                            >
                                <option value="weekly">Weekly</option>
                                <option value="monthly">Monthly</option>
                            </select>
                        </label>
                    </div>
                    <div className="d-flex justify-content-center">
                        <button className="btn btn-primary" type="submit">Submit</button>
                    </div>
                </form>
            </div>
        </div>
    );
}

export default Form;