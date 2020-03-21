let pictures = JSON.parse(document.getElementById('pictures').textContent);
let originalPictureIndex = JSON.parse(
    document.getElementById('original-picture-index').textContent
);

let galleryNextImages = document.getElementById('gallery-next-images');
let imagesInfo = document.getElementById('images-info');
let uploadedByLink = <HTMLAnchorElement>(
    document.getElementById('uploaded-by-link')
);

let galleryImageContainer = <HTMLDivElement>(
    document.getElementById('gallery-image-container')
);
let modalImageContainer = <HTMLDivElement>(
    document.getElementById('modal-image-container')
);

let modalImage = <HTMLDivElement>document.getElementById('modal-image');

let currentIndex = originalPictureIndex;
let previousButtons = document.getElementsByClassName('previous-button');
let nextButtons = document.getElementsByClassName('next-button');
let previousLinks = <HTMLCollectionOf<HTMLAnchorElement>>(
    document.getElementsByClassName('previous-link')
);
let nextLinks = <HTMLCollectionOf<HTMLAnchorElement>>(
    document.getElementsByClassName('next-link')
);

let sideBarSlots: number = 26;

// Only set the next/previous links (used in nextPicture and previousPicture functions)
// if there is a valid next/previous link and that link is enabled
let nextLinkHREF = '';
if (nextLinks.length > 0 && !hasClass(nextLinks[0], 'pointer-events-none')) {
    nextLinkHREF = nextLinks[0].href;
}

let previousLinkHREF = '';
if (
    previousLinks.length > 0 &&
    !hasClass(previousLinks[0], 'pointer-events-none')
) {
    previousLinkHREF = previousLinks[0].href;
}

let emptyHeartIcon = document.createElement('i');
emptyHeartIcon.className = 'far fa-heart';

let fullHeartIcon = document.createElement('i');
fullHeartIcon.className = 'fas fa-heart text-error';

setImage(originalPictureIndex, 'replace');

let preloadedImages = {};
preloadImages();

let favoriteLoader = document.createElement('div');
favoriteLoader.className = 'la-ball-clip-rotate la-sm la-dark';
favoriteLoader.appendChild(document.createElement('div'));

function setImage(index: number, stateAction: string = '') {
    if (index < pictures.length) {
        if (galleryImageContainer) {
            // Remove children
            removeChildren(galleryImageContainer);

            // Add new child
            let image = document.createElement('img');
            addClass(image, 'max-h-80-screen');
            image.src = `/media/${pictures[index].photo}`;
            galleryImageContainer.appendChild(image);
        }
        if (modalImageContainer) {
            // Remove children
            removeChildren(modalImageContainer);

            // Add child to modal image
            let modalImage = document.createElement('img');
            modalImage.src = `/media/${pictures[index].photo}`;
            modalImageContainer.appendChild(modalImage);
        }

        updateNextPrevActions(index);

        if (galleryNextImages) {
            removeClass(
                galleryNextImages.children[currentIndex],
                'selected-picture'
            );
            addClass(galleryNextImages.children[index], 'selected-picture');
        }

        // Set the title
        let imageTitle = document.getElementById('image-title');
        if (imageTitle) {
            imageTitle.innerHTML = pictures[index].title;
        }
        let imageTitleLink = <HTMLAnchorElement>(
            document.getElementById('image-title-link')
        );
        if (imageTitleLink) {
            imageTitleLink.href = `/pictures/${pictures[index].public_id}`;
        }

        // Set the tags
        let imageTags = <HTMLDivElement>document.getElementById('image-tags');
        if (imageTags) {
            // Remove previous tags
            removeChildren(imageTags);
            // Add the new tags
            pictures[index].tags.forEach((tag: string) => {
                addTag(imageTags, tag);
            });
        }

        // Set the favorite button
        let favoriteButton = <HTMLButtonElement>(
            document.getElementById('favoriteButton')
        );
        if (pictures[index].favorite) {
            setToDeleteFavoriteMode(favoriteButton);
        } else {
            setToAddFavoriteMode(favoriteButton);
        }

        // Set the uploaded by link
        if (uploadedByLink) {
            removeChildren(uploadedByLink);
            console.log(pictures[index]);
            if (pictures[index].uploaded_by_public_id) {
                uploadedByLink.href = `/accounts/users/${pictures[index].uploaded_by_public_id}`;
                uploadedByLink.innerHTML =
                    pictures[index].uploaded_by_display_name;
            }
        }

        currentIndex = index;

        // TODO: Iterate over url params instead of building individually
        let query = getUrlParameter('q');
        let after = getUrlParameter('after');
        let before = getUrlParameter('before');
        let favorites = getUrlParameter('favorites');
        let uploadedBy = getUrlParameter('uploaded_by');

        if (stateAction) {
            let newState = `?p=${pictures[index].public_id}`;
            if (query) {
                newState += `&q=${query}`;
            }
            if (after) {
                newState += `&after=${after}`;
            }
            if (before) {
                newState += `&before=${before}`;
            }
            if (favorites) {
                newState += `&favorites=${favorites}`;
            }
            if (uploadedBy) {
                newState += `&uploaded_by=${uploadedBy}`;
            }

            if (stateAction === 'push') {
                history.pushState({ index: index }, '', newState);
            } else if (stateAction === 'replace') {
                history.replaceState({ index: index }, '', newState);
            }
        }
    }
}

