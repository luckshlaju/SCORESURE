async function loadRiskChart() {
    try {
        const response = await fetch("http://127.0.0.1:8000/risk-distribution");
        const data = await response.json();

        const ctx = document.getElementById("riskChart").getContext("2d");

        new Chart(ctx, {
            type: "doughnut",
            data: {
                labels: data.labels,
                datasets: [{
                    data: data.values,
                    backgroundColor: [
                        "#4CAF50",
                        "#FFC107",
                        "#F44336"
                    ]
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: "bottom"
                    }
                }
            }
        });

    } catch (error) {
        console.error(error);
    }
}

loadRiskChart();