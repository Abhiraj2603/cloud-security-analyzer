document.addEventListener("DOMContentLoaded", function () {

    const pdfBtn = document.getElementById("pdfBtn");
    const excelBtn = document.getElementById("excelBtn");

    if (pdfBtn) {
        pdfBtn.addEventListener("click", function () {
            window.location.href = "/download/pdf";
        });
    }

    if (excelBtn) {
        excelBtn.addEventListener("click", function () {
            window.location.href = "/download/excel";
        });
    }

});
