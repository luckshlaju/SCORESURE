// ============================================
// LOAN PERFORMANCE REPORT (LINE CHART)
// ============================================

const performanceData = [120, 145, 170, 185, 210, 248];

const loanPerformanceChart = new Chart(
    document.getElementById("loanPerformanceChart"),
    {
        type: "line",

        data: {
            labels: [
                "Feb",
                "Mar",
                "Apr",
                "May",
                "Jun",
                "Jul"
            ],

            datasets: [{
                label: "Reports Generated",

                data: performanceData,

                borderColor: "#2563eb",

                backgroundColor: "rgba(37,99,235,0.15)",

                fill: true,

                tension: 0.45,

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

                duration: 1800

            },

            scales: {

                y: {

                    beginAtZero: true

                }

            }

        }

    }

);



// ============================================
// APPROVAL STATUS (DOUGHNUT)
// ============================================

const approvalChart = new Chart(
    document.getElementById("approvalChart"),
    {

        type: "doughnut",

        data: {

            labels: [

                "Approved",

                "Pending",

                "Rejected"

            ],

            datasets: [{

                data: [72,18,10],

                backgroundColor: [

                    "#22c55e",

                    "#f59e0b",

                    "#ef4444"

                ],

                borderWidth:2

            }]

        },

        options: {

            responsive: true,

            cutout: "65%",

            plugins: {

                legend: {

                    position: "bottom"

                }

            },

            animation: {

                animateRotate: true,

                duration: 1800

            }

        }

    }

);



// ============================================
// LIVE AI REPORT SIMULATION
// Updates every 4 seconds
// ============================================

setInterval(function () {

    // Loan Performance

    performanceData.shift();

    let last = performanceData[performanceData.length - 1];

    performanceData.push(

        last + Math.floor(Math.random() * 20 - 5)

    );

    loanPerformanceChart.update();



    // Approval Chart

    let approved = Math.floor(Math.random() * 15) + 65;

    let pending = Math.floor(Math.random() * 15) + 15;

    let rejected = 100 - approved - pending;

    approvalChart.data.datasets[0].data = [

        approved,

        pending,

        rejected

    ];

    approvalChart.update();

}, 4000);