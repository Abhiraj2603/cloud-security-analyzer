async function loadS3() {

    try {

        const response = await fetch("/api/s3");
        const data = await response.json();

        const summary = data.summary || {};
        const inventory = data.inventory || [];
        const findings = data.findings || [];

        // =========================
        // Summary Cards
        // =========================

        document.getElementById("totalBuckets").innerText =
            summary.total_buckets || 0;

        document.getElementById("publicBuckets").innerText =
            summary.public_buckets || 0;

        document.getElementById("encryptedBuckets").innerText =
            summary.encrypted_buckets || 0;

        document.getElementById("totalFindings").innerText =
            summary.total_findings || 0;

        // =========================
        // Inventory Table
        // =========================

        const inventoryTable =
            document.getElementById("inventoryTable");

        inventoryTable.innerHTML = "";

        inventory.forEach(bucket => {

            inventoryTable.innerHTML += `

            <tr>

                <td>${bucket.name}</td>

                <td>
                    ${bucket.public
                        ? '<span class="badge bg-danger">Public</span>'
                        : '<span class="badge bg-success">Private</span>'}
                </td>

                <td>
                    ${bucket.encryption
                        ? '<span class="badge bg-success">Enabled</span>'
                        : '<span class="badge bg-danger">Disabled</span>'}
                </td>

                <td>
                    ${bucket.versioning
                        ? '<span class="badge bg-success">Enabled</span>'
                        : '<span class="badge bg-warning text-dark">Disabled</span>'}
                </td>

                <td>
                    ${bucket.logging
                        ? '<span class="badge bg-success">Enabled</span>'
                        : '<span class="badge bg-secondary">Disabled</span>'}
                </td>

                <td>
                    ${bucket.lifecycle
                        ? '<span class="badge bg-success">Enabled</span>'
                        : '<span class="badge bg-secondary">Disabled</span>'}
                </td>

            </tr>

            `;

        });

        // =========================
        // Findings Table
        // =========================

        const findingsTable =
            document.getElementById("findingsTable");

        findingsTable.innerHTML = "";

        findings.forEach(finding => {

            let badge = "secondary";

            switch (finding.severity) {

                case "CRITICAL":
                    badge = "danger";
                    break;

                case "HIGH":
                    badge = "warning";
                    break;

                case "MEDIUM":
                    badge = "info";
                    break;

                case "LOW":
                    badge = "secondary";
                    break;
            }

            findingsTable.innerHTML += `

            <tr>

                <td>
                    <span class="badge bg-${badge}">
                        ${finding.severity}
                    </span>
                </td>

                <td>${finding.category}</td>

                <td>${finding.resource}</td>

                <td>${finding.detail}</td>

                <td>${finding.remediation}</td>

            </tr>

            `;

        });

    }
    catch (err) {

        console.error(err);

        alert("Unable to load S3 data.");

    }

}

// =========================
// Refresh Button
// =========================

document
    .getElementById("refreshBtn")
    .addEventListener("click", loadS3);

// =========================
// Search
// =========================

document
    .getElementById("searchInput")
    .addEventListener("keyup", function () {

        const value = this.value.toLowerCase();

        document
            .querySelectorAll("#inventoryTable tr")
            .forEach(row => {

                row.style.display =
                    row.innerText.toLowerCase().includes(value)
                        ? ""
                        : "none";

            });

    });

// =========================
// Initial Load
// =========================

loadS3();
