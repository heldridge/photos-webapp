let addTagsButton = <HTMLAnchorElement>document.getElementById('addTagsButton');
let addTagsInput = <HTMLInputElement>document.getElementById('addTagsInput');
let originalHREF = addTagsButton.href;

function addTagsInputUpdated(currentQuery: string) {
  let value = addTagsInput.value;

  let newHREF = originalHREF;
  if (currentQuery !== '' && value !== '') {
    newHREF += '+';
  }
  newHREF += value;
  addTagsButton.href = newHREF;
}
