// Display a notification popup
function showNotification(title, message) {
    const popup = document.createElement('div');
    popup.className = 'notification-popup';
    popup.innerHTML = `
        <h4>${title}</h4>
        <p>${message}</p>
        <button onclick="dismissPopup(this)">Dismiss</button>
    `;
    document.body.appendChild(popup);

    // Show the popup
    popup.style.display = 'block';

    // Automatically dismiss after 5 seconds
    setTimeout(() => {
        dismissPopup(popup);
    }, 5000);
}

// Dismiss the notification popup
function dismissPopup(buttonOrElement) {
    const popup = buttonOrElement.parentElement || buttonOrElement;
    popup.style.animation = 'slideOut 0.5s ease-out';
    setTimeout(() => popup.remove(), 500); // Remove after animation ends
}

// Simulate receiving a notification
setTimeout(() => {
    showNotification('Subscription Reminder', 'Your Platinum plan expires in 7 days!');
}, 2000);

setTimeout(() => {
    showNotification('New Book Alert', 'The book "Python for Beginners" has been added to the library.');
}, 4000);
