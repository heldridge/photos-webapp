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

function setImage(index: number) {
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
}

function setNextImages(index: number) {
  while (galleryNextImages.hasChildNodes()) {
    galleryNextImages.removeChild(galleryNextImages.lastChild);
  }

  let nextPictures = [];
  if (allPictures.length - index < 9) {
    nextPictures = allPictures.slice(-9);
  } else {
    nextPictures = allPictures.slice(index, index + 9);
  }

  nextPictures.forEach(picture => {
    let pictureNode = document.createElement("div");
    pictureNode.className =
      "h-0 pb-1-3 w-under-1-3 border rounded overflow-hidden mt-5";

    let imageNode = document.createElement("img");
    imageNode.className = "object-cover";
    imageNode.src = picture.photo;

    pictureNode.appendChild(imageNode);

    galleryNextImages.appendChild(pictureNode);
  });
}

setImage(originalPictureIndex);
setNextImages(originalPictureIndex);
