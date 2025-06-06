const tabs = document.querySelectorAll(".scroll-section__tab");
const indicator = document.querySelector(".scroll-section__indicator");
const sections = document.querySelectorAll(".scroll-section__content");
let currentIndex = 0;

const sectionIds = ["cloud", "silicon", "hardware"];

function showSection(index) {
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

  currentIndex = index;
}

// Click navigation
tabs.forEach((tab, index) => {
  tab.addEventListener("click", () => showSection(index));
});

// Scroll navigation
const wrapper = document.querySelector(".scroll-section");
let scrollEnabled = false;

const observer = new IntersectionObserver(
  (entries) => {
    entries.forEach((entry) => {
      scrollEnabled = entry.isIntersecting;
    });
  },
  {
    threshold: 0.2, // Trigger when at least 50% visible
  }
);

observer.observe(wrapper);

// Scroll listener
window.addEventListener(
  "wheel",
  (e) => {
    if (!scrollEnabled) return;

    if (e.deltaY > 0 && currentIndex < sections.length - 1) {
      showSection(currentIndex + 1);
    } else if (e.deltaY < 0 && currentIndex > 0) {
      showSection(currentIndex - 1);
    }
  },
  { passive: true }
);

// Initial state
window.addEventListener("load", () => {
  showSection(0);
});
