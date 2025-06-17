import { DotLottie } from "@lottiefiles/dotlottie-web";

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
      threshold: 0.25, // 50% visibility triggers
      rootMargin: "-30% 0px 0px 0px", // Adjust the root margin to trigger earlier
    }
  );

  // FIX: remove "#" when using getElementById
  const suruContainer = document.getElementById("hero-section-suru-wrapper");
  observer.observe(suruContainer);
}

// we need to wait for the animations to load before we can use them
window.homepageSuru_dark.addEventListener("load", suruScrollHandler);

window.centrepage = new DotLottie({
  autoplay: true,
  loop: false,
  canvas: document.querySelector("#centre-animation"),
  src: "/static/json/centre.lottie",
});

window.centrepage.addEventListener("load", () => {
  // Play the animation when it is loaded
  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          playAnimation(window.centrepage, true);
        } else {
          window.centrepage.pause();
        }
      });
    },
    {
      threshold: 0.1, // Trigger when at least 50% visible
    }
  );
  const centreContainer = document.querySelector("#centre-animation");
  observer.observe(centreContainer);
});
