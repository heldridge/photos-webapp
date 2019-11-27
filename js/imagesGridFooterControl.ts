let cards: HTMLCollection = document.getElementsByClassName('h-picture-card');
let cardsHolder: HTMLElement = document.getElementById('cardsHolder');
let previousButton: HTMLElement = document.getElementById('previousButton');
let nextButton: HTMLElement = document.getElementById('nextButton');
positionFooterButtons();

function positionFooterButtons(): void {
    if (cards.length > 0) {
        let margin: string = `${cards[0].getBoundingClientRect().left -
            cardsHolder.getBoundingClientRect().left}px`;
        if (previousButton !== null) {
            previousButton.style.marginLeft = margin;
        }

        if (nextButton !== null) {
            nextButton.style.marginRight = margin;
        }
    }
}

window.addEventListener('resize', positionFooterButtons);
