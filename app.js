// ============================================================
// SMARTMEET
// Frontend JavaScript
// ============================================================


// ------------------------------------------------------------
// GLOBAL DATA
// ------------------------------------------------------------

const schedules = {};


// ------------------------------------------------------------
// SHORTCUT FOR GETTING HTML ELEMENTS
// ------------------------------------------------------------

function $(id) {
    return document.getElementById(id);
}


// ------------------------------------------------------------
// TOAST MESSAGE
// ------------------------------------------------------------

function showToast(message) {

    const toast = $("toast");

    if (!toast) {
        alert(message);
        return;
    }

    toast.textContent = message;

    toast.classList.add("show");

    clearTimeout(window.smartMeetToastTimer);

    window.smartMeetToastTimer = setTimeout(
        function () {
            toast.classList.remove("show");
        },
        2500
    );
}


// ------------------------------------------------------------
// TIME VALIDATION
// ------------------------------------------------------------

function isValidTime(time) {

    const pattern = /^([01]\d|2[0-3]):[0-5]\d$/;

    return pattern.test(time);
}


// ------------------------------------------------------------
// CONVERT HH:MM TO MINUTES
// ------------------------------------------------------------

function timeToMinutes(time) {

    const parts = time.split(":");

    const hours = Number(parts[0]);
    const minutes = Number(parts[1]);

    return (
        hours * 60 +
        minutes
    );
}


// ------------------------------------------------------------
// ADD PARTICIPANT SCHEDULE
// ------------------------------------------------------------

function addSchedule() {

    const name = $("participant").value.trim();

    const start = $("busyStart").value.trim();

    const end = $("busyEnd").value.trim();


    // Check empty fields

    if (
        name === "" ||
        start === "" ||
        end === ""
    ) {

        showToast(
            "Please fill in all schedule fields."
        );

        return;
    }


    // Validate time format

    if (
        !isValidTime(start) ||
        !isValidTime(end)
    ) {

        showToast(
            "Please use HH:MM format. Example: 09:30"
        );

        return;
    }


    // Validate time order

    if (
        timeToMinutes(start) >=
        timeToMinutes(end)
    ) {

        showToast(
            "Busy start time must be before busy end time."
        );

        return;
    }


    // Create participant if necessary

    if (!schedules[name]) {

        schedules[name] = [];
    }


    // Add interval

    schedules[name].push([
        start,
        end
    ]);


    // Clear inputs

    $("participant").value = "";

    $("busyStart").value = "";

    $("busyEnd").value = "";


    // Update interface

    renderSchedules();

    clearResults();


    // Focus participant field

    $("participant").focus();


    showToast(
        `Added ${name}'s schedule.`
    );
}


// ------------------------------------------------------------
// REMOVE ONE SCHEDULE
// ------------------------------------------------------------

function removeSchedule(
    participantName,
    scheduleIndex
) {

    if (
        !schedules[participantName]
    ) {

        return;
    }


    schedules[participantName].splice(
        scheduleIndex,
        1
    );


    // Remove participant if no schedules remain

    if (
        schedules[participantName].length === 0
    ) {

        delete schedules[participantName];
    }


    renderSchedules();

    clearResults();

    showToast(
        "Schedule removed."
    );
}


// ------------------------------------------------------------
// CLEAR ALL SCHEDULES
// ------------------------------------------------------------

function clearAll() {

    const participantNames =
        Object.keys(schedules);


    if (
        participantNames.length === 0
    ) {

        showToast(
            "There are no schedules to clear."
        );

        return;
    }


    const confirmed = confirm(
        "Are you sure you want to remove all schedules?"
    );


    if (!confirmed) {

        return;
    }


    participantNames.forEach(
        function (name) {

            delete schedules[name];
        }
    );


    renderSchedules();

    clearResults();

    showToast(
        "All schedules have been cleared."
    );
}


// ------------------------------------------------------------
// DISPLAY SCHEDULES
// ------------------------------------------------------------

