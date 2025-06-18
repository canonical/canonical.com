const wrappers = document.querySelectorAll(".scroll-section");

function showSection(
  index,
  currentIndex,
  setCurrentIndex,
  tabs,
  indicator,
  sections
) {
  console.log(`Switching from section ${currentIndex} to ${index}`);
  if (index === currentIndex) return;

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
  tabs.forEach((tab) => tab.classList.remove("active"));
  const activeTab = tabs[index];
  activeTab.classList.add("active");
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
      threshold: 0.95, // Trigger when at least 50% visible
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
      if (currentIndex != 0 && currentIndex != sections.length - 1) {
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
