function expandTags(collapser) {
    let hiddenTags = collapser.parentElement.getElementsByClassName('collapsed-tag');
    for (i = 0; i < hiddenTags.length; i ++) {
        removeClass(hiddenTags[i], 'hidden');
    }
    addClass(collapser, 'hidden');
}
