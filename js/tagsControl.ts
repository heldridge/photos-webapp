function expandTags(expander: HTMLElement) {
    let hiddenTags = expander.parentElement.getElementsByClassName(
        'collapsed-tag'
    );
    for (let i = 0; i < hiddenTags.length; i++) {
        removeClass(hiddenTags[i], 'hidden');
    }
    expander.getElementsByClassName('fas')[0].className = 'fas fa-level-up-alt';
    expander.onclick = () => {
        collapseTags(expander);
    };
}

function collapseTags(collapser: HTMLElement) {
    let hiddenTags = collapser.parentElement.getElementsByClassName(
        'collapsed-tag'
    );
    for (let i = 0; i < hiddenTags.length; i++) {
        addClass(hiddenTags[i], 'hidden');
    }
    collapser.getElementsByClassName('fas')[0].className =
        'fas fa-level-down-alt';
    collapser.onclick = () => {
        expandTags(collapser);
    };
}
