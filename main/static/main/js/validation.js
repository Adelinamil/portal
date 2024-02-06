let delayTimer;
const numberRegex = /^(([АВЕКМНОРСТУХ]\d{3}[АВЕКМНОРСТУХ]{1,2})(\d{2,3})|(\d{4}[АВЕКМНОРСТУХ]{2})(\d{2})|(\d{3}C?D{1,2}\d{3})(\d{2})|([АВЕКМНОРСТУХ]{2}\d{3}[АВЕКМНОРСТУХ])(\d{2})|([АВЕКМНОРСТУХ]\d{4})(\d{2})|(\d{3}[АВЕКМНОРСТУХ])(\d{2})|(\d{4}[АВЕКМНОРСТУХ])(\d{2}))$/i;

const addError = (id, message, detail) => {
    if (document.getElementById(`error_${id}_${detail}`) !== null) {
        return;
    }

    const divElement = document.getElementById("div_" + id);
    const pElement = document.createElement("p");
    pElement.id = `error_${id}_${detail}`
    pElement.className = "text-danger invalid-feedback";
    pElement.innerHTML = '<strong>' + message + '</strong>';

    const helpText = document.getElementById(id + "_helptext");
    if (divElement.innerText.includes(message)) return;

    if (helpText !== null) {
        divElement.insertBefore(pElement, helpText);
    } else {
        divElement.appendChild(pElement);
    }
};

const removeError = (id, detail) => {
    const pElement = document.getElementById(`error_${id}_${detail}`);
    if (pElement === null) {
        return;
    }
    pElement.remove();
};

const validateRegex = (id, regex, errorMessage) => {
    const elementInput = document.getElementById(id);
    if (elementInput.value !== "") {
        if (!regex.test(elementInput.value)) {
            elementInput.classList.remove("is-valid");
            elementInput.classList.add("is-invalid");
            elementInput.setCustomValidity("Неверный формат");
            addError(id, errorMessage, "format");
            return true;
        } else {
            elementInput.classList.remove("is-invalid");
            elementInput.setCustomValidity("");
            removeError(id, "format");
            return false;
        }
    } else {
        elementInput.classList.remove("is-invalid");
        elementInput.setCustomValidity("");
        removeError(id, "format");
        return false;
    }
};

const checkViolationForm = (withoutDelay = false) => {
    const vehicleNumber = document.getElementById("id_vehicle_number");
    const description = document.getElementById("id_description");
    const btn = document.getElementById("saveViolationBtn");
    if (withoutDelay) {
        btn.disabled = vehicleNumber.value === "" || description.value === "";
        return;
    }

    if (delayTimer) clearTimeout(delayTimer);
    delayTimer = setTimeout(() => {
        const answer = validateRegex(
            "id_vehicle_number", numberRegex, "Регистрационный номер не соответствует формату"
        );
        btn.disabled = vehicleNumber.value === "" || description.value === "" || answer;
    }, 750);
};