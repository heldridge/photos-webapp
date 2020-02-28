// Class manipulation functions from: https://jaketrent.com/post/addremove-classes-raw-javascript/
function hasClass(ele: Element, cls: string): boolean {
    return !!ele.className.match(new RegExp('(\\s|^)' + cls + '(\\s|$)'));
}

function addClass(ele: Element, cls: string): void {
    if (!hasClass(ele, cls)) ele.className += ' ' + cls;
}

function removeClass(ele: Element, cls: string): void {
    if (hasClass(ele, cls)) {
        var reg: RegExp = new RegExp('(\\s|^)' + cls + '(\\s|$)');
        ele.className = ele.className.replace(reg, ' ');
    }
}
