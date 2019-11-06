function expandTags(expander) {
    let hiddenTags = expander.parentElement.getElementsByClassName('collapsed-tag');
    for (i = 0; i < hiddenTags.length; i ++) {
        removeClass(hiddenTags[i], 'hidden');
    }
    addClass(expander, 'hidden');
}

function collapseTags(collapser) {
    let hiddenTags = collapser.parentElement.getElementsByClassName('collapsed-tag');
    for (i = 0; i < hiddenTags.length; i ++) {
        addClass(hiddenTags[i], 'hidden');
    }
    let expander = collapser.parentElement.getElementsByClassName('tag-expander')[0];
    removeClass(expander, 'hidden');
}