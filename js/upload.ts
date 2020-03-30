function addPopularTag(source: HTMLButtonElement) {
    let tagsInput = <HTMLInputElement>document.getElementById('id_tags');
    let title = source.getElementsByTagName('span')[0];

    if (tagsInput.value.length === 0) {
        tagsInput.value = title.innerHTML;
    } else if (tagsInput.value.slice(-1) === ' ') {
        tagsInput.value = tagsInput.value + title.innerHTML;
    } else {
        tagsInput.value = tagsInput.value + ' ' + title.innerHTML;
    }
}
