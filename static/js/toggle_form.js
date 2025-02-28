document.addEventListener("DOMContentLoaded", function () {
    const reportFormContainer = document.getElementById("report-form-container");
    const reportButton = document.getElementById("show-report-form");

    if (reportButton) {
        reportButton.addEventListener("click", function (event) {
            event.preventDefault(); // Prevent default link behavior

            // Toggle form visibility
            if (reportFormContainer.style.display === "none" || reportFormContainer.style.display === "") {
                reportFormContainer.style.display = "block";
            } else {
                reportFormContainer.style.display = "none";
            }
        });
    }
});
