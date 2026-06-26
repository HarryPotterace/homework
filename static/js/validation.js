const forms = document.querySelectorAll("[data-validation-form]");

forms.forEach((form) => {
  form.addEventListener("submit", (event) => {
    const inputs = form.querySelectorAll("input[required], textarea[required], select[required]");
    for (const input of inputs) {
      if (!String(input.value || "").trim()) {
        event.preventDefault();
        window.alert("请先完整填写必填项。");
        input.focus();
        return;
      }
    }

    if (form.dataset.validationForm === "register") {
      const passwordField = form.querySelector("[data-password-field='true']");
      const password = String(passwordField?.value || "");
      const strongEnough =
        password.length >= 8 &&
        /[A-Za-z]/.test(password) &&
        /\d/.test(password);

      if (!strongEnough) {
        event.preventDefault();
        window.alert("密码至少 8 位，并且同时包含字母和数字。");
        passwordField?.focus();
      }
    }
  });
});
