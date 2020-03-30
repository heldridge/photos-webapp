function addPopularTag(source: HTMLButtonElement) {
    let tagsInput = <HTMLInputElement>document.getElementById('id_tags');
    let title = source.getElementsByTagName('span')[0];
    tagsInput.value = tagsInput.value + ' ' + title.innerHTML;
}
