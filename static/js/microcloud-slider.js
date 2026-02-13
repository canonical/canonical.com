// Slider that shows 3 resource items at a time
function threeItemSlider() {
  const activeItems = 3;
  let sliders = document.querySelectorAll(".js-slider");
  sliders.forEach((slider) => {
    initSlider(slider, activeItems);
  });
}

function initSlider(slider, activeItems) {
  let items = slider.querySelector(".js-slider--items").children;
  let resultsCount = slider.querySelector(".js-results-count");
  let length = items.length;
  let totalPages = Math.ceil(length / activeItems);
  let currentPage = 1;

  /** @type {HTMLElement} */
  let nextBtn = slider.querySelector(".js-slider--next");
  /** @type {HTMLElement} */
  let prevBtn = slider.querySelector(".js-slider--prev");

  updateButtonState(prevBtn, nextBtn, currentPage, totalPages);
  updateResultsCount(resultsCount, currentPage, totalPages);

  // Hide items > activeItems
  for (let i = activeItems; i < length; i++) {
    items[i].classList.add("u-hide");
  }

  if (nextBtn) {
    nextBtn.onclick = (e) => {
      if (currentPage < totalPages) {
        togglePageItems(items, currentPage, activeItems, false);
        currentPage += 1;
        togglePageItems(items, currentPage, activeItems, true);
        updateResultsCount(resultsCount, currentPage, totalPages);
        updateButtonState(prevBtn, nextBtn, currentPage, totalPages);
      }
    };
  }

  if (prevBtn) {
    prevBtn.onclick = (e) => {
      if (currentPage > 1) {
        togglePageItems(items, currentPage, activeItems, false);
        currentPage -= 1;
        togglePageItems(items, currentPage, activeItems, true);
        updateResultsCount(resultsCount, currentPage, totalPages);
        updateButtonState(prevBtn, nextBtn, currentPage, totalPages);
      }
    };
  }
}

function togglePageItems(items, page, activeItems, show) {
  const start = (page - 1) * activeItems;
  const end = Math.min(items.length, page * activeItems);
  for (let i = start; i < end; i++) {
    if (show) {
      items[i].classList.remove("u-hide");
    } else {
      items[i].classList.add("u-hide");
    }
  }
}

function updateResultsCount(resultsCount, page, total) {
  if (resultsCount) {
    resultsCount.innerHTML = `${page} of ${total} `;
  }
}

function updateButtonState(prevBtn, nextBtn, page, total) {
  if (total > 1) {
    nextBtn?.classList.remove("is-disabled");
  } else {
    nextBtn?.classList.add("is-disabled");
  }

  if (page === 1) {
    prevBtn?.classList.add("is-disabled");
  } else {
    prevBtn?.classList.remove("is-disabled");
  }

  if (page === total) {
    nextBtn?.classList.add("is-disabled");
  }
}

window.addEventListener("DOMContentLoaded", (e) => {
  threeItemSlider();
});
