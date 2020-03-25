let favoriteLoader = document.createElement('div');
favoriteLoader.className = 'la-ball-clip-rotate la-sm la-dark';
favoriteLoader.appendChild(document.createElement('div'));

function addFavorite(
    source: HTMLButtonElement,
    picturePublicId: string,
    successCallback: Function
) {
    removeChildren(source);
    source.appendChild(favoriteLoader);
    addClass(source, 'pointer-events-none');

    let csrftoken = (<HTMLInputElement>(
        document.querySelector('[name=csrfmiddlewaretoken]')
    )).value;

    let request = new Request(`/pictures/${picturePublicId}/favorites/`, {
        headers: { 'X-CSRFToken': csrftoken }
    });

    fetch(request, {
        method: 'POST',
        mode: 'same-origin'
    }).then(response => {
        removeChildren(source);
        removeClass(source, 'pointer-events-none');
        let emptyHeartIcon = document.createElement('i');
        emptyHeartIcon.className = 'far fa-heart';
        if (response.status >= 200 && response.status < 300) {
            successCallback();
            setToDeleteFavoriteMode(source);
        } else if (response.status === 401) {
            source.appendChild(emptyHeartIcon);
            addMessage(
                'You must be logged in to add a favorite!',
                'must-be-logged-in'
            );
        } else {
            source.appendChild(emptyHeartIcon);
            addMessage(
                'Something went wrong. Please try again later.',
                'something-went-wrong'
            );
        }
    });
}

function removeFavorite(
    source: HTMLButtonElement,
    picturePublicId: string,
    successCallback: Function
) {
    removeChildren(source);
    source.appendChild(favoriteLoader);
    addClass(source, 'pointer-events-none');

    let csrftoken = (<HTMLInputElement>(
        document.querySelector('[name=csrfmiddlewaretoken]')
    )).value;

    let request = new Request(`/pictures/${picturePublicId}/favorites/`, {
        headers: { 'X-CSRFToken': csrftoken }
    });

    fetch(request, {
        method: 'DELETE',
        mode: 'same-origin'
    }).then(response => {
        removeChildren(source);
        removeClass(source, 'pointer-events-none');
        let fullHeartIcon = document.createElement('i');
        fullHeartIcon.className = 'fas fa-heart text-error';
        if (response.status >= 200 && response.status < 300) {
            successCallback();
            setToAddFavoriteMode(source);
        } else if (response.status === 401) {
            source.appendChild(fullHeartIcon);
            addMessage(
                'You must be logged in to remove a favorite!',
                'must-be-logged-in'
            );
        } else {
            source.appendChild(fullHeartIcon);
            addMessage(
                'Something went wrong. Please try again later.',
                'something-went-wrong'
            );
        }
    });
}

function addMessage(text: string, classIdentifier: string) {
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
        message.className = `rounded bg-error text-black pl-4 min-w-64 text-center mt-2 ml-2 z-10 md:text-lg message sm:h-10 ${classIdentifier}`;
        message.innerHTML = text;
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

function setToAddFavoriteMode(favoriteButton: HTMLButtonElement) {
    let emptyHeartIcon = document.createElement('i');
    emptyHeartIcon.className = 'far fa-heart';

    removeChildren(favoriteButton);
    favoriteButton.appendChild(emptyHeartIcon);
    favoriteButton.onclick = () => addFavoriteWrapper(favoriteButton);
}

function setToDeleteFavoriteMode(favoriteButton: HTMLButtonElement) {
    let fullHeartIcon = document.createElement('i');
    fullHeartIcon.className = 'fas fa-heart text-error';
    removeChildren(favoriteButton);
    favoriteButton.appendChild(fullHeartIcon);
    favoriteButton.onclick = () => removeFavoriteWrapper(favoriteButton);
}
