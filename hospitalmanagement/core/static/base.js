console.log("Working");

// Edit slot
document.querySelectorAll(".edit-slot").forEach(btn => {
    btn.addEventListener("click", function (e) {
        e.preventDefault();

        const row = this.closest("tr");
        const text = row.querySelector(".slot-text");
        const form = row.querySelector(".sloteditform");
        const actions = row.querySelectorAll(".edit-slot, .delete-slot");

        // Hide text & action buttons, show form
        text.style.display = "none";
        actions.forEach(b => b.style.display = "none");
        form.classList.remove("hidden");

        // Focus first input
        const startInput = form.querySelector('[name="starttime"]');
        startInput.focus();
        startInput.select();
    });
});

// Cancel edit on focus out
document.querySelectorAll(".sloteditform").forEach(form => {
    form.addEventListener("focusout", function () {
        setTimeout(() => {
            if (!form.contains(document.activeElement)) {
                const row = form.closest("tr");
                const text = row.querySelector(".slot-text");
                const actions = row.querySelectorAll(".edit-slot, .delete-slot");

                // Restore text & buttons, hide form
                form.classList.add("hidden");
                text.style.display = "inline";
                actions.forEach(b => b.style.display = "inline-block");
            }
        }, 150);
    });
});

// Submit form on Enter key (since submit button is hidden)
document.querySelectorAll("#sloteditform").forEach(form => {
    form.addEventListener("keydown", function (e) {
        if (e.key === "Enter") {
            e.preventDefault();
            form.submit();
        }
    });
});



// Add time slot
const createBtn = document.getElementById("startslotcreation");
const cancelBtn = document.getElementById("cancelslotcreation");

if(createBtn && cancelBtn){
    createBtn.addEventListener("click", function(){
        const slotcreateform = document.getElementById("slotcreateform");

        slotcreateform.classList.remove("hidden");
        createBtn.classList.add("hidden");
        cancelBtn.classList.remove("hidden");
    });

    cancelBtn.addEventListener("click", function(){
        const slotcreateform = document.getElementById("slotcreateform");

        slotcreateform.classList.add("hidden");
        createBtn.classList.remove("hidden");
        cancelBtn.classList.add("hidden");
    });
}