function renderSchedules() {

    const tableBody =
        $("scheduleBody");


    tableBody.innerHTML = "";


    let totalSchedules = 0;


    Object.entries(schedules).forEach(
        function ([name, intervals]) {

            intervals.forEach(
                function ([start, end], index) {

                    totalSchedules++;


                    const row =
                        document.createElement("tr");


                    // Participant cell

                    const participantCell =
                        document.createElement("td");

                    const strong =
                        document.createElement("strong");

                    strong.textContent = name;

                    participantCell.appendChild(
                        strong
                    );


                    // Start cell

                    const startCell =
                        document.createElement("td");

                    startCell.textContent =
                        start;


                    // End cell

                    const endCell =
                        document.createElement("td");

                    endCell.textContent =
                        end;


                    // Remove cell

                    const removeCell =
                        document.createElement("td");

                    removeCell.style.textAlign =
                        "right";


                    const removeButton =
                        document.createElement("button");

                    removeButton.className =
                        "remove-row";

                    removeButton.textContent =
                        "Remove";


                    removeButton.addEventListener(
                        "click",
                        function () {

                            removeSchedule(
                                name,
                                index
                            );
                        }
                    );


                    removeCell.appendChild(
                        removeButton
                    );


                    row.appendChild(
                        participantCell
                    );

                    row.appendChild(
                        startCell
                    );

                    row.appendChild(
                        endCell
                    );

                    row.appendChild(
                        removeCell
                    );


                    tableBody.appendChild(
                        row
                    );
                }
            );
        }
    );


    // Empty state

    if (
        totalSchedules === 0
    ) {

        const row =
            document.createElement("tr");

        row.className =
            "empty-row";


        const cell =
            document.createElement("td");

        cell.colSpan = 4;

        cell.textContent =
            "Add schedules or load demo data.";


        row.appendChild(cell);

        tableBody.appendChild(row);
    }


    // Update counters

    const participantCount =
        Object.keys(schedules).length;


    $("participantCount").textContent =
        participantCount;


    $("scheduleCount").textContent =
        `${totalSchedules} schedule${
            totalSchedules === 1
                ? ""
                : "s"
        }`;
}


// ------------------------------------------------------------
// LOAD DEMO DATA
// ------------------------------------------------------------

function loadDemoData() {

    // Clear old data

    Object.keys(schedules).forEach(
        function (name) {

            delete schedules[name];
        }
    );


    // Demo participant 1

    schedules["Alice"] = [
        ["09:00", "10:00"],
        ["13:00", "14:00"]
    ];


    // Demo participant 2

    schedules["Bob"] = [
        ["09:30", "11:00"],
        ["14:00", "15:00"]
    ];


    // Demo participant 3

    schedules["Charlie"] = [
        ["10:00", "11:30"]
    ];


    // Demo participant 4

    schedules["David"] = [
        ["12:30", "13:30"],
        ["16:00", "16:30"]
    ];


    renderSchedules();


    showToast(
        "Demo data loaded."
    );


    // Automatically calculate

    findCommonTime(false);
}


// ------------------------------------------------------------
// FIND COMMON MEETING TIME
// ------------------------------------------------------------

async function findCommonTime(
    showMessage = true
) {

    // Check schedules

    if (
        Object.keys(schedules).length === 0
    ) {

        showToast(
            "Please add at least one participant schedule."
        );

        return;
    }


    // Get values

    const workStart =
        $("workStart").value.trim();

    const workEnd =
        $("workEnd").value.trim();

    const duration =
        Number(
            $("duration").value
        );


    // Validate working hours

    if (
        !isValidTime(workStart) ||
        !isValidTime(workEnd)
    ) {

        showToast(
            "Working hours must use HH:MM format."
        );

        return;
    }


    // Validate working time order

    if (
        timeToMinutes(workStart) >=
        timeToMinutes(workEnd)
    ) {

        showToast(
            "Working start must be before working end."
        );

        return;
    }


    // Validate duration

    if (
        !Number.isInteger(duration) ||
        duration <= 0
    ) {

        showToast(
            "Meeting duration must be a positive number."
        );

        return;
    }


    // Prepare API data

    const requestData = {

        schedules: schedules,

        work_start: workStart,

        work_end: workEnd,

        duration: duration
    };


    try {

        // Change button state

        const findButton =
            $("findBtn");

        findButton.disabled = true;

        findButton.textContent =
            "Finding...";


        // Call Flask backend

        const response =
            await fetch(
                "/api/find-time",
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body:
                        JSON.stringify(
                            requestData
                        )
                }
            );


        // Convert response to JSON

        const result =
            await response.json();


        // Check server response

        if (
            !response.ok ||
            !result.success
        ) {

            throw new Error(
                result.error ||
                "Unable to calculate meeting time."
            );
        }


        // Display results

        displayResults(
            result
        );


        if (showMessage) {

            showToast(
                `Found ${
                    result.meeting_slots.length
                } possible meeting slot(s).`
            );
        }

    } catch (error) {

        console.error(
            "SMARTMEET Error:",
            error
        );


        showToast(
            error.message
        );

    } finally {

        const findButton =
            $("findBtn");


        findButton.disabled =
            false;


        findButton.textContent =
            "Find Common Time";
    }
}


// ------------------------------------------------------------
// DISPLAY RESULTS
// ------------------------------------------------------------

