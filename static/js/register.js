document.addEventListener('DOMContentLoaded', () => {
  const togglePassword = document.querySelectorAll('.toggle-password');

  togglePassword.forEach((eye) => {
    eye.addEventListener('click', () => {
      const targetId = eye.dataset.target;
      const input = document.getElementById(targetId);
      if (input.type === 'password') {
        input.type = 'text';
        eye.textContent = '🙈';
      } else {
        input.type = 'password';
        eye.textContent = '👁';
      }
    });
  });
});
