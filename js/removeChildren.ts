function removeChildren(e: HTMLElement) {
    while (e.hasChildNodes()) {
        e.removeChild(e.lastChild);
    }
}
