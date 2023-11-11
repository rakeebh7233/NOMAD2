import React from "react";

function FinancialInfo({ formData, setFormData }) {
  return (
    <div className="financial-info-container">
      
      <label>
        Yearly Income: <input
        type="number"
        placeholder="$$$$..."
        value={formData.yearlyIncome}
        onChange={(event) =>
          setFormData({ ...formData, yearlyIncome: event.target.value })
        }
      />
      </label>  

      <label>
        Monthly Spending: <input
        type="number"
        placeholder="$$$$..."
        value={formData.firstName}
        onChange={(event) =>
          setFormData({ ...formData, monthlySpending: event.target.value })
        }
      />
      </label>

      <label>
        Estimated Savings: <input
        type="number"
        placeholder="$$$$..."
        value={formData.estimatedSavings}
        onChange={(event) =>
          setFormData({ ...formData, estimatedSavings: event.target.value })
        }
      />
      </label>

      <label>
        Travel Budge: <input
        type="number"
        placeholder="$$$$..."
        value={formData.travelBudget}
        onChange={(event) =>
          setFormData({ ...formData, travelBudget: event.target.value })
        }
      />
      </label>

      <label>
        Monthly Saving Goal: <input
        type="number"
        placeholder="$$$$..."
        value={formData.monthlySavingGoal}
        onChange={(event) =>
          setFormData({ ...formData, monthlySavingGoal: event.target.value })
        }
      />
      </label>

    </div>
  );
}

export default FinancialInfo;