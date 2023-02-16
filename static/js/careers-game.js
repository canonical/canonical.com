function initCareersGame() {
  var selectedSkillsContainer = document.querySelector(".js-selected-skills");
  var skillsContainer = document.querySelector(".js-skills");
  var submitButton = document.querySelector(".js-submit-button");
  var selectedSkills = [];
  selectedSkillsContainer.classList.remove("u-hide");
  skillsContainer.classList.remove("u-hide");

  handleData();
  handleCheckbox();
  handleCardClick();
  handleModalButton();
  handleSkillRemove();
  handleSubmit(); 
   
  function handleData(){
    fetch("/static/data/skill-data.json")
    .then((response) => response.json())
    .then((data) => {
      data.forEach(skill => {
        buildCard(skill)
        buildModal(skill)
      })
    })
  }

  function buildCard(skill) {
    const cardParent = document.querySelector(".js-skills");
    let colDiv = document.createElement('div')
    colDiv.setAttribute("class", "col-3")
   
    let card = document.createElement('div')
    card.setAttribute("class", "p-card--test col-3")
    card.setAttribute("data-skill", skill.id)
    
    let form = document.createElement('form')
    
    let label = document.createElement('label')
    label.setAttribute("class", "p-checkbox")
    
    let input = document.createElement('input')
    input.setAttribute("type", "checkbox")
    input.setAttribute("id", `skill-${skill.id}`)
    input.setAttribute("name", "skill-card")
    input.setAttribute("aria-labelledby", "skill")
    input.setAttribute("class", "p-checkbox__input")
    
    let span = document.createElement('span')
    span.setAttribute("class", "p-checkbox__label p-card--test__title")
    span.setAttribute("id", "skill")
    span.textContent = skill.title
    
    let p = document.createElement('p')
    p.setAttribute("class", "u-text--muted p-card--test__tagline p-heading--6")
    p.innerText = skill.tagline
    
    label.append(input)
    label.append(span)
    form.append(label)
    form.append(p)
    card.append(form)
    cardParent.append(card)
  }

  function buildModal(skill) {
    const cardParent = document.querySelector(".js-skills");

    let modal = document.createElement("div")
    modal.setAttribute("class", "p-card--modal u-hide")
    modal.setAttribute("id", "modal")
    modal.setAttribute("data-skill", skill.id)

    let section = document.createElement("section")
    section.setAttribute("class", "p-modal__dialog")
    section.setAttribute("role", "dialog")
    section.setAttribute("aria-modal", "true")
    section.setAttribute("aria-labelledby", "modal-title")
    section.setAttribute("aria-describedby", "modal-description")
  
    let closeButton = document.createElement("button")
    closeButton.setAttribute("class", "p-modal__close")
    closeButton.setAttribute("aria-label", "Close active modal")
    closeButton.setAttribute("aria-controls", "modal")
    closeButton.innerText = "Close"

    let formDiv = document.createElement('div')
    formDiv.setAttribute("class", "p-card--test")
    
    let form = document.createElement('form')

    let label = document.createElement('label')
    label.setAttribute("class", "p-checkbox")
  
    let input = document.createElement('input')
    input.setAttribute("type", "checkbox")
    input.setAttribute("aria-labelledby", "skill-modal")
    input.setAttribute("class", "p-checkbox__input")
    
    let span = document.createElement('span')
    span.setAttribute("class", "p-checkbox__label")
    span.setAttribute("id", "skill-modal")
    span.textContent = skill.title

    let pTitle = document.createElement("p")
    pTitle.setAttribute("class", "u-text--muted p-card--test__tagline p-heading--6")
    pTitle.innerText = skill.title

    let pDescription = document.createElement("p")
    pDescription.setAttribute("class", "u-text--muted p-card--test__tagline")
    pDescription.innerText = skill.description

    let addButton = document.createElement("button")
    addButton.setAttribute("class", "p-button add-skill-button")
    addButton.innerText = "That's me"
  
    label.append(input)
    label.append(span)
    form.append(label)
    form.append(pTitle)
    form.append(pDescription)
    form.append(addButton)
    formDiv.append(form)
    section.append(closeButton)
    section.append(formDiv)
    modal.append(section)
    cardParent.append(modal)
  }

  function handleCardClick() {
    let selectableCards = document.querySelectorAll(".p-card--test");

    let cardModal = document.querySelectorAll(".p-card--modal")
    console.log("from code", cardModal, typeof(cardmodal));
    
    
    const closeModalButton = document.querySelectorAll(".p-modal__close");

    // Show modal 
    [].forEach.call(selectableCards, function (selectedCard) {
      selectedCard.addEventListener("click", function (e){
        cardModal.classList.remove("u-hide")
      });
    });

    // Close modal
    closeModalButton.addEventListener('click', function(e){   
      cardModal.classList.add("u-hide")
    });
  }

  function handleCheckbox() {
    var checkboxes = document.querySelectorAll("input[type=checkbox][name=skill-card]");
    
    [].forEach.call(checkboxes, function (checkbox) {
      checkbox.addEventListener("click", function(e) {
        let parentDiv = e.target.parentNode.parentNode;
        let title = parentDiv.querySelector(".p-card--test__title").innerText
        handleSkillAdd(title)
      })
    })
  }

  function handleModalButton() {
    let skillButtons = document.querySelectorAll(".add-skill-button");

    [].forEach.call(skillButtons, function (skillButton) {
      // let parentDiv = skillButton.parentNode.parentNode;
      // let title = parentDiv.querySelector("span").innerText;
      //   console.log(parentDiv, title)
      skillButton.addEventListener("click", function(e) {
        let parentDiv = skillButton.parentNode.parentNode;
        let title = parentDiv.querySelector("span").innerText;
        e.preventDefault()
        handleSkillAdd(title)
      })
    })
    
  }

  function handleSkillAdd(title) {
 
    if (selectedSkills.length < 5) {
      selectedSkills.push(title)
      console.log(selectedSkills)
    }

    // [].forEach.call(skillAddButtons, function (button) {
    //   button.addEventListener("click", function (event) {

        // var skillCardID = event.currentTarget.getAttribute("data-parent");
        // var skillCard = document.getElementById(skillCardID);
        // var title = skillCard.querySelector(".p-card--test__title");
        // var tagline = skillCard.querySelector(".p-card--test__tagline")
        //   .innerText;

        // event.stopPropagation();

        // if (skillCard) {
        //   if (selectedSkills.length < 5) {
        //     var skillObject = {
        //       id: skillCard.getAttribute("data-skill"),
        //       title: title,
        //       tagline: tagline,
        //     };

        //     selectedSkills.push(skillObject);
        //     toggleCardVisibility(skillCard);
        //     renderSelectedSkills();
        //   } else {
        //     alert(
        //       "You have already selected 5 skills! Please click the 'Submit choices' button to see the list of roles suitable for you."
        //     );
        //   }
        // }
    //   });
    // });
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

      location.href = "results?core-skills=" + skillsString;
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
