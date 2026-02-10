// Slider that shows 3 resource items at a time
function threeItemSlider() {
  let activePages = [];
  const activeItems = 3;
  let sliders = document.querySelectorAll(".js-slider");
  for (let i = 0; i < sliders.length; i++) {
    let slider = sliders[i];
    let items = slider.querySelector(".js-slider--items").children;
    let resultsCount = slider.querySelector(".js-results-count");
    let length = items.length;
    let totalPages = Math.ceil(length / activeItems);
    activePages.push(1);
    if (resultsCount) {
      resultsCount.innerHTML = `1 of ${totalPages} `;
    }
    /** @type {HTMLElement} */
    let nextBtn = slider.querySelector(".js-slider--next");
    /** @type {HTMLElement} */
    let prevBtn = slider.querySelector(".js-slider--prev");
    let currentPage = activePages[i];

    if (totalPages > 1) {
      nextBtn.classList.remove("is-disabled");
    }
    if (currentPage == 1) {
      prevBtn.classList.add("is-disabled");
    }

    for (let i = 0; i < length; i++) {
      if (i >= activeItems) {
        items[i].classList.add("u-hide");
      }
    }

    if (nextBtn) {
      nextBtn.onclick = (e) => {
        if (currentPage < totalPages) {
          for (
            let i = (currentPage - 1) * activeItems;
            i < currentPage * activeItems;
            i++
          ) {
            items[i].classList.add("u-hide");
          }

          let windowLimit = Math.min(length, (currentPage + 1) * activeItems);

          for (let i = currentPage * activeItems; i < windowLimit; i++) {
            items[i].classList.remove("u-hide");
          }

          currentPage += 1;

          resultsCount.innerHTML = `${currentPage} of ${totalPages} `;
          prevBtn.classList.remove("is-disabled");
        }

        if (currentPage == totalPages) {
          nextBtn.classList.add("is-disabled");
        }
      };
    }

    if (prevBtn) {
      prevBtn.onclick = (e) => {
        if (currentPage > 1) {
          let windowLimit = Math.min(length, currentPage * activeItems);
          for (let i = (currentPage - 1) * activeItems; i < windowLimit; i++) {
            items[i].classList.add("u-hide");
          }
          currentPage -= 1;

          for (
            let i = (currentPage - 1) * activeItems;
            i < currentPage * activeItems;
            i++
          ) {
            items[i].classList.remove("u-hide");
          }
        }

        resultsCount.innerHTML = `${currentPage} of ${totalPages} `;
        nextBtn.classList.remove("is-disabled");

        if (currentPage == 1) {
          prevBtn.classList.add("is-disabled");
        }
      };
    }
  }
}

window.addEventListener("DOMContentLoaded", (e) => {
  threeItemSlider();
});
