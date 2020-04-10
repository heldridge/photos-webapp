let publicId = JSON.parse(document.getElementById('publicId').textContent);

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
