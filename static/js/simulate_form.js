// const option_head = document.createElement("option");
// const option_head_text = document.createTextNode("Select start time");
// const option_head_selected = document.createAttribute("selected");
// option_head.appendChild(option_head_text);
// option_head.setAttributeNode(option_head_selected);

const select_time_element = document.getElementById("start-time-hour");
// select_time_element.appendChild(option_head);
for (let i = 1; i <= 12; i++) {
  const option = document.createElement("option");
  const option_text = document.createTextNode(`${i}:00`);
  const option_text_value = document.createAttribute("value");
  option_text_value.value = `${i}:00`;
  option.appendChild(option_text);
  option.setAttributeNode(option_text_value);
  select_time_element.appendChild(option);
}

const select_period_element = document.getElementById("start-time-period");
// select_period_element.appendChild(option_head_text);
const period_list = ["AM", "PM"];
for (let item of period_list) {
  const option = document.createElement("option");
  const option_text = document.createTextNode(item);
  const option_text_value = document.createAttribute("value");
  option_text_value.value = item;
  option.appendChild(option_text);
  option.setAttributeNode(option_text_value);
  select_period_element.appendChild(option);
}

function hideCustomScenario() {
  const random_seed_div = document.querySelector(".random-scenario-seed");
  const custom_scenario_chkbox = document.getElementById(
    "custom-scenario-chkbox"
  );
  const custom_scenario_detail = document.getElementsByClassName(
    "custom-scenario-detail"
  );
  const meal_time = ["breakfast", "lunch", "dinner", "snack"];
  if (custom_scenario_chkbox.checked) {
    random_seed_div.style.display = "none";
    random_seed_div.disabled = true;
    custom_scenario_detail[0].style.display = "flex";

    for (let item of meal_time) {
      const select_time_element = document.getElementById(`${item}-time`);
      for (let i = 1; i <= 12; i++) {
        const option = document.createElement("option");
        const option_text = document.createTextNode(`${i}:00`);
        const option_text_value = document.createAttribute("value");
        option_text_value.value = `${i}:00`;
        option.appendChild(option_text);
        option.setAttributeNode(option_text_value);
        select_time_element.appendChild(option);
      }

      const select_period_element = document.getElementById(`${item}-period`);
      const period_list = ["AM", "PM"];
      for (let item of period_list) {
        const option = document.createElement("option");
        const option_text = document.createTextNode(item);
        const option_text_value = document.createAttribute("value");
        option_text_value.value = item;
        option.appendChild(option_text);
        option.setAttributeNode(option_text_value);
        select_period_element.appendChild(option);
      }
    }
  } else {
    for (let item of custom_scenario_detail) {
      item.style.display = "none";
      random_seed_div.style.display = "block";
      random_seed_div.disabled = false;
    }
  }
}

function disablePatientIDBox() {
  const custom_patientID_chkbox = document.getElementById(
    "custom-patientID-chkbox"
  );
  const custom_patientID_div_chkbox =
    document.getElementsByClassName("custom-patientID");

  const all_adolescents = document.getElementById("all-adolescents");
  const all_adults = document.getElementById("all-adults");
  const all_children = document.getElementById("all-children");
  if (custom_patientID_chkbox.checked) {
    for (let item of custom_patientID_div_chkbox) {
      item.style.display = "block";
    }
    all_adolescents.disabled = true;
    all_adults.disabled = true;
    all_children.disabled = true;
  } else {
    for (let item of custom_patientID_div_chkbox) {
      item.style.display = "none";
    }
    all_adolescents.disabled = false;
    all_adults.disabled = false;
    all_children.disabled = false;
  }
}

function disablePathBox() {
  const custom_path_radio = document.getElementById("custom-path-radio");
  const custom_path_input = document.getElementById("custom-path-input");
  custom_path_input.disabled = custom_path_radio.checked ? false : true;
  if (custom_path_input.disabled) {
    custom_path_input.focus();
  }
}

// disable the parallel button.
const system_js = system;
function disableParallelRadio() {
  const animate_yes = document.getElementById("with-animation");
  const parallel_yes = document.getElementById("with-parallel");
  if (system_js == "Darwin") {
    parallel_yes.disabled = animate_yes.checked ? true : false;
  }
}

// const form = document.getElementById("simulation-form");
// const form_data = new FormData(form);
// fetch("/simulate", {
//   method: "POST",
//   body: form_data,
// })
//   .then((response) => (data = response.text()))
//   .then((data) => {
//     console.log(data);
//   });
