window.setTimeout(clearMessages, 3 * 1000);

function clearMessages() {
    let messages = document.getElementsByClassName('message');
    for (let i = 0; i < messages.length; i++) {
        addClass(messages[i], 'opacity-0');
    }
}
