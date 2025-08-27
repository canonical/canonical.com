import lottie from "lottie-web";

// Initialize the centrepage animation
const centrepage = lottie.loadAnimation({
  container: document.querySelector("#centre-animation"),
  renderer: "svg",
  loop: false,
  autoplay: false,
  path: "/static/json/centre_hover.json",
});

// Intersection observer to control playback on viewport entry
const observer = new IntersectionObserver(
  (entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        centrepage.setSpeed(1);
        centrepage.playSegments([1, 26], true);
      } else {
        centrepage.pause();
      }
    });
  },
  {
    threshold: 0.1,
  }
);

observer.observe(document.querySelector("#centre-animation"));

const zoneConfigs = {
  1: [28, 47],
  2: [52, 71],
  3: [76, 95],
  4: [100, 119],
  5: [124, 143],
  6: [148, 167],
  7: [172, 191],
};

const prefersReducedMotion = window.matchMedia(
  "(prefers-reduced-motion: reduce)"
).matches;
if (!prefersReducedMotion) {
  Object.entries(zoneConfigs).forEach(([zoneId, [start, end]]) => {
    const zone = document.querySelector(`.centre-animation__zone--${zoneId}`);
    if (!zone) return;

    zone.addEventListener("mouseenter", () => {
      centrepage.setSpeed(1);
      centrepage.setDirection(1); // forward
      centrepage.playSegments([start, end], true);
    });

    zone.addEventListener("mouseleave", () => {
      const currentFrame = centrepage.currentFrame;
      const safeFrame = Math.max(start, Math.min(currentFrame, end));

      centrepage.setSpeed(4);
      centrepage.setDirection(-1); // reverse
      centrepage.playSegments([safeFrame, start], true);
    });
  });
} else {
  observer.unobserve(document.querySelector("#centre-animation"));
  centrepage.goToAndStop(26, true);
}
