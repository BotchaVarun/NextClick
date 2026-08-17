// Booking form: prevent selecting a past date, basic client-side validation
document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("booking-form");
  const dateInput = form ? form.querySelector('input[name="event_date"]') : null;

  if (dateInput) {
    const today = new Date().toISOString().split("T")[0];
    dateInput.setAttribute("min", today);
  }

  if (form) {
    form.addEventListener("submit", (e) => {
      const email = form.querySelector('input[name="email"]').value.trim();
      const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      if (!emailPattern.test(email)) {
        e.preventDefault();
        alert("Please enter a valid email address.");
      }
    });
  }
});
