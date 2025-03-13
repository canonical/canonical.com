// Slider that shows 3 resource items at a time
function threeItemSlider() {
  const nextBtn = document.querySelector(".js-slider--next");
  const prevBtn = document.querySelector(".js-slider--prev");
  const items = document.querySelector(".js-slider--items").children;
  let resultsCount = document.getElementById("js-results-count");
  
  const activeItems = 3;
  const length = items.length;
  let totalPages = Math.ceil(length / activeItems);
  let currentPage = 1;


  if (resultsCount) {
    resultsCount.innerHTML = `${currentPage} of ${totalPages} `;
  }

  if (currentPage == 1) {
    prevBtn.classList.add("is-disabled");
  }

  // Handles next button click and disables button if there are no more items to show
  if (nextBtn) {
    nextBtn.onclick = (e) => {
      console.log(currentPage);
      if (currentPage < totalPages) {
        for (let i = (currentPage-1)*activeItems; i < currentPage * activeItems; i++) {
          items[i].classList.add("u-hide");
        }

        let windowLimit = Math.min(length, (currentPage+1) * activeItems);

        for (let i = currentPage*activeItems; i < windowLimit; i++) {
          items[i].classList.remove("u-hide");
        }
        
        currentPage += 1;

        resultsCount.innerHTML = `${currentPage} of ${totalPages} `;
        prevBtn.classList.remove("is-disabled");
      }

      if (currentPage==totalPages) {
        nextBtn.classList.add("is-disabled");
      }

      jumpToTop();
    };
  }

  // Handles prev button click and disables button if at beginning of list
  if (prevBtn) {
    prevBtn.onclick = (e) => {

      if (currentPage > 1) {

        let windowLimit = Math.min(length, currentPage * activeItems);
        for (let i = (currentPage-1)*activeItems; i < windowLimit; i++) {
          items[i].classList.add("u-hide");
        }
        currentPage -= 1;

        for (let i = (currentPage-1)*activeItems; i < currentPage * activeItems; i++) {
          items[i].classList.remove("u-hide");
        }

      }

      if (currentPage == 1) {
        prevBtn.classList.add("is-disabled");

        if (length > activeItems) {
          nextBtn.classList.remove("is-disabled");
        }
      }

      resultsCount.innerHTML = `${currentPage} of ${totalPages} `;
    };
  }
}

// Scrolls to top of section on tablet/mobile
function jumpToTop() {
  if (window.screen.width < 1036) {
    document.getElementById("videos-and-webinars").scrollIntoView();
  }
}

window.addEventListener("DOMContentLoaded", (e) => {
  threeItemSlider();
});
