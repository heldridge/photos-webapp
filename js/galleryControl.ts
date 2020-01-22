// @ts-ignore
let allPictures: Array = allPicturesOutside;
//@ts-ignore
let originalPictureIndex = originalPictureIndexOutside;
//@ts-ignore
let nextPageLink = nextPageLinkOutside;
//@ts-ignore
let previousPageLink = previousPageLinkOutside;
//@ts-ignore
let renderNextButton = renderNextButtonOutside;
//@ts-ignore
let renderPreviousButton = renderPreviousButtonOutside;

let galleryNextImages = document.getElementById('gallery-next-images').children;
let imagesInfo = document.getElementById('images-info').children;

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
let previousLinks = document.getElementsByClassName('previous-link');
let nextLinks = document.getElementsByClassName('next-link');

let sideBarSlots: number = 26;

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
            // Remove children
            while (modalImageContainer.hasChildNodes()) {
                modalImageContainer.removeChild(modalImageContainer.lastChild);
            }

            // Add new child
            let image = document.createElement('img');
            addClass(image, 'max-h-80-screen');
            image.src = allPictures[index].photo;
            galleryImageContainer.appendChild(image);

            // Add child to modal image
            let modalImage = document.createElement('img');
            modalImage.src = allPictures[index].photo;
            modalImageContainer.appendChild(modalImage);
        }
        updateNextPrevActions(index);

        removeClass(galleryNextImages[currentIndex], 'selected-picture');
        addClass(galleryNextImages[index], 'selected-picture');

        addClass(imagesInfo[currentIndex], 'hidden');
        removeClass(imagesInfo[index], 'hidden');

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
    }
}

function previousPicture(): void {
    if (currentIndex > 0) {
        setImage(currentIndex - 1, 'push');
    }
}

function updateNextPrevActions(index: number): void {
    // Controls whether the "next" and "previous" buttons in the gallery sidebar are
    // buttons or links. When index is 0 "previous" becomes a link. When index is at its
    // maximum value "next" becomes a link. If either is not a link it is made a button.
    if (index === 0) {
        for (let i = 0; i < previousButtons.length; i++) {
            console.log('HERE!!');
            console.log(previousButtons[i]);

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
