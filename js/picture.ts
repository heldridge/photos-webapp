let publicId = JSON.parse(document.getElementById('publicId').textContent);

let loader = document.createElement('div');
loader.className = 'la-ball-clip-rotate la-sm la-dark ml-1';
loader.appendChild(document.createElement('div'));

let confirmDeleteBox = document.getElementById('confirmDeleteBox');
let deleteButton = document.getElementById('deleteButton');
document.addEventListener('click', (event) => {
    if (
        //@ts-ignore
        !confirmDeleteBox.contains(event.target) &&
        //@ts-ignore
        !deleteButton.contains(event.target) &&
        !hasClass(confirmDeleteBox, 'hidden')
    ) {
        addClass(confirmDeleteBox, 'hidden');
    }
});

function addFavoriteWrapper(source: HTMLButtonElement) {
    addFavorite(source, publicId, () => {});
}

function removeFavoriteWrapper(source: HTMLButtonElement) {
    removeFavorite(source, publicId, () => {});
}

function toggleConfirmDeleteBoxVisibility() {
    if (confirmDeleteBox) {
        if (hasClass(confirmDeleteBox, 'hidden')) {
            removeClass(confirmDeleteBox, 'hidden');
        } else {
            addClass(confirmDeleteBox, 'hidden');
        }
    }
}

function deletePicture(source: HTMLButtonElement) {
    source.appendChild(loader);
    addClass(source, 'pointer-events-none');

    let csrftoken = (<HTMLInputElement>(
        document.querySelector('[name=csrfmiddlewaretoken]')
    )).value;

    let request = new Request(`/pictures/${publicId}`, {
        headers: { 'X-CSRFToken': csrftoken },
    });

    fetch(request, {
        method: 'DELETE',
        mode: 'same-origin',
    }).then((response) => {
        source.removeChild(source.lastChild);
        removeClass(source, 'pointer-events-none');
        if (response.status >= 200 && response.status < 300) {
            document.location.href = '/pictures/delete-success';
        } else if (response.status === 401) {
            addMessage(
                'You must be logged in to delete pictures!',
                'must-be-logged-in-delete'
            );
        } else if (response.status === 403) {
            addMessage(
                'You are not authorized to delete this picture.',
                'not-authorized-delete'
            );
        } else if (response.status === 404) {
            addMessage('This picture was already deleted', 'already-deleted');
        } else {
            addMessage(
                'Something went wrong. Please try again later.',
                'something-went-wrong-delete'
            );
        }
    });
}
