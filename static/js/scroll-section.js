import lottie from "lottie-web";

const wrappers = document.querySelectorAll(".scroll-section");

let activeWrapper = null;

function lockScroll() {
  const scrollbarWidth =
    window.innerWidth - document.documentElement.clientWidth;
  document.body.style.overflow = "hidden";
  document.body.style.paddingRight = `${scrollbarWidth}px`;
}

function unlockScroll() {
  document.body.style.overflow = "";
  document.body.style.paddingRight = "";
}

function showSection(
  index,
  currentIndex,
  setCurrentIndex,
  tabs,
  indicator,
  sections
) {
  if (index === currentIndex) {
    const initialTab = tabs[index];
    const iconContainer = initialTab.querySelector(".scroll-section__tab-icon");
    const lottiePath = initialTab.dataset.lottie;

    if (lottiePath && iconContainer) {
      iconContainer.querySelector("img")?.classList.add("u-hide");

      lottie.loadAnimation({
        container: iconContainer,
        renderer: "svg",
        loop: true,
        autoplay: true,
        path: lottiePath,
      });
    }
    return;
  }

  const currentSection = sections[currentIndex];
  const nextSection = sections[index];

  // Animate sections
  currentSection.classList.remove("active");
  currentSection.classList.add("slide-out-up");
  currentSection.setAttribute("aria-hidden", "true");

  nextSection.classList.add("active");
  nextSection.classList.remove("slide-out-up");
  nextSection.setAttribute("aria-hidden", "false");

  setTimeout(() => {
    currentSection.classList.remove("slide-out-up");
  }, 400); // match CSS transition time

  // Animate tabs
  tabs.forEach((tab) => {
    tab.classList.remove("active");

    const icon = tab.querySelector(".scroll-section__tab-icon");
    if (icon) {
      icon.querySelector("img")?.classList.remove("u-hide");
      icon.querySelector("svg")?.remove(); // Remove Lottie
    }
  });

  const activeTab = tabs[index];
  activeTab.classList.add("active");

  const iconContainer = activeTab.querySelector(".scroll-section__tab-icon");
  const lottiePath = activeTab.dataset.lottie;

  if (lottiePath && iconContainer) {
    iconContainer.querySelector("img")?.classList.add("u-hide");

    lottie.loadAnimation({
      container: iconContainer,
      renderer: "svg",
      loop: true,
      autoplay: true,
      path: lottiePath,
    });
  }

  indicator.style.top = `${activeTab.offsetTop}px`;
  setCurrentIndex(index);
}

function setScrollSection(wrapper) {
  const tabs = wrapper.querySelectorAll(".scroll-section__tab");
  const indicator = wrapper.querySelector(".scroll-section__indicator");
  const sections = wrapper.querySelectorAll(".scroll-section__content");

  let currentIndex = 0;
  const setCurrentIndex = (val) => {
    currentIndex = val;
  };

  let scrollEnabled = false;

  // Tab click navigation
  tabs.forEach((tab, index) => {
    tab.addEventListener("click", () => {
      showSection(
        index,
        currentIndex,
        setCurrentIndex,
        tabs,
        indicator,
        sections
      );
    });
  });

  // Track which scroll section is active
  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          activeWrapper = wrapper;
          scrollEnabled = true;
        } else if (activeWrapper === wrapper) {
          scrollEnabled = false;
        }
      });
    },
    {
      threshold: 1,
      rootMargin: "-12% 0px 0px 0px",
    }
  );

  observer.observe(wrapper);

  // Scroll navigation
  window.addEventListener(
    "wheel",
    (e) => {
      if (
        activeWrapper !== wrapper ||
        !scrollEnabled ||
        window.innerWidth <= 1036
      ) {
        return;
      }

      const atLast = currentIndex < sections.length - 1 && e.deltaY > 0;
      const atFirst = currentIndex > 0 && e.deltaY < 0;

      if (atLast || atFirst) {
        e.preventDefault();

        lockScroll();

        const newIndex = currentIndex + (e.deltaY > 0 ? 1 : -1);
        showSection(
          newIndex,
          currentIndex,
          setCurrentIndex,
          tabs,
          indicator,
          sections
        );

        scrollEnabled = false;
        setTimeout(() => {
          scrollEnabled = true;
          unlockScroll();
        }, 600); // allow transition to finish
      }
    },
    { passive: false }
  );

  // Initialize first section
  window.addEventListener("load", () => {
    showSection(0, 0, setCurrentIndex, tabs, indicator, sections);
  });
}

// Init all wrappers
wrappers.forEach(setScrollSection);
