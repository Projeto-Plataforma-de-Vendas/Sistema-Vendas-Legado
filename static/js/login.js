document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll('.toggle-password').forEach(icon => {
    icon.addEventListener('click', () => {
      const target = document.getElementById(icon.dataset.target);
      target.type = target.type === 'password' ? 'text' : 'password';
    });
  });
});
