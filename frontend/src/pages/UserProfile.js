import React, { useState } from 'react';

function UserProfile() {
    const [firstName, setFirstName] = useState('');
    const [lastName, setLastName] = useState('');
    const [email, setEmail] = useState('');
    const [address, setAddress] = useState(''); // [street, city, state, zip
    const [phoneNumber, setPhoneNumber] = useState('');
    const [citizenship, setCitizenship] = useState(''); // [country, passport number, expiration date]
    const [birthday, setBirthday] = useState(''); // [month, day, year]

    const[yearlyIncome, setYearlyIncome] = useState('');
    const[monthlySpending, setMonthlySpending] = useState('');
    const[estimatedSavings, setEstimatedSavings] = useState('');
    const[travelBudget, setTravelBudget] = useState('');
    const[monthlySavingGoal, setMonthlySavingGoal] = useState('');

    const handleSubmit = (event) => {
        event.preventDefault();
        // handle form submission logic here

    };

    const getUserInfo = () => {
        //go into user database and get all info related to user based on user and pass
    };

    const updateUserInfo = () => {
        //update all user info based on any changes made once submit is click
    };

    return (
        <form class="flex-form" onSubmit={handleSubmit}>
        <h3>Personal Information</h3>
        <div className='row'>
            <div className='col-sm-3'>
                <label>
                    First Name:
                    <input type="text" value={firstName} onChange={(e) => setFirstName(e.target.value)} />
                </label>
            </div>
            <div className='col-sm-3'>
                <label>
                    Last Name:
                    <input type="text" value={lastName} onChange={(e) => setLastName(e.target.value)} />
                </label>
            </div>
            <div className='col-sm-3'>
                <label>
                    Email:
                    <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} />
                </label>
            </div>
        </div>


        <div className='row'>
            <div className='col-sm-3'>
                <label>
                    Address:
                    <input type="address" value={address} onChange={(e) => setAddress(e.target.value)} />
                </label>
            </div>
            <div className='col-sm-3'>
                <label>
                    Phone Number:
                    <input type="tel" value={phoneNumber} onChange={(e) => setPhoneNumber(e.target.value)} />
                </label>
            </div>
            <div className='col-sm-3'>
                <label>
                    Citizenship:
                    <input type="text" value={citizenship} onChange={(e) => setCitizenship(e.target.value)} />
                </label>
            </div>
            <div className='col-sm-3'>
                <label>
                    Birthday:
                    <input type="date" value={birthday}  placeholder = 'YYYY-MM-DD' onChange={(e) => setBirthday(e.target.value)} />
                </label>  
            </div>
        </div>


        <h3>Financial Information</h3>

        <div className='row'>
            <div className='col-sm-3'>
                <label>
                    Yearly Income:
                    <input type="number" value={yearlyIncome} onChange={(e) => setYearlyIncome(e.target.value)} />
                </label>
            </div>
            <div className='col-sm-3'>
                <label>
                    Monthly Spending:
                    <input type="number" value={monthlySpending} onChange={(e) => setMonthlySpending(e.target.value)} />
                </label>
            </div>
            <div className='col-sm-3'>
                <label>
                    Estimated Savings:
                    <input type="number" value={estimatedSavings} onChange={(e) => setEstimatedSavings(e.target.value)} />
                </label>
            </div>
        </div>

        <div className='row'>
            <div className='col-sm-3'>
                <label>
                    Monthly Saving Goal:
                    <input type="number" value={monthlySavingGoal} onChange={(e) => setMonthlySavingGoal(e.target.value)} />
                </label>
            </div>
            <div className='col-sm-3'>
                <label>
                    Travel Budget:
                    <input type="number" value={travelBudget} onChange={(e) => setTravelBudget(e.target.value)} />
                </label>
            </div>
        </div>
  
        <button type="submit">Submit</button>
        </form>
    );
}

export default UserProfile;
