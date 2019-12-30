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

setImage(originalPictureIndex);

let nextPictures = [];
if (allPictures.length - originalPictureIndex < 9) {
  nextPictures = allPictures.slice(-9);
} else {
  nextPictures = allPictures.slice(
    originalPictureIndex,
    originalPictureIndex + 9
  );
}

console.log(nextPictures);

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

/*
<div class="border-2 rounded-b border-gray-300 mx-6 pb-5 px-1 flex flex-row flex-wrap justify-around" id="gallery-next-images">
    {% if pictures %}
        {% for picture in pictures %}
            {% if forloop.counter0 == current_picture_index%}
                <div class="h-0 pb-1-3 w-under-1-3 border-2 border-green-300 rounded overflow-hidden mt-5">
                    <img src="{{ picture.photo }}" alt="" class="object-cover">
                </div>
            {% else %}
                <div class="h-0 pb-1-3 w-under-1-3 border rounded overflow-hidden mt-5">
                    <img src="{{ picture.photo }}" alt="" class="object-cover">
                </div>
            {% endif %}

        {% endfor %}
    {% endif %}
    {% for placeholder in grid_placeholders %}
        <div class="h-0 w-under-1-3"></div>
    {% endfor %}
</div>

 if len(data["photos"]) - current_picture_index < 9:
        pictures = data["photos"][-9:]
    else:
        pictures = data["photos"][current_picture_index : current_picture_index + 9]
*/
