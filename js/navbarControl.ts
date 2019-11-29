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

function navSearchFocus(): void {
    let searchBorder: HTMLElement = document.getElementById('navSearchBorder');
    let navSearchIcon: HTMLElement = document.getElementById('navSearchIcon');

    removeClass(searchBorder, 'border-gray-300');
    addClass(searchBorder, 'border-blue-300');

    removeClass(navSearchIcon, 'opacity-50');
    addClass(navSearchIcon, 'opacity-100');
}

function navSearchFocusOut(): void {
    let searchBorder: HTMLElement = document.getElementById('navSearchBorder');
    let navSearchIcon: HTMLElement = document.getElementById('navSearchIcon');

    removeClass(searchBorder, 'border-blue-300');
    addClass(searchBorder, 'border-gray-300');

    removeClass(navSearchIcon, 'opacity-100');
    addClass(navSearchIcon, 'opacity-50');
}

function focusNavSearch(): void {
    document.getElementById('navSearch').focus();
}

function navSearchOnKeyUp(event, inputElement): void {
    if (event.key === 'Enter') {
        let value = inputElement.value;
        if (value !== '') {
            window.location.href = `/search?q=${value}`;
        }
    }
}
