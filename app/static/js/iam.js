async function loadIAM() {

    try {

        const response = await fetch("/api/iam");

        const data = await response.json();

        const summary = data.summary;
        const findings = data.findings;

        // ======================
        // Summary Cards
        // ======================

        document.getElementById("totalUsers").innerText =
            summary.total_users || 0;

        document.getElementById("totalRoles").innerText =
            summary.total_roles || 0;

        document.getElementById("totalGroups").innerText =
            summary.total_groups || 0;

        document.getElementById("totalFindings").innerText =
            summary.total_findings || 0;

        document.getElementById("mfaDisabled").innerText =
            summary.mfa_disabled || 0;

        document.getElementById("adminUsers").innerText =
            summary.admin_users || 0;

        document.getElementById("rootKeys").innerText =
            summary.root_keys || 0;

        document.getElementById("oldAccessKeys").innerText =
            summary.old_access_keys || 0;

        // ======================
        // Table
        // ======================

        const tbody = document.getElementById("iamTableBody");

        tbody.innerHTML = "";

        if (findings.length === 0) {

            tbody.innerHTML = `
                <tr>
                    <td colspan="5" class="text-center py-4">
                        No Findings
                    </td>
                </tr>
            `;

            return;
        }

        findings.forEach(finding => {

            let badge = "bg-success";

            if (finding.severity === "CRITICAL")
                badge = "bg-danger";

            else if (finding.severity === "HIGH")
                badge = "bg-warning text-dark";

            else if (finding.severity === "MEDIUM")
                badge = "bg-info";

            else if (finding.severity === "LOW")
                badge = "bg-success";

            tbody.innerHTML += `

            <tr>

                <td>
                    <span class="badge ${badge}">
                        ${finding.severity}
                    </span>
                </td>

                <td>${finding.category}</td>

                <td>${finding.resource}</td>

                <td>${finding.title}</td>

                <td>${finding.remediation}</td>

            </tr>

            `;

        });

    }

    catch (err) {

        console.error(err);

    }

}

// Refresh

document
.getElementById("refreshBtn")
.addEventListener("click", loadIAM);

// Search

document
.getElementById("searchInput")
.addEventListener("keyup", function () {

    let value = this.value.toLowerCase();

    let rows = document.querySelectorAll("#iamTableBody tr");

    rows.forEach(row => {

        row.style.display =
            row.innerText.toLowerCase().includes(value)
            ? ""
            : "none";

    });

});

// Initial Load

loadIAM();
