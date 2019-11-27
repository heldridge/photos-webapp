let addTagsButton = <HTMLAnchorElement>document.getElementById('addTagsButton');
let addTagsInput = <HTMLInputElement>document.getElementById('addTagsInput');
let addTagsInputContainer = <HTMLDivElement>(
    document.getElementById('addTagsInputContainer')
);
let addTagsErrorMessage = <HTMLParagraphElement>(
    document.getElementById('addTagsErrorMessage')
);

if (addTagsButton !== null) {
    let originalHREF = addTagsButton.href;
}

interface validData {
    isValid: boolean;
    message: string;
}

interface onKeyUpEvent {
    key: string;
}

function validateTag(
    tag: string,
    maxTagLength: number,
    minTagLength: number,
    validTagRegex: RegExp
): validData {
    // Returns whether an input tag is valid, and a message to display if it
    // is not
    if (tag.length > maxTagLength) {
        return {
            isValid: false,
            message: `Tags must be under ${maxTagLength} characters`
        };
    } else if (tag.length < minTagLength && tag.length !== 0) {
        // Length of 0 doesn't count as invalid
        return {
            isValid: false,
            message: `Tags must be at least ${minTagLength} characters`
        };
    } else if (!validTagRegex.test(tag)) {
        return {
            isValid: false,
            message: `Tags must only contain alphanumeric characters and dashes`
        };
    } else {
        return {
            isValid: true,
            message: ''
        };
    }
}

function addTagsInputOnKeyUp(
    e: onKeyUpEvent,
    currentQuery: string,
    maxTagLength: number,
    minTagLength: number,
    validTagRegex: string
) {
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

function addTagsInputUpdated(
    currentQuery: string,
    maxTagLength: number,
    minTagLength: number,
    validTagRegex: string
) {
    // Checks tag input to display message if tag is invalid
    let value = addTagsInput.value;

    // Disable link if tag is empty
    if (value === '') {
        addClass(addTagsButton, 'disabled-link');
    }

    let valid = validateTag(
        value,
        maxTagLength,
        minTagLength,
        new RegExp(validTagRegex)
    );
    if (valid.isValid) {
        addClass(addTagsInputContainer, 'border-gray-300');
        removeClass(addTagsInputContainer, 'border-red-500');
        addClass(addTagsErrorMessage, 'hidden');
        let newHREF = originalHREF;
        if (currentQuery !== '' && value !== '') {
            newHREF += '+';
        }
        newHREF += value;
        addTagsButton.href = newHREF;

        if (value !== '') {
            removeClass(addTagsButton, 'disabled-link');
        }
    } else if (value !== '') {
        addTagsErrorMessage.innerHTML = valid.message;
        removeClass(addTagsInputContainer, 'border-gray-300');
        addClass(addTagsInputContainer, 'border-red-500');
        removeClass(addTagsErrorMessage, 'hidden');
        addClass(addTagsButton, 'disabled-link');
    }
}
