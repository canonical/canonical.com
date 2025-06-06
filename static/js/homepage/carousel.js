const slides = document.querySelectorAll(".p-homepage-carousel--slide");
const navItems = document.querySelectorAll(".p--homepage-carousel-tabs__item");
const pauseBtn = document.querySelector(".pause-btn");

let currentIndex = 0;
let interval = null;
let isPaused = false;

function activateSlide(index) {
  slides.forEach((slide, i) => {
    slide.classList.toggle("u-hide", i !== index);
    slide.setAttribute("aria-hidden", i !== index);
    slide.setAttribute("tabindex", i === index ? "0" : "-1");
  });
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

pauseBtn.addEventListener("click", () => {
  isPaused = !isPaused;
  pauseBtn.textContent = isPaused ? "▶️" : "⏸";
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
});

// INIT
activateSlide(currentIndex);
startAutoRotate();
