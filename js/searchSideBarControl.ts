let addTagsButton = <HTMLAnchorElement>document.getElementById("addTagsButton");
let addTagsIcon = document.getElementById("addTagsIcon");
let addTagsInput = <HTMLInputElement>document.getElementById("addTagsInput");
let addTagsInputContainer = <HTMLDivElement>(
  document.getElementById("addTagsInputContainer")
);
let addTagsErrorMessage = <HTMLParagraphElement>(
  document.getElementById("addTagsErrorMessage")
);
let originalHREF = "";
if (addTagsButton !== null) {
  originalHREF = addTagsButton.href;
}

function addTagsInputOnKeyUp(
  e: onKeyUpEvent,
  currentQuery: string,
  maxTagLength: number,
  minTagLength: number,
  validTagRegex: string
) {
  // Listens for an "Enter" keypress in the add tags input,
  // on one directs the page to the page + tag
  if (e.key === "Enter") {
    let value = addTagsInput.value;
    if (value !== "") {
      // Don't change pages if input is empty
      let valid = validateTag(
        value,
        maxTagLength,
        minTagLength,
        new RegExp(validTagRegex)
      );

      if (valid.isValid) {
        // Only change pages if tag is valid
        let newHREF = originalHREF;
        if (currentQuery !== "") {
          newHREF += "+";
        }
        newHREF += value;
        window.location.href = newHREF;
      }
    }
  }
}

function addTagsInputUpdated(
  currentQuery: string,
  maxTagLength: number,
  minTagLength: number,
  validTagRegex: string
) {
  // Checks tag input to display message if tag is invalid
  let value = addTagsInput.value;

  // Disable link if tag is empty
  if (value === "") {
    console.log("HERE!!!!");
    addClass(addTagsButton, "disabled-button");
    removeClass(addTagsIcon, "text-black");
    addClass(addTagsIcon, "text-disabled");
    console.log(addTagsIcon.className);
  }

  let valid = validateTag(
    value,
    maxTagLength,
    minTagLength,
    new RegExp(validTagRegex)
  );
  if (valid.isValid) {
    addClass(addTagsInputContainer, "border-dt-0");
    removeClass(addTagsInputContainer, "border-red-500");
    addClass(addTagsErrorMessage, "hidden");
    let newHREF = originalHREF;
    if (currentQuery !== "" && value !== "") {
      newHREF += "+";
    }
    newHREF += value;
    addTagsButton.href = newHREF;

    if (value !== "") {
      removeClass(addTagsButton, "disabled-button");
      addClass(addTagsButton, "enabled-button");
      removeClass(addTagsIcon, "text-disabled");
      addClass(addTagsIcon, "text-black");
    }
  } else if (value !== "") {
    addTagsErrorMessage.innerHTML = valid.message;
    removeClass(addTagsInputContainer, "border-dt-0");
    addClass(addTagsInputContainer, "border-red-500");

    removeClass(addTagsErrorMessage, "hidden");
    addClass(addTagsButton, "disabled-button");

    removeClass(addTagsIcon, "text-black");
    addClass(addTagsIcon, "text-disabled");
  }
}
