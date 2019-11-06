function expandTags(collapser) {
    let hiddenTags = collapser.parentElement.nextElementSibling;
    removeClass(hiddenTags, 'hidden');
    addClass(collapser, 'hidden');
}
