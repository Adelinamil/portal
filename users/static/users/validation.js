const checkUser = async (columnName, columnValue) => {
    let form = new FormData();
    form.append('column_name', columnName);
    form.append('column_value', columnValue);
    const response = await fetch('/users/check_user/', {
        method: 'POST',
        body: form,
        credentials: 'same-origin',
        headers: {"X-CSRFToken": Cookies.get('csrftoken')},
    });
    return (await response.json())['is_taken'];
};

const validateInputWithRequest = async (elementId, columnName, errorMessage, isPhone = false) => {
    let element = document.getElementById(elementId);
    let regButton = document.getElementById("registerButton");
    if (element.value !== "") {
        delayTimer = setTimeout(async () => {
            const value = isPhone ? `7${element.value.replace(/\D/g, '')}` : element.value;
            const isUsernameExists = await checkUser(columnName, value);
            if (isUsernameExists) {
                element.classList.remove("is-valid");
                element.classList.add("is-invalid");
                element.setCustomValidity(errorMessage);
                addError(elementId, errorMessage, "exists");
                regButton.disabled = true;
            } else {
                element.classList.remove("is-invalid");
                element.setCustomValidity("");
                removeError(elementId, "exists");
                regButton.disabled = false;
            }
        }, 500);
    } else {
        element.classList.remove("is-invalid");
        element.setCustomValidity("");
        removeError(elementId, "exists");
        regButton.disabled = false;
    }
};

const validateUsername = async () => {
    clearTimeout(delayTimer);
    await validateInputWithRequest(
        "id_username", "username", "Это имя пользователя уже занято"
    );
};

const validateEmail = async () => {
    clearTimeout(delayTimer);
    await validateInputWithRequest("id_email", "email", "Эта почта уже занята");
};

const validatePhone = async () => {
    clearTimeout(delayTimer);
    await validateInputWithRequest(
        "id_phone", "phone", "Этот телефон уже занят", true
    );
};

const validatePassword = () => {
    const validate = () => {
        const passwordInput = document.getElementById('id_password1');
        let regButton = document.getElementById("registerButton");
        if (passwordInput.value !== "") {
            const passwordRegex = /^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$/;
            if (!passwordRegex.test(passwordInput.value)) {
                passwordInput.classList.remove("is-valid");
                passwordInput.classList.add("is-invalid");
                passwordInput.setCustomValidity("Неверный формат");
                addError("id_password1", "Пароль не соответствует формату", "format");
                regButton.disabled = true;
                return;
            } else {
                passwordInput.classList.remove("is-invalid");
                passwordInput.setCustomValidity("");
                removeError("id_password1", "format");
                regButton.disabled = false;
            }
        } else {
            passwordInput.classList.remove("is-invalid");
            passwordInput.setCustomValidity("");
            removeError("id_password1", "format");
            regButton.disabled = false;
        }

        const confirmPasswordInput = document.getElementById('id_password2');
        if (confirmPasswordInput.value !== "" && passwordInput.value !== passwordInput && passwordInput.value !== confirmPasswordInput.value) {
            confirmPasswordInput.classList.remove("is-valid");
            confirmPasswordInput.classList.add("is-invalid");
            confirmPasswordInput.setCustomValidity("Пароли не соответствуют");
            addError("id_password2", "Пароли не соответствуют", "confirm");
            regButton.disabled = true;
        } else {
            confirmPasswordInput.classList.remove("is-invalid");
            confirmPasswordInput.setCustomValidity("");
            removeError("id_password2", "confirm");
            regButton.disabled = false;
        }
    };
    if (delayTimer) clearTimeout(delayTimer);
    delayTimer = setTimeout(() => validate(), 750);
};