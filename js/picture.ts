let publicId = JSON.parse(document.getElementById('publicId').textContent);

function addFavoriteWrapper(source: HTMLButtonElement) {
    addFavorite(source, publicId, () => {});
}

function removeFavoriteWrapper(source: HTMLButtonElement) {
    removeFavorite(source, publicId, () => {});
}
