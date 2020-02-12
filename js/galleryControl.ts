// @ts-ignore
let allPictures: Array = allPicturesOutside;
//@ts-ignore
let originalPictureIndex = originalPictureIndexOutside;

let galleryNextImages = document.getElementById('gallery-next-images');
let imagesInfo = document.getElementById('images-info');

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

setImage(originalPictureIndex, 'replace');

function setImage(index: number, stateAction: string = '') {
    if (index < allPictures.length) {
        if (galleryImageContainer) {
            // Remove children
            while (galleryImageContainer.hasChildNodes()) {
                galleryImageContainer.removeChild(
                    galleryImageContainer.lastChild
                );
            }

            // Add new child
            let image = document.createElement('img');
            addClass(image, 'max-h-80-screen');
            image.src = `/media/${allPictures[index].photo}`;
            galleryImageContainer.appendChild(image);
        }
        if (modalImageContainer) {
            // Remove children
            while (modalImageContainer.hasChildNodes()) {
                modalImageContainer.removeChild(modalImageContainer.lastChild);
            }

            // Add child to modal image
            let modalImage = document.createElement('img');
            modalImage.src = `/media/${allPictures[index].photo}`;
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

        if (imagesInfo) {
            addClass(imagesInfo.children[currentIndex], 'hidden');
            removeClass(imagesInfo.children[index], 'hidden');
        }

        currentIndex = index;

        let query = getUrlParameter('q');
        let after = getUrlParameter('after');
        let before = getUrlParameter('before');

        if (stateAction) {
            let newState = `?p=${allPictures[index].public_id}`;
            if (query) {
                newState += `&q=${query}`;
            }
            if (after) {
                newState += `&after=${after}`;
            }
            if (before) {
                newState += `&before=${before}`;
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
    if (currentIndex + 1 < allPictures.length) {
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

    if (index === allPictures.length - 1) {
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
