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

function updateWrapperMinHeight(wrapper) {
  const activeContent = wrapper.querySelector(".scroll-section__content");
  if (activeContent) {
    // this works because the content section is set to have height equal to maxcontent height
    wrapper.style.minHeight = `${activeContent.scrollHeight}px`;
  }
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
    return;
  }

  const currentSection = sections[currentIndex];
  const nextSection = sections[index];

  // Animate sections
  currentSection.classList.remove("active");
  currentSection.classList.add("slide-out-up");
  currentSection.setAttribute("aria-hidden", "true");
  currentSection.inert = true;

  nextSection.classList.add("active");
  nextSection.classList.remove("slide-out-up");
  nextSection.setAttribute("aria-hidden", "false");
  nextSection.inert = false;

  setTimeout(() => {
    currentSection.classList.remove("slide-out-up");
  }, 400); // match CSS transition time

  // Animate tabs
  tabs.forEach((tab) => {
    tab.classList.remove("active");

    const icon = tab.querySelector(".scroll-section__tab-icon");
    if (icon) {
      icon.querySelector("img").style.opacity = 1; // show image
      icon.querySelector(".p-lottie--container").style.opacity = 0; // hide Lottie
    }
  });

  const activeTab = tabs[index];
  activeTab.classList.add("active");

  const iconContainer = activeTab.querySelector(".scroll-section__tab-icon");
  const lottiePath = activeTab.dataset.lottie;

  if (lottiePath && iconContainer) {
    iconContainer.querySelector("img").style.opacity = 0; // hide image
    iconContainer.querySelector(".p-lottie--container").style.opacity = 1; // show Lottie
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
    // Initialize Lottie animations
    const iconContainer = tab.querySelector(".scroll-section__tab-icon");
    const lottiePath = tab.dataset.lottie;
    if (lottiePath && iconContainer) {
      const lottieContainer = iconContainer.querySelector(
        ".p-lottie--container"
      );
      lottie.loadAnimation({
        container: lottieContainer,
        renderer: "svg",
        loop: true,
        autoplay: true,
        path: lottiePath,
      });
    }

    // Add click event listener to each tab
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

  const activeContent_wrapper = wrapper.querySelector(
    ".scroll-section__contentArea"
  );
  // Update wrapper min-height based on active content
  let loadtimer;

  window.addEventListener("load", () => {
    clearTimeout(loadtimer);
    loadtimer = setTimeout(() => {
      updateWrapperMinHeight(activeContent_wrapper);
    }, 1500);
  });

  // Debounce resize event to update wrapper min-height
  let resizeTimeout;
  window.addEventListener("resize", () => {
    clearTimeout(resizeTimeout);
    resizeTimeout = setTimeout(() => {
      updateWrapperMinHeight(activeContent_wrapper);
    }, 100);
  });

  // Track which scroll section is active
  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          activeWrapper = wrapper;
          scrollEnabled = true;
        } else {
          scrollEnabled = false;
        }
      });
    },
    {
      threshold: 0.9,
      rootMargin: "0px 0px 0px 0px",
    }
  );
  const observe_element = wrapper.closest(".scroll-section-observe-anchor");
  observer.observe(observe_element);

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

        // Debouncing scroll so that it doesn't trigger too fast and go across all sections in one go
        scrollEnabled = false;
        setTimeout(() => {
          scrollEnabled = true;
          unlockScroll();
        }, 300);
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
