let addTagsButton = <HTMLAnchorElement>document.getElementById('addTagsButton');
let addTagsInput = <HTMLInputElement>document.getElementById('addTagsInput');
let originalHREF = addTagsButton.href;

function addTagsInputUpdated() {
  let value = addTagsInput.value;
  if (value !== '') {
    addTagsButton.href = `${originalHREF}+${addTagsInput.value}`;
  } else {
    addTagsButton.href = originalHREF;
  }
}
