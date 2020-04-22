let currentPage = 1;

let loader = document.createElement('div');
loader.className = 'la-ball-clip-rotate la-sm la-dark ml-1';
loader.appendChild(document.createElement('div'));

function fetchNextPage(source: HTMLButtonElement) {
    source.appendChild(loader);
    addClass(source, 'pointer-events-none');

    let request = new Request(`/pictures/tags?page=${currentPage + 1}`);

    fetch(request, {
        method: 'GET',
        mode: 'same-origin',
    })
        .then((response) => {
            return response.json();
        })
        .then((data) => {
            let tagsContainer = document.getElementById('tagsContainer');
            data.tags.forEach((tag) => {
                let tagElement = document.createElement('a');
                tagElement.className =
                    'tag bg-gray-300 hover:bg-gray-400 rounded py-2 px-3 text mr-5 font-medium text-lg mb-5 bg-tag hover:bg-tag-hover text-tag hover:text-tag-hover';
                tagElement.href = `/search?tags=${tag.title}`;
                let tagText = document.createElement('span');
                tagText.className = 'opacity-medium-emphasis';
                tagText.innerHTML = `${tag.title}: ${tag.count}`;

                tagElement.appendChild(tagText);
                tagsContainer.appendChild(tagElement);
            });

            if (!data.more_left) {
                addClass(source, 'bg-button-disabled');
                removeClass(source, 'text-black');

                let fetchNextPageText = document.getElementById(
                    'fetchNextPageText'
                );
                addClass(fetchNextPageText, 'text-disabled');
                addClass(fetchNextPageText, 'opacity-disabled');
            } else {
                removeClass(source, 'pointer-events-none');
            }
            source.removeChild(source.lastChild);

            currentPage += 1;
        });
}

// <a href="{% url 'search' %}?tags={{ tag.title }}" class="tag bg-gray-300 hover:bg-gray-400 rounded py-2 px-3 text mr-5 font-medium text-lg mb-5 bg-tag hover:bg-tag-hover text-tag hover:text-tag-hover">
//     <span class="opacity-medium-emphasis">{{ tag.title }}: {{ tag.count }}</span>
// </a>
