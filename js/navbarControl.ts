let defaultBorderClass = 'border-default';
let selectedBorderClass = 'border-input-selected';
let errorBorderClass = 'border-error';

let unfocusedIconClass = 'opacity-disabled';
let focusedIconClass = 'opacity-medium-emphasis';

let theme = localStorage.getItem('theme');
if (theme === 'dark') {
    setDarkTheme();
    let themeSwitch = <HTMLInputElement>document.getElementById('theme-switch');
    themeSwitch.checked = true;
} else if (theme === 'light') {
    setLightTheme();
    let themeSwitch = <HTMLInputElement>document.getElementById('theme-switch');
    themeSwitch.checked = false;
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

function navSearchOnFocus(): void {
    let searchBorder: HTMLElement = document.getElementById('navSearchBorder');
    let navSearchIcon: HTMLElement = document.getElementById('navSearchIcon');

    if (!hasClass(searchBorder, errorBorderClass)) {
        removeClass(searchBorder, defaultBorderClass);
        addClass(searchBorder, selectedBorderClass);

        removeClass(navSearchIcon, unfocusedIconClass);
        addClass(navSearchIcon, focusedIconClass);
    }
}

function navSearchFocusOut(): void {
    let searchBorder: HTMLElement = document.getElementById('navSearchBorder');
    let navSearchIcon: HTMLElement = document.getElementById('navSearchIcon');

    if (!hasClass(searchBorder, errorBorderClass)) {
        removeClass(searchBorder, selectedBorderClass);
        addClass(searchBorder, defaultBorderClass);

        removeClass(navSearchIcon, focusedIconClass);
        addClass(navSearchIcon, unfocusedIconClass);
    }
}

function focusNavSearch(): void {
    document.getElementById('navSearch').focus();
}

function navSearchOnKeyUp(
    event: onKeyUpEvent,
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

function navSearchRestrictOnInput(
    navSearchInput: HTMLInputElement,
    invalidCharRegex: string
) {
    navSearchInput.value = navSearchInput.value.replace(
        new RegExp(invalidCharRegex, 'g'),
        ''
    );
}

function setDarkTheme() {
    let body = document.getElementById('body');
    let themeSunIcon = document.getElementById('theme-sun-icon');
    let themeMoonIcon = document.getElementById('theme-moon-icon');

    removeClass(body, 'theme-light');
    addClass(body, 'theme-dark');

    removeClass(themeSunIcon, 'opacity-high-emphasis');
    addClass(themeSunIcon, 'opacity-disabled');

    removeClass(themeMoonIcon, 'opacity-disabled');
    addClass(themeMoonIcon, 'opacity-high-emphasis');
}

function setLightTheme() {
    let body = document.getElementById('body');
    let themeSunIcon = document.getElementById('theme-sun-icon');
    let themeMoonIcon = document.getElementById('theme-moon-icon');

    removeClass(body, 'theme-dark');
    addClass(body, 'theme-light');

    removeClass(themeMoonIcon, 'opacity-high-emphasis');
    addClass(themeMoonIcon, 'opacity-disabled');

    removeClass(themeSunIcon, 'opacity-disabled');
    addClass(themeSunIcon, 'opacity-high-emphasis');
}

function toggleLightDarkTheme() {
    let themeSwitch = <HTMLInputElement>document.getElementById('theme-switch');

    if (themeSwitch.checked) {
        setDarkTheme();
        window.localStorage.setItem('theme', 'dark');
    } else {
        setLightTheme();
        window.localStorage.setItem('theme', 'light');
    }
}
