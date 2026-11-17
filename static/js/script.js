// Small client-side enhancement: prevent accidental double-clicks on submit buttons.
document.addEventListener("submit", function (event) {
  const button = event.target.querySelector('button[type="submit"]');
  if (button && !button.dataset.allowRepeat) {
    button.dataset.originalText = button.textContent;
    button.disabled = true;
    button.textContent = "Please wait...";
  }
});
