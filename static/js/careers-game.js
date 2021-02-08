function initCareersGame() {
  var selectedSkillsContainer = document.querySelector(".js-selected-skills");
  var skillsContainer = document.querySelector(".js-skills");
  var submitButton = document.querySelector(".js-submit-button");
  var selectedSkills = [];

  selectedSkillsContainer.classList.remove("u-hide");
  skillsContainer.classList.remove("u-hide");

  handleCardClick();
  handleSkillAdd();
  handleSkillRemove();
  handleSubmit();

  function handleCardClick() {
    selectableCards = document.querySelectorAll(".p-card--game");

    [].forEach.call(selectableCards, function (selectableCard) {
      selectableCard.addEventListener("click", function (e) {
        var expandedCard = document.querySelector(".p-card--game.is-grey");
        var targetCard = e.currentTarget;

        if (expandedCard) {
          expandedCard.classList.remove("is-grey");
        }

        targetCard.classList.add("is-grey");
      });
    });
  }

  function handleSkillAdd() {
    var skillAddButtons = document.querySelectorAll(".js-button--add");

    [].forEach.call(skillAddButtons, function (button) {
      button.addEventListener("click", function (event) {
        var skillCardID = event.currentTarget.getAttribute("data-parent");
        var skillCard = document.getElementById(skillCardID);
        var title = skillCard.querySelector(".p-card--game__title").innerText;
        var tagline = skillCard.querySelector(".p-card--game__tagline")
          .innerText;

        event.stopPropagation();

        if (skillCard) {
          if (selectedSkills.length < 5) {
            var skillObject = {
              id: skillCard.getAttribute("data-skill"),
              title: title,
              tagline: tagline,
            };

            selectedSkills.push(skillObject);
            toggleCardVisibility(skillCard);
            renderSelectedSkills();
          } else {
            alert(
              "You have already selected 5 skills! Please click the 'Submit choises' button to see the list of roles suitable for you."
            );
          }
        }
      });
    });
  }

  function handleSkillRemove() {
    var removeSkillCTAs = document.querySelectorAll(".js-button--remove");

    [].forEach.call(removeSkillCTAs, function (cta) {
      cta.addEventListener("click", function (event) {
        var selectedCardID = event.currentTarget.getAttribute("data-parent");
        var selectedCard = document.getElementById(selectedCardID);
        var skillID = selectedCard.getAttribute("data-skill");
        var skillCard = document.getElementById("skill-" + skillID);

        selectedSkills = selectedSkills.filter(function (el) {
          return !(el.id === skillID);
        });

        toggleCardVisibility(skillCard);
        renderSelectedSkills();
      });
    });
  }

  function handleSubmit() {
    submitButton.addEventListener("click", function () {
      var skillsString = "";

      [].forEach.call(selectedSkills, function (skill) {
        skillsString += skill.title;

        if (skill !== selectedSkills[selectedSkills.length - 1]) {
          skillsString += ",";
        }
      });

      location.href = "results?coreSkills=" + skillsString;
    });
  }

  function renderSelectedSkills() {
    var cards = selectedSkillsContainer.querySelectorAll(".p-card--game");

    for (i = 0; i < cards.length; i++) {
      var tagline = "";
      var title = "";
      var cardTitleEl = cards[i].querySelector(".p-card--game__title");
      var cardTaglineEl = cards[i].querySelector(".p-card--game__tagline");

      if (selectedSkills[i]) {
        title = selectedSkills[i].title;
        tagline = selectedSkills[i].tagline;
        cards[i].classList.remove("is-empty");
        cards[i].classList.add("is-selected");
        cards[i].setAttribute("data-skill", selectedSkills[i].id);
      } else {
        cards[i].classList.add("is-empty");
        cards[i].classList.remove("is-selected");
        cards[i].removeAttribute("data-skill");
      }

      cardTitleEl.innerText = title;
      cardTaglineEl.innerText = tagline;
    }

    if (selectedSkills.length === 5) {
      submitButton.disabled = false;
    } else {
      submitButton.disabled = true;
    }
  }

  function toggleCardVisibility(card) {
    card.classList.toggle("is-empty");
    card.classList.remove("is-grey");
  }
}

window.addEventListener("DOMContentLoaded", function () {
  initCareersGame();
});
