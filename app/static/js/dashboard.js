// Global chart variables
let severityChart = null;
let categoryChart = null;

// ----------------------------
// Scan Button
// ----------------------------
document.addEventListener("DOMContentLoaded", () => {

    const btn1 = document.getElementById("scanBtn");
    const btn2 = document.getElementById("scanBtn2");

    if (btn1) btn1.addEventListener("click", startScan);
    if (btn2) btn2.addEventListener("click", startScan);

});

// ----------------------------
// Main Scan Function
// ----------------------------

async function startScan(){

    const buttons = document.querySelectorAll("#scanBtn,#scanBtn2");

    buttons.forEach(btn=>{
        btn.disabled=true;
        btn.innerHTML='<span class="spinner-border spinner-border-sm"></span> Scanning...';
    });

    try{

        const response = await fetch("/api/scan",{
            method:"POST"
        });

        const result = await response.json();

        if(result.success){

            updateDashboard(result.data);

            document.getElementById("lastScan").innerText =
                new Date().toLocaleString();

        }else{

            alert(result.error || "Scan failed");

        }

    }catch(err){

        console.error(err);

        alert("Unable to connect to backend.");

    }

    buttons.forEach(btn=>{
        btn.disabled=false;
        btn.innerHTML='<i class="bi bi-play-circle"></i> Scan AWS';
    });

}

// ----------------------------
// Update Dashboard
// ----------------------------

function updateDashboard(data){

    const summary = data.summary;

    document.getElementById("sgCount").innerText =
        summary.total_sgs || 0;

    document.getElementById("findingCount").innerText =
        summary.total_findings || 0;

    document.getElementById("criticalCount").innerText =
        summary.CRITICAL || 0;

    document.getElementById("highCount").innerText =
        summary.HIGH || 0;

    document.getElementById("mediumCount").innerText =
        summary.MEDIUM || 0;

    document.getElementById("lowCount").innerText =
        summary.LOW || 0;

    updateRisk(summary);

    populateTable(data.findings);

    drawCharts(summary, data.findings);

    // Display AI Security Assessment
    const aiSummary = document.getElementById("aiSummary");

    if (aiSummary) {
        aiSummary.innerText =
            data.ai_summary || "No AI security assessment available.";
    }

}

// ----------------------------
// Risk
// ----------------------------

function updateRisk(summary){

    let score="LOW";
    let cls="text-success";

    if((summary.CRITICAL||0)>0){

        score="CRITICAL";
        cls="text-danger";

    }else if((summary.HIGH||0)>0){

        score="HIGH";
        cls="text-warning";

    }else if((summary.MEDIUM||0)>0){

        score="MEDIUM";
        cls="text-primary";

    }

    const risk=document.getElementById("riskScore");

    risk.innerText=score;
    risk.className=cls;

}

// ----------------------------
// Table
// ----------------------------

function populateTable(findings){

    const tbody = document.getElementById("findingsBody");

    tbody.innerHTML = "";

    findings.forEach(f => {

        let badge = "";

        switch (f.severity){

            case "CRITICAL":
                badge = '<span class="badge bg-danger">CRITICAL</span>';
                break;

            case "HIGH":
                badge = '<span class="badge bg-warning text-dark">HIGH</span>';
                break;

            case "MEDIUM":
                badge = '<span class="badge bg-info text-dark">MEDIUM</span>';
                break;

            default:
                badge = '<span class="badge bg-success">LOW</span>';
        }

        tbody.innerHTML += `
        <tr>

            <td>${badge}</td>

            <td>${f.sg_name || "-"}</td>

            <td>${f.category || "-"}</td>

            <td>${f.region || "-"}</td>

            <td>${f.title || "-"}</td>

            <td>${f.remediation || "-"}</td>

        </tr>
        `;

    });

}

// ----------------------------
// Charts
// ----------------------------

function drawCharts(summary,findings){

    // Severity

    const sevCtx=document.getElementById("severityChart");

    if(severityChart){

        severityChart.destroy();

    }

    severityChart=new Chart(sevCtx,{

        type:"doughnut",

        data:{

            labels:["Critical","High","Medium","Low"],

            datasets:[{

                data:[
                    summary.CRITICAL||0,
                    summary.HIGH||0,
                    summary.MEDIUM||0,
                    summary.LOW||0
                ]

            }]

        }

    });

    // Category

    const categories={};

    findings.forEach(f=>{

        categories[f.category]=(categories[f.category]||0)+1;

    });

    const catCtx=document.getElementById("categoryChart");

    if(categoryChart){

        categoryChart.destroy();

    }

    categoryChart=new Chart(catCtx,{

        type:"bar",

        data:{

            labels:Object.keys(categories),

            datasets:[{

                label:"Findings",

                data:Object.values(categories)

            }]

        }

    });

}

// ----------------------------
// Search
// ----------------------------

const search=document.getElementById("searchBox");

if(search){

search.addEventListener("keyup",function(){

const filter=this.value.toLowerCase();

const rows=document.querySelectorAll("#findingsBody tr");

rows.forEach(r=>{

r.style.display=r.innerText.toLowerCase().includes(filter)?"":"none";

});

});

}