function nextPicture(): void {
    if (currentIndex + 1 < pictures.length) {
        setImage(currentIndex + 1, 'push');
    } else if (nextLinkHREF) {
        document.location.href = nextLinkHREF;
    }
}

function previousPicture(): void {
    if (currentIndex > 0) {
        setImage(currentIndex - 1, 'push');
    } else if (previousLinkHREF) {
        document.location.href = previousLinkHREF;
    }
}

function updateNextPrevActions(index: number): void {
    // Controls whether the "next" and "previous" buttons in the gallery sidebar are
    // buttons or links. When index is 0 "previous" becomes a link. When index is at its
    // maximum value "next" becomes a link. If either is not a link it is made a button.
    if (index === 0) {
        for (let i = 0; i < previousButtons.length; i++) {
            addClass(previousButtons[i], 'hidden');
        }
        for (let i = 0; i < previousLinks.length; i++) {
            removeClass(previousLinks[i], 'hidden');
        }
    } else {
        for (let i = 0; i < previousButtons.length; i++) {
            removeClass(previousButtons[i], 'hidden');
        }
        for (let i = 0; i < previousLinks.length; i++) {
            addClass(previousLinks[i], 'hidden');
        }
    }

    if (index === pictures.length - 1) {
        for (let i = 0; i < nextButtons.length; i++) {
            addClass(nextButtons[i], 'hidden');
        }
        for (let i = 0; i < nextLinks.length; i++) {
            removeClass(nextLinks[i], 'hidden');
        }
    } else {
        for (let i = 0; i < nextButtons.length; i++) {
            removeClass(nextButtons[i], 'hidden');
        }
        for (let i = 0; i < nextLinks.length; i++) {
            addClass(nextLinks[i], 'hidden');
        }
    }
}

window.onpopstate = function(event: PopStateEvent) {
    if (event.state) {
        setImage(event.state.index);
    }
};

function showModalImage() {
    removeClass(modalImage, 'hidden');
}

function hideModalImage() {
    addClass(modalImage, 'hidden');
}

document.onkeyup = function(event) {
    if (event.code === 'ArrowLeft') {
        previousPicture();
    } else if (event.code === 'ArrowRight') {
        nextPicture();
    } else if (event.code === 'KeyF') {
        if (hasClass(modalImage, 'hidden')) {
            showModalImage();
        } else {
            hideModalImage();
        }
    }
};

function preloadImages() {
    pictures.forEach(picture => {
        let newImg = new Image();
        newImg.src = `/media/${picture.photo}`;
        preloadedImages[picture.public_id] = newImg;
    });
}

function addTag(parent: HTMLDivElement, tag: string) {
    let tagAnchor = document.createElement('a');
    tagAnchor.className =
        'tag rounded py-1 md:py-2 px-2 md:px-3 mr-3 font-medium mb-3 text-xs md:text-md bg-tag hover:bg-tag-hover text-tag hover:text-tag-hover';
    tagAnchor.href = `/search?q=${tag}`;

    let tagSpan = document.createElement('span');
    tagSpan.className = 'opacity-medium-emphasis';
    tagSpan.innerHTML = tag;

    tagAnchor.appendChild(tagSpan);
    parent.appendChild(tagAnchor);
}

function addFavorite(source: HTMLButtonElement) {
    removeChildren(source);
    source.appendChild(favoriteLoader);
    addClass(source, 'pointer-events-none');

    let csrftoken = (<HTMLInputElement>(
        document.querySelector('[name=csrfmiddlewaretoken]')
    )).value;

    let request = new Request(
        `/pictures/${pictures[currentIndex].public_id}/favorites/`,
        {
            headers: { 'X-CSRFToken': csrftoken }
        }
    );

    fetch(request, {
        method: 'POST',
        mode: 'same-origin'
    }).then(response => {
        removeChildren(source);
        removeClass(source, 'pointer-events-none');
        if (response.status >= 200 && response.status < 300) {
            pictures[currentIndex].favorite = true;
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

function removeFavorite(source: HTMLButtonElement) {
    removeChildren(source);
    source.appendChild(favoriteLoader);
    addClass(source, 'pointer-events-none');

    let csrftoken = (<HTMLInputElement>(
        document.querySelector('[name=csrfmiddlewaretoken]')
    )).value;

    let request = new Request(
        `/pictures/${pictures[currentIndex].public_id}/favorites/`,
        {
            headers: { 'X-CSRFToken': csrftoken }
        }
    );

    fetch(request, {
        method: 'DELETE',
        mode: 'same-origin'
    }).then(response => {
        removeChildren(source);
        removeClass(source, 'pointer-events-none');
        if (response.status >= 200 && response.status < 300) {
            pictures[currentIndex].favorite = false;
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
    removeChildren(favoriteButton);
    favoriteButton.appendChild(emptyHeartIcon);
    favoriteButton.onclick = () => addFavorite(favoriteButton);
}

function setToDeleteFavoriteMode(favoriteButton: HTMLButtonElement) {
    removeChildren(favoriteButton);
    favoriteButton.appendChild(fullHeartIcon);
    favoriteButton.onclick = () => removeFavorite(favoriteButton);
}

function removeChildren(e: HTMLElement) {
    while (e.hasChildNodes()) {
        e.removeChild(e.lastChild);
    }
}
