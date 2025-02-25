document.addEventListener('DOMContentLoaded', function() {
    // Get all message items
    const messages = document.querySelectorAll('.message-item');

    // Show messages with a slight delay between each
    messages.forEach((message, index) => {
        setTimeout(() => {
            // Show the message
            message.classList.remove('opacity-0', 'translate-x-[-100%]');

            // Remove the message after 5 seconds
            setTimeout(() => {
                message.classList.add('opacity-0', 'translate-x-[-100%]');

                // Remove from DOM after animation completes
                setTimeout(() => {
                    message.remove();
                }, 500);
            }, 5000);
        }, index * 200); // 200ms delay between each message
    });
});
