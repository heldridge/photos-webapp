let addTagsButton = <HTMLAnchorElement>document.getElementById('addTagsButton');
let addTagsInput = <HTMLInputElement>document.getElementById('addTagsInput');
let addTagsInputContainer = <HTMLDivElement>(
    document.getElementById('addTagsInputContainer')
);
let addTagsErrorMessage = <HTMLParagraphElement>(
    document.getElementById('addTagsErrorMessage')
);
let originalHREF = addTagsButton.href;

function validateTag(
    tag: string,
    maxTagLength: number,
    minTagLength: number,
    validTagRegex: RegExp
) {
    if (tag.length > maxTagLength) {
        return {
            isValid: false,
            message: `Tags must be under ${maxTagLength} characters`
        };
    } else if (tag.length < minTagLength && tag.length !== 0) {
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
            isValid: true
        };
    }
}

function addTagsInputUpdated(
    currentQuery: string,
    maxTagLength: number,
    minTagLength: number,
    validTagRegex: string
) {
    let value = addTagsInput.value;

    let validData = validateTag(
        value,
        maxTagLength,
        minTagLength,
        new RegExp(validTagRegex)
    );
    if (validData.isValid) {
        addClass(addTagsInputContainer, 'border-gray-300');
        removeClass(addTagsInputContainer, 'border-red-500');
        addClass(addTagsErrorMessage, 'hidden');
        let newHREF = originalHREF;
        if (currentQuery !== '' && value !== '') {
            newHREF += '+';
        }
        newHREF += value;
        addTagsButton.href = newHREF;
        removeClass(addTagsButton, 'disabled-link');
    } else if (value !== '') {
        addTagsErrorMessage.innerHTML = validData.message;
        removeClass(addTagsInputContainer, 'border-gray-300');
        addClass(addTagsInputContainer, 'border-red-500');
        removeClass(addTagsErrorMessage, 'hidden');
        addClass(addTagsButton, 'disabled-link');
    }
}
