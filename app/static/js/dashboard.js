document.addEventListener("DOMContentLoaded", () => {

    const button = document.getElementById("scanButton");
    const status = document.getElementById("status");

    button.addEventListener("click", async () => {

        button.disabled = true;
        button.innerHTML = "Scanning...";

        status.className = "alert alert-info";
        status.innerHTML = "Scanning AWS...";

        try {

            const response = await fetch("/api/scan", {
                method: "POST"
            });

            const result = await response.json();

            if (!result.success) {

                status.className = "alert alert-danger";
                status.innerHTML = result.error;

                button.disabled = false;
                button.innerHTML = "Scan AWS";

                return;
            }

            const summary = result.data.summary;

            document.getElementById("total-sgs").innerHTML =
                summary.total_sgs;

            document.getElementById("total-findings").innerHTML =
                summary.total_findings;

            document.getElementById("critical").innerHTML =
                summary.by_severity.CRITICAL || 0;

            document.getElementById("high").innerHTML =
                summary.by_severity.HIGH || 0;

            document.getElementById("medium").innerHTML =
                summary.by_severity.MEDIUM || 0;

            document.getElementById("low").innerHTML =
                summary.by_severity.LOW || 0;

            const tbody =
                document.getElementById("findings-table");

            tbody.innerHTML = "";

            result.data.findings.forEach(finding => {

                tbody.innerHTML += `
                    <tr>
                        <td>${finding.severity}</td>
                        <td>${finding.sg_name}</td>
                        <td>${finding.category}</td>
                        <td>${finding.region}</td>
                        <td>${finding.title}</td>
                    </tr>
                `;

            });

            status.className = "alert alert-success";
            status.innerHTML = "Scan completed successfully.";

        }

        catch (err) {

            status.className = "alert alert-danger";
            status.innerHTML = err;

        }

        button.disabled = false;
        button.innerHTML = "Scan AWS";

    });

});
