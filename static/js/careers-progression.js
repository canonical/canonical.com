window.addEventListener("DOMContentLoaded", (e) => {
  scrollAnimation();
  standardCarousel();
  carousel3DTestimonials();
  removeAutoplay();
});

/**
 * Removes video autoplay if reduced motion is set
 */
function removeAutoplay() {
  const reducedMotion = window.matchMedia(
    "(prefers-reduced-motion: reduce)"
  ).matches;
  if (reducedMotion) {
    const videoElement = document.querySelectorAll("video");
    videoElement.forEach((element) => {
      element.removeAttribute("autoplay");
    });
  }
}

function scrollAnimation() {
  // Replicate homepage scroll animations
  // https://github.com/canonical/canonical.com/blob/main/templates/index.html#L587
  /** @type {NodeListOf<HTMLElement>} */
  const elementsToAnimate = document.querySelectorAll("[data-animation]");
  let windowHeight = window.innerHeight;
  window.addEventListener("scroll", () => {
    elementsToAnimate.forEach((element) => {
      var positionFromTop = element.getBoundingClientRect().top;
      if (positionFromTop - windowHeight <= 0) {
        if (element.dataset.animation) {
          element.classList.add(element.dataset.animation);
        }
        element.removeAttribute("data-animation");
      }
    });
  });
}

/**
 * Standard carousel that shows the career progression
 * at Canonical.
 */
function standardCarousel() {
  const previousButton = document.querySelector(
    ".p-careers-progression-carousel__previous"
  );
  const nextButton = document.querySelector(
    ".p-careers-progression-carousel__next"
  );
  const slidesContainer = document.querySelectorAll(
    ".p-careers-progression-carousel__slides"
  );
  let slideDots = document.querySelectorAll(
    ".p-careers-progression-carousel__navigation .p-careers-progression-carousel__selector"
  );
  let currentIndex = 0;
  // Use dots as source of truth
  // other elements have clones
  const totalSlides = slideDots.length;

  previousButton.addEventListener("click", previousSlide);
  nextButton.addEventListener("click", nextSlide);

  function updateSlide() {
    if (currentIndex <= -1) {
      currentIndex = totalSlides - 1;
    }
    if (currentIndex >= totalSlides) {
      currentIndex = 0;
    }
    goToSlide(currentIndex, (ms = "0"));
  }

  for (let i = 0; i < slidesContainer.length; i++) {
    slidesContainer[i].addEventListener("transitionend", updateSlide);
    slidesContainer[i].append(slidesContainer[i].children[0].cloneNode(true));
  }

  // Set up the slide dot behaviors
  slideDots.forEach((dot) => {
    dot.addEventListener("click", (e) => {
      /** @type {HTMLElement} */
      const target = e.target;
      currentIndex = target.tabIndex;
      goToSlide(currentIndex);
    });
  });

  function previousSlide() {
    if (currentIndex <= -1) return;
    currentIndex -= 1;
    goToSlide(currentIndex);
  }

  function nextSlide() {
    if (currentIndex >= totalSlides) return;
    currentIndex += 1;
    goToSlide(currentIndex);
  }

  // Go to selected slide
  // Used both for dots and chevron navigation
  function goToSlide(index, ms = "0.75") {
    currentIndex = index;
    for (let i = 0; i < slidesContainer.length; i++) {
      for (let j = 0; j < slidesContainer[i].children.length; j++) {
        /** @type {HTMLElement} */
        const child = slidesContainer[i].children[j];
        child.style.transitionDuration = `${ms}s`;
        child.style.transform = `translateX(-${
          child.offsetWidth * index
        }px)`;
      }
    }

    // Set aria-current attribute on the correct slide dot
    // this will also apply styles
    slideDots.forEach((element) => {
      if (element) {
        element.setAttribute("aria-current", false);
      }
    });
    slideDots[currentIndex].setAttribute("aria-current", true);
  }
}

