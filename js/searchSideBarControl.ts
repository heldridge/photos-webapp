// @ts-ignore
let currentQuery = currentQueryOutside;
// @ts-ignore
let maxTagLength = maxTagLengthOutside;
// @ts-ignore
let minTagLength = minTagLengthOutside;
// @ts-ignore
let validTagRegex = validTagRegexOutside;

// @ts-ignore
let baseFavoritesQuery = baseFavoritesQueryOutside;
console.log(baseFavoritesQuery);

let addTagsIconEnabledClasses = ['text-black'];
let addTagsIconDisabledClass = 'opacity-disabled';

let addTagsButtonEnabledClasses = ['bg-primary', 'hover:bg-primary-hover'];
let addTagsButtonDisabledClasses = [
    'bg-button-disabled',
    'pointer-events-none',
];

let addTagsInputContainerDefaultClass = 'border-default';
let addTagsInputContainerErrorClass = 'border-error';

let addTagsButton = <HTMLAnchorElement>document.getElementById('addTagsButton');
let addTagsIcon = document.getElementById('addTagsIcon');
let addTagsInput = <HTMLInputElement>document.getElementById('addTagsInput');
let addTagsInputContainer = <HTMLDivElement>(
    document.getElementById('addTagsInputContainer')
);
let addTagsErrorMessage = <HTMLParagraphElement>(
    document.getElementById('addTagsErrorMessage')
);
let originalHREF = '';
if (addTagsButton !== null) {
    originalHREF = addTagsButton.href;
}

addTagsInputUpdated();

function addTagsInputOnKeyUp(e: onKeyUpEvent) {
    // Listens for an "Enter" keypress in the add tags input,
    // on one directs the page to the page + tag
    if (e.key === 'Enter') {
        let value = addTagsInput.value;
        if (value !== '') {
            // Don't change pages if input is empty
            let valid = validateTag(
                value,
                maxTagLength,
                minTagLength,
                new RegExp(validTagRegex)
            );

            if (valid.isValid) {
                // Only change pages if tag is valid
                let newHREF = originalHREF;
                if (currentQuery !== '') {
                    newHREF += '+';
                }
                newHREF += value;
                window.location.href = newHREF;
            }
        }
    }
}

function addTagsInputUpdated() {
    // Checks tag input to display message if tag is invalid
    let value = addTagsInput.value;

    // Disable link if tag is empty
    if (value === '') {
        addTagsButtonEnabledClasses.forEach((className) => {
            removeClass(addTagsButton, className);
        });
        addTagsButtonDisabledClasses.forEach((className) => {
            addClass(addTagsButton, className);
        });

        addTagsIconEnabledClasses.forEach((className) => {
            removeClass(addTagsIcon, className);
        });
        addClass(addTagsIcon, addTagsIconDisabledClass);
    }

    let valid = validateTag(
        value,
        maxTagLength,
        minTagLength,
        new RegExp(validTagRegex)
    );
    if (valid.isValid) {
        addClass(addTagsInputContainer, addTagsInputContainerDefaultClass);
        removeClass(addTagsInputContainer, addTagsInputContainerErrorClass);
        addClass(addTagsErrorMessage, 'hidden');

        let newHREF = originalHREF;
        if (currentQuery !== '' && value !== '') {
            newHREF += '+';
        }
        newHREF += value;
        addTagsButton.href = newHREF;

        if (value !== '') {
            addTagsButtonDisabledClasses.forEach((className) => {
                removeClass(addTagsButton, className);
            });

            addTagsButtonEnabledClasses.forEach((className) => {
                addClass(addTagsButton, className);
            });

            removeClass(addTagsIcon, addTagsIconDisabledClass);

            addTagsIconEnabledClasses.forEach((className) => {
                addClass(addTagsIcon, className);
            });
        }
    } else if (value !== '') {
        addTagsErrorMessage.innerHTML = valid.message;
        removeClass(addTagsInputContainer, addTagsInputContainerDefaultClass);
        addClass(addTagsInputContainer, addTagsInputContainerErrorClass);

        removeClass(addTagsErrorMessage, 'hidden');

        addTagsButtonEnabledClasses.forEach((className) => {
            removeClass(addTagsButton, className);
        });
        addTagsButtonDisabledClasses.forEach((className) => {
            addClass(addTagsButton, className);
        });

        addTagsIconEnabledClasses.forEach((className) => {
            removeClass(addTagsIcon, className);
        });
        addClass(addTagsIcon, addTagsIconDisabledClass);
    }
}

function updateFavoritesSearch(e: HTMLInputElement) {
    let newHREF = `/search?${baseFavoritesQuery}`;

    if (e.checked) {
        newHREF = `${newHREF}&favorites=true`;
    }
    document.location.href = newHREF;
}

function toggleSortOrderVisible(source: HTMLButtonElement) {
    let sortOrderBox = source.lastElementChild;

    if (hasClass(sortOrderBox, 'hidden')) {
        removeClass(sortOrderBox, 'hidden');
    } else {
        addClass(sortOrderBox, 'hidden');
    }
}
