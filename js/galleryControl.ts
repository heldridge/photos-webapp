// @ts-ignore
let allPictures: Array = allPicturesOutside;

// @ts-ignore
let originalPictureIndex = originalPictureIndexOutside;

//@ts-ignore
let nextPageLink = nextPageLinkOutside;

let galleryNextImages: HTMLElement = document.getElementById(
  "gallery-next-images"
);

let galleryImageContainer = <HTMLDivElement>(
  document.getElementById("gallery-image-container")
);
let currentIndex = originalPictureIndex;
setImage(originalPictureIndex);

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
  while (galleryNextImages.hasChildNodes()) {
    galleryNextImages.removeChild(galleryNextImages.lastChild);
  }

  let nextPictures = [];
  let startingIndex = 0;
  let renderNextPageButton = false;
  if (allPictures.length - index < 9) {
    nextPictures = allPictures.slice(-8);
    startingIndex = allPictures.length - 8;
    if (startingIndex < 0) {
      startingIndex = 0;
    }
    renderNextPageButton = true;
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
    pictureNode.onclick = () => setImage(newIndex);
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
}

function setImage(index: number) {
  console.log(index);
  if (index < allPictures.length && galleryImageContainer) {
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
}

function nextPicture() {
  if (currentIndex + 1 < allPictures.length) {
    setImage(currentIndex + 1);
  }
}

function previousPicture() {
  if (currentIndex > 0) {
    setImage(currentIndex - 1);
  }
}