function carousel3DTestimonials(showItems = 3) {
  /** @type {HTMLElement | null} */
  const next = document.querySelector("#next-testimonial");
  /** @type {HTMLElement | null} */
  const previous = document.querySelector("#previous-testimonial");
  /** @type {NodeListOf<HTMLElement>} */
  const carouselItems = document.querySelectorAll(".p-3d-carousel__item");
  /** @type {NodeListOf<HTMLElement>} */
  const goToSlideButton = document.querySelectorAll(".js-go-to-slide");

  const transition = "0.75s ease-out";

  // initial states
  let itemNum = carouselItems.length;
  let activeItem = carouselItems[0];
  let activeIndex = 0;
  let rItem = carouselItems[1];
  let lItem = carouselItems[itemNum - 1];

  // -80 to adjust for responsive design
  let itemWidth = activeItem.clientWidth - 100;
  let radius = (showItems * itemWidth) / 2;

  let rHead = 2; // index of the next item to show on the right side
  let lHead = itemNum - 2; // index of the next item to show on the left side

  shiftToActive(activeItem);
  shiftToLeft(lItem);
  shiftToRight(rItem);

  for (let i = 2; i < itemNum - 1; i++) {
    shiftToBack(carouselItems[i]);
  }

  next.onclick = (e) => {
    if (activeIndex >= itemNum - 1) {
      activeIndex = 0;
    } else {
      activeIndex = activeIndex + 1;
    }

    goToSlideButton.forEach((element) =>
      element.setAttribute("aria-current", false)
    );
    goToSlideButton[activeIndex].setAttribute("aria-current", true);
    moveRight();
  };

  previous.onclick = (e) => {
    if (activeIndex <= 0) {
      activeIndex = itemNum - 1;
    } else {
      activeIndex = activeIndex - 1;
    }

    goToSlideButton.forEach((element) =>
      element.setAttribute("aria-current", false)
    );
    goToSlideButton[activeIndex].setAttribute("aria-current", true);
    moveLeft();
  };

  goToSlideButton.forEach((elem) => {
    elem.addEventListener("click", (e) => {
      const index = +elem.dataset.target;
      let count = Math.abs(index - activeIndex);
      if (index < activeIndex) {
        // shift right
        for (let si = 0; si < count; si++) {
          moveRight();
          activeIndex = index;
        }
        goToSlideButton[index].setAttribute("aria-current", true);
        goToSlideButton.forEach((element) =>
          element.setAttribute("aria-current", false)
        );
      } else {
        // shift left
        for (let li = 0; li < count; li++) {
          moveLeft();
          activeIndex = index;
        }
        goToSlideButton[index].setAttribute("aria-current", true);
        goToSlideButton.forEach((element) =>
          element.setAttribute("aria-current", false)
        );
      }
    });
  });

  function moveRight() {
    shiftToBack(rItem);
    shiftToRight(activeItem);
    shiftToActive(lItem);

    rItem = activeItem;
    activeItem = lItem;

    lItem = carouselItems[lHead--];
    rHead--;

    if (lHead < 0) {
      lHead = itemNum - 1;
    }

    if (rHead < 0) {
      rHead = itemNum - 1;
    }

    shiftToLeft(lItem);
  }

  function moveLeft() {
    shiftToBack(lItem);
    shiftToLeft(activeItem);
    shiftToActive(rItem);

    lItem = activeItem;
    activeItem = rItem;

    rItem = carouselItems[rHead++];
    lHead++;
    if (lHead >= itemNum) lHead = 0;
    if (rHead >= itemNum) rHead = 0;
    shiftToRight(rItem);
  }

  function shiftToRight(elem) {
    elem.ariaCurrent = "false";
    elem.style.filter = "blur(4px)";
    elem.style.transform = `translateX(${
      radius - itemWidth / 2
    }px) translateZ(400px)`;
    elem.style["z-index"] = `${itemNum - 10}`;
    elem.style.transition = transition;
  }

  function shiftToLeft(elem) {
    elem.ariaCurrent = "false";
    elem.style.filter = "blur(4px)";
    elem.style.transform = `translateX(${
      -radius + itemWidth / 2
    }px) translateZ(400px)`;
    elem.style["z-index"] = `${itemNum - 10}`;
    elem.style.transition = transition;
  }

  function shiftToActive(elem) {
    elem.ariaCurrent = "true";
    elem.style.filter = "none";
    elem.style.transform = "translateX(0) scale(1.25) translateZ(800px)";
    elem.style["z-index"] = `${itemNum}`;
    elem.style.transition = transition;
  }

  function shiftToBack(elem) {
    elem.ariaCurrent = "false";
    elem.style.filter = "blur(4px)";
    elem.style.transform = "translateX(0) translateZ(0)";
    elem.style["z-index"] = `${itemNum - 20}`;
    elem.style.transition = transition;
  }
}
