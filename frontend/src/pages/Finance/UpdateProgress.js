import { useState, useContext } from "react"
// import { useNavigate } from "react-router-dom"
import { AuthContext } from "../../AuthContext"
import TitleCard from "../../components/cards/TitleCard"
import axios from "axios"

function UpdateProgress(){

    // const navigate = useNavigate()

    const [addToSavings, setAddToSavings] = useState(0);

    const { user } = useContext(AuthContext);

    const updateInputValue = (val) => {
        console.log(val)
        if (!isNaN(val)) {
            setAddToSavings(parseFloat(val))
        } else {
            setAddToSavings(0)
        }
        console.log(addToSavings)
    }
    
    

    const updateSavings = () => {

        const email = user.email_address;
        console.log(email);
        axios.get(`http://localhost:8000/savings/update_progress/${email}/${addToSavings}`)
          .then(response => {
            console.log("Current Savings: " + response.data.current_savings);
            console.log("Progress per period: " + response.data.progress_per_period);
            console.log("Goal per period: " + response.data.goal_per_period);
            console.log("Goal: " + response.data.goal);
          })
          .catch(error => {
            console.error('Error fetching current savings:', error);
          });

        // navigate("/Dashboard") // Redirect to Dashboard

    }

    const onClick = () => {
        updateSavings()
        window.location.reload()
    }
    
    return(
        <>
            <TitleCard title="Update Progress" topMargin="mt-2">

                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div className={`form-control w-full`}>
                        <label className="label">
                            <span className={"label-text text-base-content "}>Added Savings ($)</span>
                        </label>
                        <input type="number" value={addToSavings} placeholder={0} onChange={(e) => updateInputValue(e.target.value)}className="input  input-bordered w-full " />
                    </div>
                </div>
                <div className="mt-16"><button className="btn btn-primary float-right" onClick={onClick}>Update</button></div>

            </TitleCard>
        </>

    )

}

export default UpdateProgress