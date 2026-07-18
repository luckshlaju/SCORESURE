// ===============================
// Loan Approval Trend (Line Chart)
// ===============================

const loanCtx = document.getElementById("loanChart").getContext("2d");

const loanData = [65, 72, 68, 81, 77, 89];

const loanChart = new Chart(loanCtx, {
    type: "line",
    data: {
        labels: ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
        datasets: [{
            label: "Approval %",
            data: loanData,
            borderColor: "#2563eb",
            backgroundColor: "rgba(37,99,235,0.15)",
            fill: true,
            tension: 0.4,
            pointRadius: 5,
            pointHoverRadius: 7
        }]
    },
    options: {
        responsive: true,
        plugins: {
            legend: {
                display: false
            }
        },
        animation: {
            duration: 1500
        },
        scales: {
            y: {
                min: 50,
                max: 100
            }
        }
    }
});

// ===============================
// Risk Distribution (Doughnut)
// ===============================

const riskCtx = document.getElementById("riskChart");

new Chart(riskCtx, {
    type: "doughnut",
    data: {
        labels: [
            "Low Risk",
            "Medium Risk",
            "High Risk"
        ],
        datasets: [{
            data: [68, 22, 10],
            backgroundColor: [
                "#22c55e",
                "#f59e0b",
                "#ef4444"
            ],
            borderColor: "#ffffff",
            borderWidth: 4,
            hoverOffset: 12
        }]
    },
    options: {
        responsive: true,
        maintainAspectRatio: true,
        aspectRatio: 1,
        cutout: "65%",   // Nice donut look

        plugins: {
            legend: {
                position: "bottom",
                labels: {
                    boxWidth: 18,
                    padding: 18,
                    font: {
                        family: "Poppins",
                        size: 13
                    }
                }
            },
            tooltip: {
                callbacks: {
                    label: function(context) {
                        return context.label + ": " + context.raw + "%";
                    }
                }
            }
        },

        layout: {
            padding: 15
        },

        animation: {
            animateRotate: true,
            animateScale: true,
            duration: 1800
        }
    }
});
// ===============================
// Monthly Applications (Bar Chart)
// ===============================

const barCtx = document.getElementById("barChart").getContext("2d");

const monthlyData = [105, 122, 141, 158, 174, 196];

const barChart = new Chart(barCtx, {
    type: "bar",
    data: {
        labels: ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
        datasets: [{
            label: "Applications",
            data: monthlyData,
            backgroundColor: "#2563eb",
            borderRadius: 8
        }]
    },
    options: {
        responsive: true,
        plugins: {
            legend: {
                display: false
            }
        },
        animation: {
            duration: 1500
        }
    }
});

// ======================================
// Simulate Live Dashboard Updates
// ======================================

setInterval(() => {

    // Loan trend
    loanData.shift();
    loanData.push(Math.floor(Math.random() * 25) + 70);
    loanChart.update();

    // Monthly applications
    monthlyData.shift();
    monthlyData.push(Math.floor(Math.random() * 70) + 140);
    barChart.update();

    // Risk distribution
    const low = Math.floor(Math.random() * 15) + 55;
    const medium = Math.floor(Math.random() * 20) + 20;
    const high = 100 - low - medium;

    riskChart.data.datasets[0].data = [low, medium, high];
    riskChart.update();

}, 5000);