function displayResults(
    result
) {

    const commonIntervals =
        result.common_intervals || [];


    const meetingSlots =
        result.meeting_slots || [];


    // Update counters

    $("commonCount").textContent =
        commonIntervals.length;


    $("slotCount").textContent =
        meetingSlots.length;


    // --------------------------------------------------------
    // COMMON INTERVALS
    // --------------------------------------------------------

    const commonGrid =
        $("commonGrid");


    commonGrid.innerHTML = "";


    if (
        commonIntervals.length === 0
    ) {

        const message =
            document.createElement("div");

        message.className =
            "result-placeholder";

        message.textContent =
            "No common available time was found.";


        commonGrid.appendChild(
            message
        );

    } else {

        commonIntervals.forEach(
            function (interval) {

                const card =
                    document.createElement("div");

                card.className =
                    "common-card";


                const time =
                    document.createElement("strong");

                time.textContent =
                    `${interval.start} - ${interval.end}`;


                const duration =
                    document.createElement("span");

                duration.textContent =
                    `${interval.duration} minutes available`;


                card.appendChild(time);

                card.appendChild(duration);


                commonGrid.appendChild(
                    card
                );
            }
        );
    }


    // --------------------------------------------------------
    // MEETING SLOTS
    // --------------------------------------------------------

    const slotsGrid =
        $("slotsGrid");


    slotsGrid.innerHTML = "";


    if (
        meetingSlots.length === 0
    ) {

        const message =
            document.createElement("div");

        message.className =
            "result-placeholder";

        message.textContent =
            "No meeting slots are available for the selected duration.";


        slotsGrid.appendChild(
            message
        );

    } else {

        meetingSlots.forEach(
            function (slot) {

                const button =
                    document.createElement("button");

                button.className =
                    "slot-btn";


                button.textContent =
                    `${slot.start} - ${slot.end}`;


                button.addEventListener(
                    "click",
                    function () {

                        selectMeetingSlot(
                            slot.start,
                            slot.end
                        );
                    }
                );


                slotsGrid.appendChild(
                    button
                );
            }
        );
    }


    // Reset selected slot

    $("selectedSlot").textContent =
        "No meeting slot selected";


    $("selectedSlot").classList.remove(
        "active"
    );
}


// ------------------------------------------------------------
// SELECT A MEETING SLOT
// ------------------------------------------------------------

function selectMeetingSlot(
    start,
    end
) {

    const selected =
        $("selectedSlot");


    selected.textContent =
        `✓ Selected Meeting Slot: ${start} - ${end}`;


    selected.classList.add(
        "active"
    );


    showToast(
        `Selected ${start} - ${end}`
    );
}


// ------------------------------------------------------------
// CLEAR RESULTS
// ------------------------------------------------------------

function clearResults() {

    $("commonCount").textContent =
        "0";


    $("slotCount").textContent =
        "0";


    $("commonGrid").innerHTML = `
        <div class="result-placeholder">
            Run the algorithm to see common availability.
        </div>
    `;


    $("slotsGrid").innerHTML = `
        <div class="result-placeholder">
            Your meeting slots will appear here.
        </div>
    `;


    $("selectedSlot").textContent =
        "No meeting slot selected";


    $("selectedSlot").classList.remove(
        "active"
    );
}


// ------------------------------------------------------------
// RESET SETTINGS
// ------------------------------------------------------------

function resetSettings() {

    $("workStart").value =
        "09:00";


    $("workEnd").value =
        "17:00";


    $("duration").value =
        "30";


    clearResults();


    showToast(
        "Settings reset."
    );
}


// ------------------------------------------------------------
// KEYBOARD SUPPORT
// ------------------------------------------------------------

function setupKeyboardEvents() {

    $("busyEnd").addEventListener(
        "keydown",
        function (event) {

            if (
                event.key === "Enter"
            ) {

                addSchedule();
            }
        }
    );


    $("participant").addEventListener(
        "keydown",
        function (event) {

            if (
                event.key === "Enter"
            ) {

                addSchedule();
            }
        }
    );
}


// ------------------------------------------------------------
// BUTTON EVENTS
// ------------------------------------------------------------

function setupButtons() {

    $("addBtn").addEventListener(
        "click",
        addSchedule
    );


    $("clearBtn").addEventListener(
        "click",
        clearAll
    );


    $("demoBtn").addEventListener(
        "click",
        loadDemoData
    );


    $("findBtn").addEventListener(
        "click",
        function () {

            findCommonTime(true);
        }
    );


    $("resetBtn").addEventListener(
        "click",
        resetSettings
    );
}


// ------------------------------------------------------------
// INITIALIZE APPLICATION
// ------------------------------------------------------------

function initializeSmartMeet() {

    setupButtons();

    setupKeyboardEvents();

    renderSchedules();

    clearResults();
}


// ------------------------------------------------------------
// START APPLICATION
// ------------------------------------------------------------

document.addEventListener(
    "DOMContentLoaded",
    initializeSmartMeet
);