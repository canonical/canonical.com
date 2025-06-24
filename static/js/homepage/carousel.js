const slides = document.querySelectorAll(".p-homepage-carousel--slide");
const navItems = document.querySelectorAll(".p-homepage-carousel-tabs__item");
const pauseBtns = document.querySelectorAll(".pause-btn");

let currentIndex = 0;
let interval = null;
let isPaused = false;

function activateSlide(index) {
  slides.forEach((slide, i) => {
    slide.classList.toggle("u-hide", i !== index);
    slide.setAttribute("aria-hidden", i !== index);
    slide.setAttribute("tabindex", i === index ? "0" : "-1");
  });
  const slide_progress_bar = slides[index].querySelector(".progress-bar");
  if (slide_progress_bar) {
    slide_progress_bar.style.animation = !isPaused
      ? "progressBarAnim 8s linear forwards"
      : "none";
  }
  navItems.forEach((nav, i) => {
    nav.setAttribute("aria-selected", i === index);
    const simpleLine = nav.querySelector("p-rule--muted");
    if (simpleLine) simpleLine.classList.toggle("u-hide", i === index);
    const bar = nav.querySelector(".progress-bar");
    if (bar)
      bar.style.animation =
        i === index && !isPaused
          ? "progressBarAnim 8s linear forwards"
          : "none";
  });
  currentIndex = index;
}

function nextSlide() {
  const next = (currentIndex + 1) % slides.length;
  activateSlide(next);
}
function pauseSlide() {
  isPaused = !isPaused;
  pauseBtns.forEach(
    (pauseBtn) =>
      {pauseBtn.querySelector("img").src = isPaused
        ? "https://assets.ubuntu.com/v1/58c707b0-play.svg"
        : "https://assets.ubuntu.com/v1/398d9c17-pause.svg"
      pauseBtn.setAttribute("aria-label", isPaused
        ? "Play carousel"
        : "Pause carousel");
      }
  );
  if (isPaused) {
    clearInterval(interval);
    // stop progress bar animation
    document
      .querySelectorAll(".progress-bar")
      .forEach((bar) => (bar.style.animation = "none"));
  } else {
    activateSlide(currentIndex); // restart animation
    startAutoRotate();
  }
}

function startAutoRotate() {
  if (interval) clearInterval(interval);
  interval = setInterval(nextSlide, 8000);
}

navItems.forEach((nav) => {
  nav.addEventListener("click", () => {
    const index = parseInt(nav.getAttribute("data-index"), 10);
    activateSlide(index);
    if (!isPaused) {
      startAutoRotate(); // restart timer
    }
  });
});

pauseBtns.forEach((pauseBtn) => pauseBtn.addEventListener("click", pauseSlide));

// Keyboard navigation
document.addEventListener("keydown", (event) => {
  if (event.key === "ArrowRight") {
    nextSlide();
  } else if (event.key === "ArrowLeft") {
    const prev = (currentIndex - 1 + slides.length) % slides.length;
    activateSlide(prev);
    if (!isPaused) {
      startAutoRotate(); // restart timer
    }
  } else if (event.key === " ") {
    pauseSlide();
  }
});

// arrow buttons
const arrowNext = document.querySelector(".p-homepage-carousel__next");
const arrowPrev = document.querySelector(".p-homepage-carousel__previous");
arrowNext.addEventListener("click", () => {
  nextSlide();
  if (!isPaused) {
    startAutoRotate(); // restart timer
  }
});
arrowPrev.addEventListener("click", () => {
  const prev = (currentIndex - 1 + slides.length) % slides.length;
  activateSlide(prev);
  if (!isPaused) {
    startAutoRotate(); // restart timer
  }
});

// INIT
activateSlide(currentIndex);
startAutoRotate();
