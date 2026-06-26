document.querySelectorAll(".alert").forEach((element) => {
  window.setTimeout(() => {
    element.classList.add("fade");
  }, 2500);
});
