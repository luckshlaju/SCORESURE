document.getElementById("predictBtn").addEventListener("click", async function (e) {

    e.preventDefault();

    const data = {
        age: parseInt(document.getElementById("age").value),
        gender: document.getElementById("gender").value,
        occupation: document.getElementById("occupation").value,
        district: document.getElementById("district").value,
        declared_income: parseFloat(document.getElementById("declared_income").value),
        electricity_bill: parseFloat(document.getElementById("electricity_bill").value),
        mobile_recharge: parseFloat(document.getElementById("mobile_recharge").value),
        existing_loans: parseInt(document.getElementById("existing_loans").value),
        repayment_rate: parseFloat(document.getElementById("repayment_rate").value),
        loan_amount: parseFloat(document.getElementById("loan_amount").value)
    };

    try {

        const response = await fetch("http://127.0.0.1:8000/predict", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify(data)

        });

        const result = await response.json();

        document.getElementById("result").innerHTML = `
            <h2>Prediction Result</h2>

            <p><strong>Credit Score:</strong> ${result.composite_score}</p>

            <p><strong>Risk:</strong> ${result.risk}</p>

            <p><strong>Decision:</strong> ${result.decision}</p>

            <p><strong>Estimated Income:</strong> ${result.estimated_income}</p>

            <p><strong>Income Match:</strong> ${result.income_match}%</p>

            <p><strong>Confidence:</strong> ${result.confidence}%</p>

            <p><strong>AI Explanation:</strong></p>

            <ul>
                ${result.ai_explanation.map(item => `<li>${item}</li>`).join("")}
            </ul>
        `;

    } catch (error) {

        alert("Cannot connect to backend.");

        console.log(error);

    }

});