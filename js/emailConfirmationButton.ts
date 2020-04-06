let loader = document.createElement('div');
loader.className = 'la-ball-clip-rotate la-sm la-dark ml-1';
loader.appendChild(document.createElement('div'));

function sendConfirmationEmail(source: HTMLButtonElement) {
    source.appendChild(loader);
    addClass(source, 'pointer-events-none');

    let csrftoken = (<HTMLInputElement>(
        document.querySelector('[name=csrfmiddlewaretoken]')
    )).value;

    let request = new Request(`/accounts/send-confirmation-email`, {
        headers: { 'X-CSRFToken': csrftoken },
    });

    fetch(request, {
        method: 'POST',
        mode: 'same-origin',
    }).then((response) => {
        source.removeChild(source.lastChild);
        removeClass(source, 'pointer-events-none');
        if (response.status >= 200 && response.status < 300) {
            addMessage('Email Sent!', 'email-sent', 'bg-success');
        } else if (response.status === 429) {
            addMessage(
                'You have requested too many emails, please try again later.',
                'too-many-emails',
                'bg-error'
            );
        } else {
            addMessage(
                'Something went wrong sending the confirmation email. Please try again later.',
                'something-went-wrong',
                'bg-error'
            );
        }
    });
}

function addMessage(text: string, classIdentifier: string, bgClass: string) {
    /*
    Build message:
    <li class="rounded bg-error text-black pl-4 min-w-64 text-center mt-2 ml-2 z-10 md:text-lg message sm:h-10 ~*~Identifier~*~"> 
        ~*~Text~*~
        <button class="pl-2 pr-4 h-full opacity-message-close hover:opacity-message-close-hover py-2 sm:py-0">
            <i class="fas fa-times"></i>
        </button>
    </li>
    */
    if (document.getElementsByClassName(classIdentifier).length === 0) {
        // Only add the message if there isn't one already
        let message = document.createElement('li');
        message.className = `rounded ${bgClass} text-black pl-4 min-w-64 flex items-center justify-between mt-2 ml-2 z-10 md:text-lg message sm:h-10 ${classIdentifier}`;

        let placeholder = document.createElement('div');
        message.appendChild(placeholder);

        let messageText = document.createElement('span');
        messageText.innerHTML = text;
        message.appendChild(messageText);

        let closeButton = document.createElement('button');
        closeButton.className =
            'pl-2 pr-4 h-full opacity-message-close hover:opacity-message-close-hover py-2 sm:py-0';
        let closeIcon = document.createElement('i');
        closeIcon.className = 'fas fa-times';
        closeButton.appendChild(closeIcon);
        closeButton.onclick = () => closeMessage(message);

        message.appendChild(closeButton);

        let messages = document.getElementById('messages');
        messages.appendChild(message);

        // After three seconds, fade out the message.
        // .6 seconds after fading out, remove from the dom
        window.setTimeout(() => {
            if (message) {
                addClass(message, 'opacity-0');
                window.setTimeout(() => {
                    if (message) {
                        message.remove();
                    }
                }, 0.6 * 1000);
            }
        }, 3 * 1000);
    }
}

// Called when the "close" button on a message is pressed
function closeMessage(message: HTMLLIElement) {
    if (message) {
        addClass(message, 'opacity-0');
        window.setTimeout(() => {
            if (message) {
                message.remove();
            }
        }, 0.6 * 1000);
    }
}
