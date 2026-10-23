
 // ===== 1. Find the elements we need =====
const membersInput = document.getElementById("members");
const memberDetails = document.getElementById("member-details");

// ===== 2. A function that builds ONE member block =====
function createMemberBlock(number) {
    const block = document.createElement("div");
    block.className = "member-block";

    block.innerHTML = `
        <h4>Member ${number}</h4>

        <div class="field">
            <label for="member-name-${number}">Name:</label>
            <input type="text" id="member-name-${number}" name="member_name" required>
        </div>

        <div class="field">
            <label for="member-age-${number}">Age:</label>
            <input type="number" id="member-age-${number}" name="member_age" min="0" max="100" required>
        </div>

        <div class="field">
            <label for="member-diet-${number}">Diet:</label>
            <select id="member-diet-${number}" name="member_diet" required>
                <option value="">-- Select --</option>
                <option value="veg">Vegetarian</option>
                <option value="vegan">Vegan</option>
                <option value="non-veg">Non-Vegetarian</option>
                <option value="egg">Eggetarian</option>
                <option value="others">Others</option>
            </select>
        </div>
    `;

    return block;
}

// ===== 3. Make the page match the number of members =====
function updateMemberBlocks(allowShrink) {
    if (membersInput.value === "") return;

    let count = parseInt(membersInput.value);

    if (isNaN(count) || count < 0) count = 0;
    if (count > 20) count = 20;

    while (memberDetails.children.length < count) {
        const nextNumber = memberDetails.children.length + 1;
        memberDetails.appendChild(createMemberBlock(nextNumber));
    }

    if (allowShrink) {
        while (memberDetails.children.length > count) {
            memberDetails.removeChild(memberDetails.lastElementChild);
        }
    }
}

// ===== 4. Add blocks while typing; remove them when finished =====
membersInput.addEventListener("input", function () {
    updateMemberBlocks(false);
});

membersInput.addEventListener("change", function () {
    updateMemberBlocks(true);
});

// ===== 5. Initialize member blocks =====
updateMemberBlocks(true);

// ===== 6. Reusable add-on checkbox and notes toggle =====
function linkToggle(checkboxId, noteId) {
    const checkbox = document.getElementById(checkboxId);
    const notes = document.getElementById(noteId);

    function updateVisibility() {
        notes.hidden = !checkbox.checked;
    }

    checkbox.addEventListener("change", updateVisibility);

    updateVisibility();
}

// ===== 7. Connect all five add-ons =====
linkToggle("ad-cake", "cake-notes");
linkToggle("ad-bev", "bevs");
linkToggle("ad-gift", "presents");
linkToggle("ad-photo", "shoots");
linkToggle("soundtrack", "music");



/* ===== 8. Private dome capacity check ===== */

const form = document.getElementById("reservation-form");

form.addEventListener("submit", function (event) {
    const dining = document.querySelector(
        'input[name="dining"]:checked'
    );

    const memberCount = document.querySelectorAll(
        "#member-details .member-block"
    ).length;

    const totalGuests = 1 + memberCount;

    if (
        dining &&
        dining.value.startsWith("private-") &&
        totalGuests > 4
    ) {
        event.preventDefault();

        alert(
            "Private domes allow a maximum of 4 guests, including the booker."
        );
    }
});


/* ===== 9. Swimming pool waiver ===== */

const poolCheckbox = document.querySelector(
    'input[name="services"][value="swimming-pool"]'
);

const poolWaiver = document.querySelector(
    'input[name="pool_waiver"]'
);

function updatePoolWaiver() {
    if (!poolCheckbox || !poolWaiver) return;

    poolWaiver.required = poolCheckbox.checked;

    if (!poolCheckbox.checked) {
        poolWaiver.checked = false;
    }
}

if (poolCheckbox && poolWaiver) {
    poolCheckbox.addEventListener("change", updatePoolWaiver);
    updatePoolWaiver();
}


/* ===== 10. Age validation ===== */

form.addEventListener("submit", function (event) {
    const ageInput = form.querySelector('[name="age"]');
    const bookerAge = Number(ageInput?.value);

    const beverageCheckbox = document.getElementById("ad-bev");

    if (
        !ageInput ||
        ageInput.value.trim() === "" ||
        !Number.isInteger(bookerAge) ||
        bookerAge < 18
    ) {
        event.preventDefault();
        alert("The person making the booking must be at least 18.");
        return;
    }

    if (beverageCheckbox?.checked && bookerAge < 21) {
        event.preventDefault();
        alert("The person booking must be at least 21 for beverage upgrades.");
        return;
    }

    const memberAges = document.querySelectorAll(
        '#member-details input[name="member_age"]'
    );

    for (let i = 0; i < memberAges.length; i++) {
        const age = Number(memberAges[i].value);

        if (
            memberAges[i].value.trim() === "" ||
            !Number.isInteger(age) ||
            age < 0 ||
            age > 100
        ) {
            event.preventDefault();
            alert(`Please enter a valid age for Member ${i + 1}.`);
            return;
        }
    }
});
