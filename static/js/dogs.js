export class DogPicture extends HTMLElement {
  constructor() {
    super();
    this.img = document.createElement("img");
    this.appendChild(this.img);
  }

  connectedCallback() {
    this.breed = this.getAttribute("breed") || null;
    this.loadRandomImage(this.breed);
  }

  loadRandomImage(breed) {
    let url = "https://dog.ceo/api/breeds/image/random";
    if (breed) {
      url =
        "https://dog.ceo/api/breed/" + breed.toLowerCase() + "/images/random";
    }

    fetch(url)
      .then((response) => response.json())
      .then((data) => {
        this.img.setAttribute("src", data.message);
        if (breed) {
          this.img.setAttribute("alt", "picture of a cute " + breed + " dog");
        } else {
          this.img.setAttribute("alt", "picture of a cute dog");
        }
      });
  }
}

customElements.define("dog-picture", DogPicture);
