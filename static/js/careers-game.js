function initCareersGame() {
  var selectedSkillsContainer = document.querySelector(".js-selected-skills");
  var skillsContainer = document.querySelector(".js-skills");
  var submitButton = document.querySelector(".js-submit-button");
  var selectedSkills = [];
  selectedSkillsContainer.classList.remove("u-hide");
  skillsContainer.classList.remove("u-hide");

  handleData();
  handleSkillRemove();
  handleSubmit(); 
   
  function handleData(){
    fetch("/static/data/skill-data.json")
    .then((response) => response.json())
    .then((data) => {
      data.forEach(skill => {
        buildCard(skill)
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
   
    p.addEventListener("click", function(e){
      buildModal(skill)
    })

    input.addEventListener("click", function (e){
      handleCheckboxSkillAdd(skill.title)
    })
  }

  function buildModal(skill) {
    const cardParent = document.querySelector(".js-skills");

    let modal = document.createElement("div")
    modal.setAttribute("class", "p-card--modal")
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

    closeButton.addEventListener("click", function(e) {
      modal.classList.add("u-hide")
    })

    addButton.addEventListener("click", function(e) {
      e.preventDefault()
      handleCheckboxSkillAdd(skill.title)
    })
  }

  function handleCheckboxSkillAdd(title) {
    // add skill
    if (selectedSkills.length < 5) {
      selectedSkills.push(title)

      let skillDiv = document.querySelector(`.selected-skills[id=selected-${selectedSkills.length}]`)
      skillDiv.innerText = title + ",";
    } 

    // check checkbox if skill added from modal

    // disable checkboxes if skill cap reached
    if (selectedSkills.length == 5) {
      let checks = document.querySelectorAll(".p-checkbox__input")
      checks.forEach(check => {
        if (!check.checked){
          check.disabled = true;
        }
      })
    }

    // disable modal button if skill cap

    
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
