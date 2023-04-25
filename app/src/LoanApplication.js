import React from "react";
import { useState, useEffect } from "react";

import "./LoanApplication.css";

function LoanApplication(props) {
  const [businessEntity, setuserName] = useState("");
  const [estdYr, setestdYr] = useState("");
  const [loanAmount, setloanAmount] = useState("");
  const options = [
    { value: "", text: "--Select Accounting Provider--" },
    { value: "MYOB", text: "MYOB" },
    { value: "Xero", text: "Xero" },
    { value: "Custom", text: "Custom" },
  ];
  const [accountingService, setAC] = useState(options[0].value);
  const [data, setData] = useState("");
  const [balanceSheetInfo, setbalanceSheetInfo] = useState(
    "Click Request Balance Sheet to view Balance Sheet"
  );
  const [PL, setPL] = useState("Profit/Loss");
  const [AAV, setAAV] = useState("Average Asset Value");
  const [decision, setDecision] = useState(
    "Click Submit to view the Application status"
  );
  const handleChange = (event) => {
    setAC(event.target.value);
  };

  useEffect(() => {
    fetch("http://localhost:5000/loanInititate/")
      .then((res) => res.json())
      .then((data) => {
        setData(data.message);
      });
  }, []);

  const OnBalSheetRequest = (e) => {
    if (businessEntity && estdYr && loanAmount && accountingService) {
      fetch(
        "http://localhost:5000/fetchBalSheets/" +
          accountingService +
          "/" +
          estdYr +
          "/"
      )
        .then((res) => res.json())
        .then((data) => {
          setPL(data["Total Profit/Loss"]);

          setAAV(data["Average assetsValue"]);
          setbalanceSheetInfo(JSON.stringify(data));
        });
    }
    e.preventDefault();
  };

  const OnSubmit = (e) => {
    if (
      businessEntity &&
      estdYr &&
      loanAmount &&
      accountingService &&
      PL &&
      AAV
    ) {
      const payload = {
        Name: businessEntity,
        LoanAmount: loanAmount,
        YearEstablished: estdYr,
        SummaryOfProfitorLoss: balanceSheetInfo,
      };
      console.log(payload);
      const requestOptions = {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(payload),
      };
      fetch("http://localhost:5000/submit/", requestOptions)
        .then((res) => res.json())
        .then((data) => {
          setDecision(data.message);
        });
    }
    e.preventDefault();
  };

  return (
    <div className="loan-application-container">
      <h1 id="pageHeader" className="loan-application-text">
        Simple Business Loan Application System
      </h1>
      <h2 id="status" className="loan-application-status">
        {data}
      </h2>
      <form className="loan-application-form">
        <input
          type="text"
          id="businessEntity"
          required
          placeholder="Business Entity"
          className="loan-application-textinput input"
          onChange={(e) => setuserName(e.target.value)}
        />
        <input
          type="number"
          id="estdYr"
          required
          placeholder="Established In"
          className="loan-application-textinput input"
          onChange={(e) => setestdYr(e.target.value)}
        />
        <input
          type="number"
          id="loanAmount"
          required
          placeholder="Loan Amount"
          className="loan-application-textinput input"
          onChange={(e) => setloanAmount(e.target.value)}
        />

        <select
          id="accountingService"
          required
          className="loan-application-textinput"
          value={accountingService}
          onChange={handleChange}
        >
          {options.map((option) => (
            <option key={option.value} value={option.value}>
              {option.text}
            </option>
          ))}
        </select>

        <button
          id="requestBalanceSheet"
          className="loan-application-button button"
          onClick={OnBalSheetRequest}
        >
          Request Balance Sheet
        </button>
        <span className="loan-application-text2">Balance Sheet Info</span>
        <textarea
          id="balSheetInfo"
          disabled
          value={balanceSheetInfo}
          className="loan-application-textarea1 textarea"
        ></textarea>
        <span className="loan-application-text2">Total Profit/Loss</span>

        <span className="loan-application-text1">
          Summary of Profit or loss in the last 12 months
        </span>
        <input
          type="text"
          id="totalProfitLoss"
          value={PL}
          disabled
          className="loan-application-textinput input"
        />
        <span className="loan-application-text2">Average Asset Value</span>
        <input
          type="text"
          id="avgAV"
          value={AAV}
          disabled
          className="loan-application-textinput input"
        />
        <button
          id="submit"
          className="loan-application-button button"
          onClick={OnSubmit}
        >
          Submit Application
        </button>
        <textarea
          id="applicationStatus"
          disabled
          value={decision}
          className="loan-application-textarea2 textarea"
        ></textarea>
      </form>
    </div>
  );
}

export default LoanApplication;
