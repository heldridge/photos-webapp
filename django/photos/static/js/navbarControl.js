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
