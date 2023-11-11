import React from "react";

function Address({ formData, setFormData }) {
  return (
    <div className="address-container">
      <label>
        Street: <input
        type="text"
        placeholder="Street..."
        value={formData.street}
        onChange={(event) =>
          setFormData({ ...formData, street: event.target.value })
        }
      />
      </label>

      <label>
        City: <input
        type="text"
        placeholder="City..."
        value={formData.city}
        onChange={(event) =>
          setFormData({ ...formData, city: event.target.value })
        }
      />
      </label>

      <label>
        State: <input
        type="text"
        placeholder="State..."
        value={formData.state}
        onChange={(event) =>
          setFormData({ ...formData, state: event.target.value })
        }
      />
      </label>

      <label>
        Zip: <input
        type="text"
        placeholder="Zip Code..."
        value={formData.zip}
        onChange={(event) =>
          setFormData({ ...formData, zip: event.target.value })
        }
      />
      </label>

    </div>
  );
}

export default Address;
