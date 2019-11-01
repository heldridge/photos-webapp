// Class manipulation functions from: https://jaketrent.com/post/addremove-classes-raw-javascript/
function hasClass(ele,cls) {
    return !!ele.className.match(new RegExp('(\\s|^)'+cls+'(\\s|$)'));
}

function addClass(ele,cls) {
    if (!hasClass(ele,cls)) ele.className += " "+cls;
}

function removeClass(ele,cls) {
    if (hasClass(ele,cls)) {
        var reg = new RegExp('(\\s|^)'+cls+'(\\s|$)');
        ele.className=ele.className.replace(reg,' ');
    }
}

function setNavSearchBorderGray() {
    let searchBorder = document.getElementById("navSearchBorder");
    removeClass(searchBorder, 'border-blue-300');
    addClass(searchBorder, 'border-gray-300');
}

function setNavSearchBorderBlue() {
    let searchBorder = document.getElementById("navSearchBorder");
    removeClass(searchBorder, 'border-gray-300');
    addClass(searchBorder, 'border-blue-300');
}

function setNavSearchIconOpacity50() {
    let navSearchIcon = document.getElementById("navSearchIcon");
    removeClass(navSearchIcon, 'opacity-100');
    addClass(navSearchIcon, 'opacity-50');
}

function setNavSearchIconOpacity100() {
    let navSearchIcon = document.getElementById("navSearchIcon");
    removeClass(navSearchIcon, 'opacity-50');
    addClass(navSearchIcon, 'opacity-100');
}

function navSearchFocus() {
    setNavSearchBorderBlue();
    setNavSearchIconOpacity100();
}

function navSearchFocusOut() {
    setNavSearchBorderGray();
    setNavSearchIconOpacity50();
}
