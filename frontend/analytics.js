// =======================================
// PORTFOLIO GROWTH (LINE CHART)
// =======================================

const portfolioData = [12, 15, 18, 20, 23, 27, 30, 34, 38, 42, 46, 50];

const portfolioChart = new Chart(
document.getElementById("portfolioChart"),
{
    type: "line",

    data: {

        labels: [
            "Jan","Feb","Mar","Apr","May","Jun",
            "Jul","Aug","Sep","Oct","Nov","Dec"
        ],

        datasets: [{

            label: "Portfolio (₹ Cr)",

            data: portfolioData,

            borderColor: "#2563eb",

            backgroundColor: "rgba(37,99,235,0.15)",

            fill: true,

            tension: 0.4,

            pointRadius: 5

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

        }

    }

});


// =======================================
// RISK DISTRIBUTION (DOUGHNUT)
// =======================================

const riskChart = new Chart(
document.getElementById("riskChart"),
{

    type: "doughnut",

    data: {

        labels: [

            "Low Risk",

            "Medium Risk",

            "High Risk"

        ],

        datasets: [{

            data: [68,22,10],

            backgroundColor: [

                "#22c55e",

                "#f59e0b",

                "#ef4444"

            ]

        }]

    },

    options: {

        responsive:true,

        cutout:"65%",

        plugins:{

            legend:{

                position:"bottom"

            }

        },

        animation:{

            animateRotate:true,

            duration:1800

        }

    }

});



// =======================================
// MONTHLY PERFORMANCE (BAR)
// =======================================

const performanceData = [82,88,91,89,94,96,93,95,97,96,98,99];

const performanceChart = new Chart(
document.getElementById("monthlyPerformanceChart"),
{

    type:"bar",

    data:{

        labels:[
        "Jan","Feb","Mar","Apr","May","Jun",
        "Jul","Aug","Sep","Oct","Nov","Dec"
        ],

        datasets:[{

            label:"Approval %",

            data:performanceData,

            backgroundColor:"#2563eb",

            borderRadius:8

        }]

    },

    options:{

        responsive:true,

        plugins:{

            legend:{

                display:false

            }

        },

        animation:{

            duration:1800

        }

    }

});



// =======================================
// LOAN CATEGORY (PIE)
// =======================================

// =======================================
// LOAN CATEGORY DISTRIBUTION
// =======================================

const categoryChart = new Chart(
    document.getElementById("loanCategoryChart"),
    {

        type: "pie",

        data: {

            labels: [

                "Home Loan",

                "Personal Loan",

                "Vehicle Loan",

                "Education Loan",

                "Business Loan"

            ],

            datasets: [{

                data: [34,24,15,8,19],

                backgroundColor: [

                    "#2563eb",
                    "#22c55e",
                    "#f59e0b",
                    "#ef4444",
                    "#8b5cf6"

                ],

                borderColor:"#ffffff",

                borderWidth:3,

                hoverOffset:20

            }]

        },

       options: {
    responsive: true,
    maintainAspectRatio: false,
    layout: {
        padding: {
            top: 10,
            bottom: 10,
            left: 20,
            right: 20
        }
    },

            plugins:{

                legend:{

                    position:"bottom",

                    labels:{

                        boxWidth:18,
                        boxHeight:18,
                        padding:20,
                        usePointStyle:true,
                        pointStyle:"circle",
                        font:{
                            size:14,
                            weight:"600"
                        }
                    }

                },

                tooltip:{

                    callbacks:{

                        label:function(context){

                            return context.label +
                            ": " +
                            context.raw +
                            "%";

                        }

                    }

                }

            }

        }

    }
);


// =======================================
// LIVE AI SIMULATION
// Updates every 4 seconds
// =======================================

setInterval(()=>{

    // Portfolio Growth

    portfolioData.shift();

    portfolioData.push(
        portfolioData[portfolioData.length-1] +
        Math.floor(Math.random()*3)
    );

    portfolioChart.update();



    // Monthly Performance

    performanceData.shift();

    performanceData.push(
        Math.floor(Math.random()*8)+92
    );

    performanceChart.update();



    // Risk Distribution

    let low=Math.floor(Math.random()*15)+60;

    let medium=Math.floor(Math.random()*15)+20;

    let high=100-low-medium;

    riskChart.data.datasets[0].data=[low,medium,high];

    riskChart.update();



    // Loan Categories

    let home=Math.floor(Math.random()*8)+30;

    let personal=Math.floor(Math.random()*8)+22;

    let vehicle=Math.floor(Math.random()*6)+12;

    let education=Math.floor(Math.random()*5)+8;

    let business=
    100-home-personal-vehicle-education;

    categoryChart.data.datasets[0].data=[

        home,

        personal,

        vehicle,

        education,

        business

    ];

    categoryChart.update();

},4000);