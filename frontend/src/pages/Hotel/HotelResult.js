import React from "react";
// import forwardArrow from "../assets/Forward.svg";
import HotelTicket from "./HotelTicket";
import NoneFound from "../Flight/NoneFound";

function HotelResult(props) {
  const {
    filteredData,
    isSearchClicked,
  } = props;

  return (
    <div className="card" style={{ height: "100%" }}>
      <div className="card-body">
        {!isSearchClicked &&
        filteredData.length === 0 ? (
          <NoneFound
            type="Hotels" 
          />
        ) : isSearchClicked &&
          filteredData.length === 0  ? (
          <div
            className="d-flex justify-content-center"
            style={{ color: "red" }}
          >
            <h3>No Hotels Found</h3>
          </div>
        ) : (
          <div>
            <div className="mb-4">
              <div
                style={{
                  fontSize: "20px",
                  fontWeight: "bold",
                }}
              >
                Available Hotels{" "}
                {/* <span>
                  <img src={forwardArrow} alt="arrow" className="ml-2" />
                </span> */}
              </div>
            </div>
            <div>
              {isSearchClicked ? (
                <div className="row">
                  <div className="col">
                    <div style={{ color: "deepskyblue", fontWeight: "bold" }}>
                      Hotel
                      <p>{filteredData[0].depart}</p>
                    </div>
                    <HotelTicket
                      filteredData={filteredData}
                    />
                  </div>
                </div>
                ) : (
                    null
                )}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default HotelResult;