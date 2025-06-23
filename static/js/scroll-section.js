import lottie from "lottie-web";

const wrappers = document.querySelectorAll(".scroll-section");

function showSection(
  index,
  currentIndex,
  setCurrentIndex,
  tabs,
  indicator,
  sections
) {
  if (index === currentIndex) {
    const initalTab = tabs[index];

    const initalTab_lottiePath = initalTab.dataset.lottie;
    const initalTab_iconContainer = initalTab.querySelector(
      ".scroll-section__tab-icon"
    );

    if (initalTab_lottiePath && initalTab_iconContainer) {
      initalTab_iconContainer.querySelector("img")?.classList.add("u-hide");

      // Inject Lottie
      lottie.loadAnimation({
        container: initalTab_iconContainer,
        renderer: "svg",
        loop: true,
        autoplay: true,
        path: initalTab_lottiePath,
      });
    }
    return;
  }

  const currentSection = sections[currentIndex];
  const nextSection = sections[index];

  // Slide out current
  currentSection.classList.remove("active");
  currentSection.classList.add("slide-out-up");
  currentSection.setAttribute("aria-hidden", "true");

  // Slide in next after short delay to allow z-index layering
  nextSection.classList.add("active");
  nextSection.classList.remove("slide-out-up");
  nextSection.setAttribute("aria-hidden", "false");

  // Remove slide-out-up class after transition ends
  setTimeout(() => {
    currentSection.classList.remove("slide-out-up");
  }, 400); // Match CSS transition duration

  // Tab indicator
  tabs.forEach((tab) => {
    tab.classList.remove("active");
    tab;
    tab
      .querySelector(".scroll-section__tab-icon img")
      ?.classList.remove("u-hide");
    tab.querySelector("svg")?.remove();
  });

  const activeTab = tabs[index];
  activeTab.classList.add("active");

  const lottiePath = activeTab.dataset.lottie;
  const iconContainer = activeTab.querySelector(".scroll-section__tab-icon");


  console.log(`Lottie path: ${lottiePath}`);
  console.log(`Icon container: ${iconContainer}`);
  
  if (lottiePath && iconContainer) {
    iconContainer.querySelector("img")?.classList.add("u-hide");

    // Inject Lottie
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

  // Click navigation
  tabs.forEach((tab, index) => {
    tab.addEventListener("click", () =>
      showSection(
        index,
        currentIndex,
        setCurrentIndex,
        tabs,
        indicator,
        sections
      )
    );
  });

  // Scroll navigation

  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        scrollEnabled = entry.isIntersecting;
      });
    },
    {
      threshold: 1, // Trigger when at least 50% visible
      // rootMargin: "0% 0px 0px -30%", // Adjust the root margin to trigger earlier
    }
  );

  observer.observe(wrapper);

  // Scroll listener
  window.addEventListener(
    "wheel",
    (e) => {
      if (!scrollEnabled || window.innerWidth <= 1036) {
        return;
      }
      if (currentIndex != sections.length - 1 && e.deltaY > 0) {
        e.preventDefault(); // Prevent default scrolling behavior
      }
      if (currentIndex != 0 && e.deltaY < 0) {
        e.preventDefault(); // Prevent default scrolling behavior
      }
      if (e.deltaY > 0 && currentIndex < sections.length - 1) {
        showSection(
          currentIndex + 1,
          currentIndex,
          setCurrentIndex,
          tabs,
          indicator,
          sections
        );
        scrollEnabled = false;
        setTimeout(() => (scrollEnabled = true), 600);
      } else if (e.deltaY < -0 && currentIndex > 0) {
        showSection(
          currentIndex - 1,
          currentIndex,
          setCurrentIndex,
          tabs,
          indicator,
          sections
        );
        scrollEnabled = false;
        setTimeout(() => (scrollEnabled = true), 600);
      }
    },
    { passive: false }
  );

  // Initial state
  window.addEventListener("load", () => {
    showSection(0, 0, setCurrentIndex, tabs, indicator, sections);
  });
}

wrappers.forEach(setScrollSection);
