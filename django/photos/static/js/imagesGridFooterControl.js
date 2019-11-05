let cards = document.getElementsByClassName("h-picture-card");
let cardsHolder = document.getElementById("cardsHolder");
let previousButton = document.getElementById("previousButton");
let nextButton = document.getElementById("nextButton");
positionFooterButtons();

function positionFooterButtons() {
    if (cards.length > 0) {
        let margin = `${cards[0].getBoundingClientRect().left - cardsHolder.getBoundingClientRect().left}px`;
        previousButton.style.marginLeft = margin;
        nextButton.style.marginRight = margin;
    }
}

window.addEventListener('resize', positionFooterButtons);
