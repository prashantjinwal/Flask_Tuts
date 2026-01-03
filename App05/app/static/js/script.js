
setTimeout(() => {
    document.querySelectorAll(".flash").forEach(flash => {
        flash.style.opacity = "0";
        setTimeout(() => flash.remove(), 500);
    });
}, 3000);


document.querySelectorAll(".clear-btn").forEach(btn => {
    btn.addEventListener("click", (e) => {
        if (!confirm("Are you sure you want to clear all tasks?")) {
            e.preventDefault();
        }
    });
});
