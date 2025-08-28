import { DotLottie } from "@lottiefiles/dotlottie-web";
import lottie from "lottie-web";

// Suru animations
// Initialize light animation
const homepageSuru_light = new DotLottie({
  autoplay: true,
  loop: false,
  canvas: document.querySelector(".hero-section-suru-light"),
  src: "/static/json/suru_light.json",
});

// Initialize dark animation
const homepageSuru_dark = new DotLottie({
  autoplay: true,
  loop: false,
  canvas: document.querySelector(".hero-section-suru-shadow"),
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
      rootMargin: "-5% 0px 0px 0px",
    }
  );

  const suruContainer = document.getElementById("suru-motion-anchor");
  observer.observe(suruContainer);
}

// We need to wait for the animations to load before we can use them
homepageSuru_dark.addEventListener("load", suruScrollHandler);
