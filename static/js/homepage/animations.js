import { DotLottie } from "@lottiefiles/dotlottie-web";
import lottie from "lottie-web";

// Initialize light animation
window.homepageSuru_light = new DotLottie({
  autoplay: true,
  loop: false,
  canvas: document.querySelector("#hero-section-suru-light"),
  src: "/static/json/suru_light.lottie",
});

// Initialize dark animation
window.homepageSuru_dark = new DotLottie({
  autoplay: true,
  loop: false,
  canvas: document.querySelector("#hero-section-suru-shadow"),
  src: "/static/json/suru_shadow.lottie",
});

// Helper function to set direction + play
function playAnimation(anim, forward = true) {
  anim.setMode(forward ? "forward" : "reverse");
  // Animation is always playing until you stop it or it reverses and reaches the end
  // If the animation is already playing, we don't need to call play again
  // Also everytime we set the mode, it will reset the current frame to 0
  console.log(`Playing animation in ${forward ? "forward" : "reverse"} mode`);
  if (!anim.isPlaying) {
    anim.play();
  }
  anim.unfreeze();
}

function suruScrollHandler() {
  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        const isVisible =
          entry.isIntersecting && entry.intersectionRatio >= 0.25;

        if (isVisible) {
          // Element enters viewport → play forward
          playAnimation(window.homepageSuru_light, true);
          playAnimation(window.homepageSuru_dark, true);
        } else {
          // Element exits viewport → play reverse
          playAnimation(window.homepageSuru_light, false);
          playAnimation(window.homepageSuru_dark, false);
        }
      });
    },
    {
      threshold: 0.5, // 50% visibility triggers
      rootMargin: "-5% 0px 0px 0px", // Adjust the root margin to trigger earlier
    }
  );

  // FIX: remove "#" when using getElementById
  const suruContainer = document.getElementById("suru-motion-anchor");
  observer.observe(suruContainer);
}

// we need to wait for the animations to load before we can use them
window.homepageSuru_dark.addEventListener("load", suruScrollHandler);

window.centrepage = lottie.loadAnimation({
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
        window.centrepage.setSpeed(1); // normal speed
        window.centrepage.playSegments([1, 26], true);
      } else {
        window.centrepage.pause();
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

Object.entries(zoneConfigs).forEach(([zoneId, [start, end]]) => {
  const zone = document.querySelector(`.centre-animation__zone--${zoneId}`);
  if (!zone) return;

  zone.addEventListener("mouseenter", () => {
    window.centrepage.setSpeed(1); // normal speed
    window.centrepage.setDirection(1); // forward
    window.centrepage.playSegments([start, end], true);
  });

  zone.addEventListener("mouseleave", () => {
    const currentFrame = window.centrepage.currentFrame;
    const safeFrame = Math.max(start, Math.min(currentFrame, end)); // clamp to zone bounds

    window.centrepage.setSpeed(4); // double speed
    window.centrepage.setDirection(-1); // reverse
    window.centrepage.playSegments([safeFrame, start], true);
  });
});
