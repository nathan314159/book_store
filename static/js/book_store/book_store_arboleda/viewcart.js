document.addEventListener("DOMContentLoaded", function() {
    const messageElement = document.querySelector('.message');
    setTimeout(() => {
        messageElement.classList.add('hidden');
    }, 2000);
  });
