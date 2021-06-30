function disableScenarioSeedBox() {
    const random_scenario = document.getElementById("random-scenario");
    const txt_random_seed = document.getElementById("random-seed");
    txt_random_seed.disabled = random_scenario.checked ? false : true;
    if (!txt_random_seed.disabled) {
        txt_random_seed.focus();
    }
}
function disablePatientIDBox() {
    const custom_patientID_chkbox = document.getElementById("custom-patientID-chkbox");
    const custom_patientID_input = document.getElementById("custom-patientID-input");
    const all_adolescents = document.getElementById("all-adolescents")
    const all_adults = document.getElementById("all-adults")
    const all_children = document.getElementById("all-children")
    custom_patientID_input.disabled = custom_patientID_chkbox.checked ? false : true;
    if (!custom_patientID_input.disabled) {
        custom_patientID_input.focus();
        all_adolescents.disabled = true
        all_adults.disabled = true
        all_children.disabled = true
    } else {
        all_adolescents.disabled = false
        all_adults.disabled = false
        all_children.disabled = false
    }
}

function disablePathBox() {
    const custom_path_radio = document.getElementById("custom-path-radio");
    const custom_path_input= document.getElementById("custom-path-input");
    custom_path_input.disabled = custom_path_radio.checked ? false : true;
    if (custom_path_input.disabled) {
        custom_path_input.focus();
    }
}