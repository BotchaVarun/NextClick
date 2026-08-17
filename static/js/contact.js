// Contact form: basic client-side validation before submit
document.addEventListener("DOMContentLoaded", () => {
  const form = document.querySelector('form[action*="contact"]');
  if (!form) return;

  form.addEventListener("submit", (e) => {
    const message = form.querySelector('textarea[name="message"]');
    if (message && message.value.trim().length < 10) {
      e.preventDefault();
      alert("Please enter a message of at least 10 characters.");
    }
  });
});
