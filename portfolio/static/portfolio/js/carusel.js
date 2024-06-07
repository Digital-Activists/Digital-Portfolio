let posts = document.querySelectorAll('.post');

for (let post of posts) {
    const slidesContainer = post.querySelector(".slides-container");
    const slide = slidesContainer.querySelector(".slide");
    const prevButton = post.querySelector(".slide-arrow-prev");
    const nextButton = post.querySelector(".slide-arrow-next");
    const slideWidth = slide.clientWidth;

    nextButton.addEventListener("click", () => {
        slidesContainer.scrollLeft += slideWidth;
    });

    prevButton.addEventListener("click", () => {
        slidesContainer.scrollLeft -= slideWidth;
    });
}

function full_view(ele) {
    let src = ele.parentElement.querySelector(".img-source").getAttribute("src");
    document.querySelector("#img-viewer").querySelector("img").setAttribute("src", src);
    document.querySelector("#img-viewer").style.display = "block";
}

function close_model() {
    document.querySelector("#img-viewer").style.display = "none";
}