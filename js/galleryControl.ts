// @ts-ignore
let allPictures: Array = allPicturesOutside;
//@ts-ignore
let originalPictureIndex = originalPictureIndexOutside;
//@ts-ignore
let nextPageLink = nextPageLinkOutside;
//@ts-ignore
let previousPageLink = previousPageLinkOutside;
//@ts-ignore
let renderNextButton = renderNextButtonOutside;
//@ts-ignore
let renderPreviousButton = renderPreviousButtonOutside;

let galleryNextImages: HTMLElement = document.getElementById(
  "gallery-next-images"
);

let galleryImageContainer = <HTMLDivElement>(
  document.getElementById("gallery-image-container")
);
let currentIndex = originalPictureIndex;
setImage(originalPictureIndex, "replace");

/*
Next Images:

<div id="gallery-next-images">

  <button class="h-0 pb-1-3 w-under-1-3 rounded overflow-hidden mt-5 next-picture">
    <img class="object-cover">
  </button>
  ...
  <a class="w-under-1-3 rounded overflow-hidden mt-5 bg-gray-300 hover:bg-gray-500 flex flex-col justify-center items-center text-xl cursor-pointer">
    Next Page
    <i class="fas fa-arrow-right"></i>
  </a>

</div>
*/

function setNextImages(index: number) {
  if (galleryNextImages) {
    while (galleryNextImages.hasChildNodes()) {
      galleryNextImages.removeChild(galleryNextImages.lastChild);
    }

    let nextPictures = [];
    let startingIndex = 0;
    let renderNextPageButton = false;
    if (allPictures.length - index < 9) {
      let numNextImages = renderNextButton ? 8 : 9;

      nextPictures = allPictures.slice(-numNextImages);
      startingIndex = allPictures.length - numNextImages;
      if (startingIndex < 0) {
        startingIndex = 0;
      }
      renderNextPageButton = renderNextButton;
    } else {
      nextPictures = allPictures.slice(index, index + 9);
      startingIndex = index;
    }

    let counter = 0;
    nextPictures.forEach(picture => {
      let pictureNode = document.createElement("button");
      pictureNode.className =
        "h-0 pb-1-3 w-under-1-3 rounded overflow-hidden mt-5 next-picture";

      if (counter + startingIndex === index) {
        pictureNode.className += " selected-picture";
      }

      let imageNode = document.createElement("img");
      imageNode.className = "object-cover";
      imageNode.src = picture.photo;

      pictureNode.appendChild(imageNode);

      galleryNextImages.appendChild(pictureNode);

      let newIndex = counter + startingIndex;
      pictureNode.onclick = () => setImage(newIndex, "push");
      counter += 1;
    });

    if (renderNextPageButton) {
      let nextPageButton = document.createElement("a");
      nextPageButton.className =
        "w-under-1-3 rounded overflow-hidden mt-5 border-2 border-gray-500 bg-gray-300 hover:bg-gray-500 flex flex-col justify-center items-center text-xl cursor-pointer";
      nextPageButton.href = nextPageLink;

      let message = document.createTextNode("Next Page");
      nextPageButton.appendChild(message);
      let iconNode = document.createElement("i");
      iconNode.className = "fas fa-arrow-right";
      nextPageButton.appendChild(iconNode);
      galleryNextImages.appendChild(nextPageButton);
    }

    if (renderPreviousButton && (nextPictures.length <= 7 || index === 0)) {
      let previousPageButton = document.createElement("a");
      previousPageButton.className =
        "w-under-1-3 rounded overflow-hidden mt-5 border-2 border-gray-500 bg-gray-300 hover:bg-gray-500 flex flex-col justify-center items-center cursor-pointer";
      previousPageButton.href = previousPageLink;
      let message = document.createTextNode("Previous Page");
      previousPageButton.appendChild(message);
      let iconNode = document.createElement("i");
      iconNode.className = "fas fa-arrow-left";
      previousPageButton.appendChild(iconNode);
      galleryNextImages.insertBefore(
        previousPageButton,
        galleryNextImages.firstChild
      );
      if (nextPictures.length >= 9) {
        galleryNextImages.removeChild(galleryNextImages.lastChild);
      }
    }

    let totalNextImages = nextPictures.length;
    if (renderNextPageButton) {
      totalNextImages += 1;
    }

    for (let i = 0; i < 9 - totalNextImages; i++) {
      let placeholderNode = document.createElement("div");
      placeholderNode.className = "w-under-1-3";
      galleryNextImages.appendChild(placeholderNode);
    }
  }
}

function setImage(index: number, stateAction: string = "") {
  if (index < allPictures.length) {
    if (galleryImageContainer) {
      // Remove children
      while (galleryImageContainer.hasChildNodes()) {
        galleryImageContainer.removeChild(galleryImageContainer.lastChild);
      }
      // Add new child
      let image = document.createElement("img");
      image.src = allPictures[index].photo;
      galleryImageContainer.appendChild(image);
    }
    setNextImages(index);
    currentIndex = index;

    let query = getUrlParameter("q");
    let after = getUrlParameter("after");
    let before = getUrlParameter("before");

    if (stateAction) {
      let newState = `?p=${allPictures[index].public_id}`;
      if (query) {
        newState += `&q=${query}`;
      }
      if (after) {
        newState += `&after=${after}`;
      }
      if (before) {
        newState += `&before=${before}`;
      }

      if (stateAction === "push") {
        history.pushState({ index: index }, "", newState);
      } else if (stateAction === "replace") {
        history.replaceState({ index: index }, "", newState);
      }
    }
  }
}

function nextPicture() {
  if (currentIndex + 1 < allPictures.length) {
    setImage(currentIndex + 1, "push");
  }
}

function previousPicture() {
  if (currentIndex > 0) {
    setImage(currentIndex - 1, "push");
  }
}

window.onpopstate = function(event: PopStateEvent) {
  console.log("HERE BOYS");
  if (event.state) {
    console.log("event had a state");
    setImage(event.state.index);
  } else {
    // console.log("event did not have a state");
    // history.go(-1);
  }
};

console.log(renderNextButton);
console.log(renderPreviousButton);
