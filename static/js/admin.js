// Admin panel interactions: confirm dialogs are handled inline via onsubmit,
// this file covers any shared admin UI behavior (e.g. auto-dismissing flash messages).
document.addEventListener("DOMContentLoaded", () => {
  const flashMessages = document.querySelectorAll("[class*='rounded-md'][class*='text-sm'][class*='font-medium']");
  flashMessages.forEach((el) => {
    setTimeout(() => {
      el.style.transition = "opacity 0.5s ease";
      el.style.opacity = "0";
      setTimeout(() => el.remove(), 500);
    }, 5000);
  });
});
