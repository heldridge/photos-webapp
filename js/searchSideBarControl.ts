let addTagsButton = <HTMLAnchorElement>document.getElementById('addTagsButton');
let addTagsInput = <HTMLInputElement>document.getElementById('addTagsInput');
console.log(addTagsInput);
let originalHREF = addTagsButton.href;

function addTagsInputUpdated() {
  addTagsButton.href = `${originalHREF}+${addTagsInput.value}`;
}
