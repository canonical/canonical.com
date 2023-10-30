// Slider that shows 3 resource items at a time
function threeItemSlider() {
  const nextBtn = document.querySelector('.js-slider--next');
  const prevBtn = document.querySelector('.js-slider--prev');
  const items = document.querySelector('.js-slider--items').children;
  let resultsCount = document.getElementById('js-results-count');
  const activeItems = 3;
  const length = items.length; 
  let index = 0;
  let windowIndex = (index + activeItems * 2);
  let windowLimit = windowIndex - (windowIndex - length);
  resultsCount.innerHTML = `${activeItems} of ${length} `;
  
  if (index == 0 ) {
    prevBtn.classList.add('is-disabled');
  }
  
  // Handles next button click and disables button if there are no more items to show
  nextBtn.onclick = (e) => {
    if (index < length - 1){
      for (let i = index; i < index + activeItems; i++) {
        items[i].classList.add('u-hide');
      }
  
      for (let i = index + activeItems; i < (windowLimit); i++) {
        items[i].classList.remove('u-hide');
      }
      index += activeItems;
  
      resultsCount.innerHTML = `${windowLimit} of ${length} `;
      prevBtn.classList.remove('is-disabled');
    } 

    if (index >= length - 1){
      nextBtn.classList.add('is-disabled');
    }  
  }

  // Handles prev button click and disables button if at beginning of list
  prevBtn.onclick = (e) => {
    if (index >= activeItems) {
      for (let i = index; i < (windowLimit); i++) {
        items[i].classList.add('u-hide');
      }
  
      for (let i = index - activeItems; i < index; i++) {
        items[i].classList.remove('u-hide');
      }
      index -= activeItems;
    }

    if (index == 0 ) {
      prevBtn.classList.add('is-disabled');

      if (length) {
        nextBtn.classList.remove('is-disabled');
      }
    } 

    resultsCount.innerHTML = `${activeItems} of ${length} `;
  }
}

window.addEventListener("DOMContentLoaded", (e) => {
  threeItemSlider();
});
