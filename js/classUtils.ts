// Class manipulation functions from: https://jaketrent.com/post/addremove-classes-raw-javascript/
function hasClass(ele: HTMLElement, cls: string): boolean {
  return !!ele.className.match(new RegExp("(\\s|^)" + cls + "(\\s|$)"));
}

function addClass(ele: any, cls: string): void {
  if (!hasClass(ele, cls)) ele.className += " " + cls;
}

function removeClass(ele: any, cls: string): void {
  if (hasClass(ele, cls)) {
    var reg: RegExp = new RegExp("(\\s|^)" + cls + "(\\s|$)");
    ele.className = ele.className.replace(reg, " ");
  }
}
