// Class manipulation functions from: https://jaketrent.com/post/addremove-classes-raw-javascript/
function hasClass(ele: HTMLElement, cls: string): boolean {
    return !!ele.className.match(new RegExp('(\\s|^)' + cls + '(\\s|$)'));
}

function addClass(ele: any, cls: string): void {
    if (!hasClass(ele, cls)) ele.className += ' ' + cls;
}

function removeClass(ele: any, cls: string): void {
    if (hasClass(ele, cls)) {
        var reg: RegExp = new RegExp('(\\s|^)' + cls + '(\\s|$)');
        ele.className = ele.className.replace(reg, ' ');
    }
}

function navSearchOnFocus(): void {
    let searchBorder: HTMLElement = document.getElementById('navSearchBorder');
    let navSearchIcon: HTMLElement = document.getElementById('navSearchIcon');

    if (!hasClass(searchBorder, 'border-red-500')) {
        removeClass(searchBorder, 'border-gray-300');
        addClass(searchBorder, 'border-blue-300');

        removeClass(navSearchIcon, 'opacity-50');
        addClass(navSearchIcon, 'opacity-100');
    }
}

function navSearchFocusOut(): void {
    let searchBorder: HTMLElement = document.getElementById('navSearchBorder');
    let navSearchIcon: HTMLElement = document.getElementById('navSearchIcon');

    if (!hasClass(searchBorder, 'border-red-500')) {
        removeClass(searchBorder, 'border-blue-300');
        addClass(searchBorder, 'border-gray-300');

        removeClass(navSearchIcon, 'opacity-100');
        addClass(navSearchIcon, 'opacity-50');
    }
}

function focusNavSearch(): void {
    document.getElementById('navSearch').focus();
}

function navSearchOnKeyUp(
    event,
    inputElement,
    maxTagLength,
    minTagLength,
    validTagRegex
): void {
    if (event.key === 'Enter') {
        let value = inputElement.value;
        if (
            value !== '' &&
            validateTag(
                value,
                maxTagLength,
                minTagLength,
                new RegExp(validTagRegex)
            ).isValid
        ) {
            window.location.href = `/search?q=${value}`;
        }
    }
}

function navSearchOnInput(
    navSearchInput,
    maxTagLength: number,
    minTagLength: number,
    validTagRegex: string
): void {
    let searchBorder: HTMLElement = document.getElementById('navSearchBorder');
    let navSearchErrorMessage = document.getElementById(
        'navSearchErrorMessage'
    );
    let value = navSearchInput.value;

    let valid = validateTag(
        value,
        maxTagLength,
        minTagLength,
        new RegExp(validTagRegex)
    );

    if (valid.isValid) {
        addClass(searchBorder, 'border-blue-300');
        removeClass(searchBorder, 'border-red-500');
        addClass(navSearchErrorMessage, 'hidden');
    } else {
        navSearchErrorMessage.innerHTML = valid.message;
        removeClass(navSearchErrorMessage, 'hidden');

        addClass(searchBorder, 'border-red-500');
        removeClass(searchBorder, 'border-blue-300');
    }
}
