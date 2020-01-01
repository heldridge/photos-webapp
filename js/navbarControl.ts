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
      message: ""
    };
  }
}

function navSearchOnFocus(): void {
  let searchBorder: HTMLElement = document.getElementById("navSearchBorder");
  let navSearchIcon: HTMLElement = document.getElementById("navSearchIcon");

  if (!hasClass(searchBorder, "border-red-500")) {
    removeClass(searchBorder, "border-gray-300");
    addClass(searchBorder, "border-blue-300");

    removeClass(navSearchIcon, "opacity-50");
    addClass(navSearchIcon, "opacity-100");
  }
}

function navSearchFocusOut(): void {
  let searchBorder: HTMLElement = document.getElementById("navSearchBorder");
  let navSearchIcon: HTMLElement = document.getElementById("navSearchIcon");

  if (!hasClass(searchBorder, "border-red-500")) {
    removeClass(searchBorder, "border-blue-300");
    addClass(searchBorder, "border-gray-300");

    removeClass(navSearchIcon, "opacity-100");
    addClass(navSearchIcon, "opacity-50");
  }
}

function focusNavSearch(): void {
  document.getElementById("navSearch").focus();
}

function navSearchOnKeyUp(
  event: onKeyUpEvent,
  inputElement,
  maxTagLength,
  minTagLength,
  validTagRegex
): void {
  if (event.key === "Enter") {
    let value = inputElement.value;
    if (
      value !== "" &&
      validateTag(value, maxTagLength, minTagLength, new RegExp(validTagRegex))
        .isValid
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
    new RegExp(invalidCharRegex, "g"),
    ""
  );
}
