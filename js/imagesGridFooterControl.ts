let cards: HTMLCollection = document.getElementsByClassName('h-picture-card');
let cardsHolder: HTMLElement = document.getElementById('cardsHolder');
let previousButton: HTMLElement = document.getElementById('previousButton');
let nextButton: HTMLElement = document.getElementById('nextButton');
positionFooterButtons();

function positionFooterButtons(): void {
    if (cards.length > 0 && nextButton !== null && previousButton !== null) {
        let margin: string = `${cards[0].getBoundingClientRect().left -
            cardsHolder.getBoundingClientRect().left}px`;
        previousButton.style.marginLeft = margin;
        nextButton.style.marginRight = margin;
    }
}

window.addEventListener('resize', positionFooterButtons);
