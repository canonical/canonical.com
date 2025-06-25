import { DotLottie } from "@lottiefiles/dotlottie-web";
import lottie from "lottie-web";

// Initialize light animation
const homepageSuru_light = new DotLottie({
  autoplay: true,
  loop: false,
  canvas: document.querySelector("#hero-section-suru-light"),
  src: "/static/json/suru_light.json",
});

// Initialize dark animation
const homepageSuru_dark = new DotLottie({
  autoplay: true,
  loop: false,
  canvas: document.querySelector("#hero-section-suru-shadow"),
  src: "/static/json/suru_shadow.json",
});

// Helper function to set direction + play
function playAnimation(anim, forward = true) {
  anim.setMode(forward ? "forward" : "reverse");
  // Animation is always playing until you stop it or it reverses and reaches the end
  // If the animation is already playing, we don't need to call play again
  // Also everytime we set the mode, it will reset the current frame to 0
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
          playAnimation(homepageSuru_light, true);
          playAnimation(homepageSuru_dark, true);
        } else {
          // Element exits viewport → play reverse
          playAnimation(homepageSuru_light, false);
          playAnimation(homepageSuru_dark, false);
        }
      });
    },
    {
      threshold: 0.5, // 50% visibility triggers
      rootMargin: "-5% 0px 0px 0px", // Adjust the root margin to trigger earlier
    }
  );

  const suruContainer = document.getElementById("suru-motion-anchor");
  observer.observe(suruContainer);
}

// we need to wait for the animations to load before we can use them
homepageSuru_dark.addEventListener("load", suruScrollHandler);

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
        centrepage.setSpeed(1); // normal speed
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

Object.entries(zoneConfigs).forEach(([zoneId, [start, end]]) => {
  const zone = document.querySelector(`.centre-animation__zone--${zoneId}`);
  if (!zone) return;

  zone.addEventListener("mouseenter", () => {
    centrepage.setSpeed(1); // normal speed
    centrepage.setDirection(1); // forward
    centrepage.playSegments([start, end], true);
  });

  zone.addEventListener("mouseleave", () => {
    const currentFrame = centrepage.currentFrame;
    const safeFrame = Math.max(start, Math.min(currentFrame, end));

    centrepage.setSpeed(4); // double speed
    centrepage.setDirection(-1); // reverse
    centrepage.playSegments([safeFrame, start], true);
  });
});
