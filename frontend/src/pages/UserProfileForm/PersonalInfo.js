import React from "react";

function PersonalInfo({ formData, setFormData }) {
  return (
    <div className="personal-info-container">
      <label>
        First Name: <input
        type="text"
        placeholder="First Name..."
        value={formData.firstName}
        onChange={(event) =>
          setFormData({ ...formData, firstName: event.target.value })
        }
      />
      </label>

      <label>
        Last Name: <input
        type="text"
        placeholder="Last Name..."
        value={formData.lastName}
        onChange={(event) =>
          setFormData({ ...formData, lastName: event.target.value })
        }
      />
      </label>

      <label>
        Email: <input
        type="email"
        placeholder="abc123@nyu.edu..."
        value={formData.email}
        onChange={(event) =>
          setFormData({ ...formData, email: event.target.value })
        }
      />
      </label>

      <label>
        Phone Number: <input
        type="tel"
        placeholder="(123)-456-7890..."
        value={formData.phoneNumber}
        onChange={(event) =>
          setFormData({ ...formData, phoneNumber: event.target.value })
        }
      />
      </label>

      <label>
        Birthday: <input
        type="date"
        placeholder="MM/DD/YYY..."
        value={formData.birthday}
        onChange={(event) =>
          setFormData({ ...formData, birthday: event.target.value })
        }
      />
      </label>

    </div>
  );
}

export default PersonalInfo;