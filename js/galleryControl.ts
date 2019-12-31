// @ts-ignore
let allPictures: Array = allPicturesOutside;

// @ts-ignore
let originalPictureIndex = originalPictureIndexOutside;

let galleryNextImages: HTMLElement = document.getElementById(
  "gallery-next-images"
);

let galleryImageContainer = <HTMLDivElement>(
  document.getElementById("gallery-image-container")
);
let currentIndex = originalPictureIndex;
setImage(originalPictureIndex);

function setNextImages(index: number) {
  while (galleryNextImages.hasChildNodes()) {
    galleryNextImages.removeChild(galleryNextImages.lastChild);
  }

  let nextPictures = [];
  let startingIndex = 0;
  if (allPictures.length - index < 9) {
    nextPictures = allPictures.slice(-9);
    startingIndex = allPictures.length - 9;
    if (startingIndex < 0) {
      startingIndex = 0;
    }
  } else {
    nextPictures = allPictures.slice(index, index + 9);
    startingIndex = index;
  }

  let counter = 0;
  nextPictures.forEach(picture => {
    let pictureNode = document.createElement("button");
    pictureNode.className =
      "h-0 pb-1-3 w-under-1-3 rounded overflow-hidden mt-5 next-picture";

    let imageNode = document.createElement("img");
    imageNode.className = "object-cover";
    imageNode.src = picture.photo;

    pictureNode.appendChild(imageNode);

    galleryNextImages.appendChild(pictureNode);

    let newIndex = counter + startingIndex;
    pictureNode.onclick = () => setImage(newIndex);
    counter += 1;
  });
}

function setImage(index: number) {
  console.log(index);
  if (index < allPictures.length) {
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
