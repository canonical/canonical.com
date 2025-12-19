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
      ? "progress-bar-anim 8s linear forwards"
      : "none";
  }
  navItems.forEach((nav, i) => {
    nav.setAttribute("aria-selected", i === index);
    const bar = nav.querySelector(".progress-bar");
    if (bar)
      bar.style.animation =
        i === index && !isPaused
          ? "progress-bar-anim 8s linear forwards"
          : "none";
    if (isPaused) {
      bar.style.width = i === index && isPaused ? "100%" : "0%"; // Ensure the progress bar is full when paused
    }
  });
  currentIndex = index;
}

function nextSlide() {
  const next = (currentIndex + 1) % slides.length;
  activateSlide(next);
}

function pause_play_Slide() {
  isPaused = !isPaused;
  pauseBtns.forEach((pauseBtn) => {
    pauseBtn.querySelector("img").src = isPaused
      ? "https://assets.ubuntu.com/v1/58c707b0-play.svg"
      : "https://assets.ubuntu.com/v1/398d9c17-pause.svg";
    pauseBtn.setAttribute(
      "aria-label",
      isPaused ? "Play carousel" : "Pause carousel"
    );
  });
  if (isPaused) {
    clearInterval(interval);
    // stop progress bar animation
    document
      .querySelectorAll(".progress-bar")
      .forEach((bar) => (bar.style.animation = "none"));
    navItems[currentIndex].querySelector(".progress-bar").style.width = "100%"; // Ensure the current slide's progress bar is full
  } else {
    activateSlide(currentIndex); // restart animation
    startAutoRotate();
  }
}

function startAutoRotate() {
  if (interval) clearInterval(interval);
  interval = setInterval(nextSlide, 8000);
}

// Event listeners for navigation items
navItems.forEach((nav) => {
  nav.addEventListener("click", (event) => {
    event.preventDefault();
    const index = parseInt(nav.getAttribute("data-index"), 10);
    activateSlide(index);
    if (!isPaused) {
      startAutoRotate(); // restart timer
    }
  });
});

pauseBtns.forEach((pauseBtn) =>
  pauseBtn.addEventListener("click", pause_play_Slide)
);

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
    pause_play_Slide();
  }
});

// arrow buttons on medium and small screens
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

const prefersReducedMotion = window.matchMedia(
  "(prefers-reduced-motion: reduce)"
).matches;
if (prefersReducedMotion) {
  pause_play_Slide(); // Pause the carousel if user prefers reduced motion
} else {
  activateSlide(currentIndex); // Ensure the first slide is active
  startAutoRotate(); // Start the auto-rotation
}
