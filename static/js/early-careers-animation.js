import { Rive, Fit, Alignment, Layout, RuntimeLoader } from "@rive-app/canvas";

// Self-host the WASM backing dependency so we don't rely on a third-party CDN
// at runtime and stay within the site's CSP (connect-src 'self')
RuntimeLoader.setWasmUrl("/static/js/modules/rive/rive.wasm");

function initCareerProgressionAnimation() {
  const canvas = document.getElementById("rive-career-progression");

  if (!canvas) {
    return;
  }

  const rivSrc = canvas.dataset.rivSrc;

  if (!rivSrc) {
    return;
  }

  const prefersReducedMotion = window.matchMedia(
    "(prefers-reduced-motion: reduce)"
  ).matches;

  // Track async state: the Rive WASM load and the scroll intersection can
  // complete in either order, so we reconcile them with flags.
  let hasLoaded = false;
  let isInView = false;

  const riveInstance = new Rive({
    src: rivSrc,
    canvas: canvas,

    autoplay: !prefersReducedMotion,
    stateMachines: "State Machine 1",
    layout: new Layout({ fit: Fit.Cover, alignment: Alignment.Center }),
    onLoad: () => {
      riveInstance.resizeDrawingSurfaceToCanvas();
      hasLoaded = true;
      // If the canvas is already off-screen when onLoad fires, pause now.
      if (!isInView && !prefersReducedMotion) {
        riveInstance.pause();
      }
    },
  });

  // Only play the animation when the canva is in view
  if (!prefersReducedMotion) {
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          isInView = entry.isIntersecting;
          if (!hasLoaded) {
            return;
          }
          if (isInView) {
            riveInstance.play("State Machine 1");
          } else {
            riveInstance.pause();
          }
        });
      },
      { threshold: 0.1 }
    );

    observer.observe(canvas);
  }

  window.addEventListener("resize", () => {
    riveInstance.resizeDrawingSurfaceToCanvas();
  });
}

if (document.readyState !== "loading") {
  initCareerProgressionAnimation();
} else {
  document.addEventListener("DOMContentLoaded", initCareerProgressionAnimation);
}
