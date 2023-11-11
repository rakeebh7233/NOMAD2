import React, { useState } from "react";
import Address from "./Address";
import PersonalInfo from "./PersonalInfo";
import FinancialInfo from "./FinancialInfo";
import "../../styles/UserProfileForm.css";

function Form() {
  const [page, setPage] = useState(0);
  const [formData, setFormData] = useState({firstName: "", 
  lastName: "", 
  email: "", 
  birthday: "", 
  phoneNumber: "", 
  street: "", 
  city: "", 
  state: "", 
  zip:"", 
  yearlyIncome:"",
  monthlySpending: "",
  estimatedSavings: "",
  travelBudget: "",
  monthlySavingGoal: "" })

  const FormTitles = ["Personal Info", "Address", "Financial Info"];

  const PageDisplay = () => {
    if (page === 0) {
      return <PersonalInfo formData={formData} setFormData={setFormData} />;
    } else if (page === 1) {
      return <Address formData={formData} setFormData={setFormData} />;
    } else {
      return <FinancialInfo formData={formData} setFormData={setFormData} />;
    }
  };

  return (
    <div className="form">
      <div className="progressbar">
        <div
          style={{ width: page === 0 ? "33.3%" : page === 1 ? "66.6%" : "100%" }}
        ></div>
      </div>
      <div className="form-container">
        <div className="header">
          <h1>{FormTitles[page]}</h1>
        </div>
        <div className="body">{PageDisplay()}</div>
        <div className="footer">
          <button
            disabled={page === 0}
            onClick={() => {
              setPage((currPage) => currPage - 1);
            }}
          >
            Prev
          </button>
          <button
            onClick={() => {
              if (page === FormTitles.length - 1) {
                alert("FORM SUBMITTED");
                console.log(formData);
              } else {
                setPage((currPage) => currPage + 1);
              }
            }}
          >
            {page === FormTitles.length - 1 ? "Submit" : "Next"}
          </button>
        </div>
      </div>
    </div>
  );
}

export default Form;