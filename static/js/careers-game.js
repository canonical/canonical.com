function initCareersGame() {
  var selectedSkillsContainer = document.querySelector(".js-selected-skills");
  var skillsContainer = document.querySelector(".js-skills");
  var submitButton = document.querySelector(".js-submit-button");
  var selectedSkills = [];
  selectedSkillsContainer.classList.remove("u-hide");

  handleSkillData();
  handleSubmit(); 
   
  function handleSkillData() {
    fetch("/static/data/skill-data.json")
    .then((response) => response.json())
    .then((data) => {
      data.forEach(skill => {
        buildModal(skill);
        buildCard(skill);
      })
    })
  }

  function buildCard(skill) {
    let colDiv = document.createElement('div');
    colDiv.setAttribute("class", "col-3");
   
    let card = document.createElement('div');
    card.setAttribute("class", "p-card--skill col-3");
    
    let form = document.createElement('form');
    
    let label = document.createElement('label');
    label.setAttribute("class", "p-checkbox");
    
    let input = document.createElement('input');
    input.setAttribute("type", "checkbox");
    input.setAttribute("id", `skill-${skill.id}`);
    input.setAttribute("name", "skill-card");
    input.setAttribute("aria-labelledby", "skill-card");
    input.setAttribute("class", "p-checkbox__input");
    input.setAttribute("data-skill", skill.id);
    
    let span = document.createElement('span');
    span.setAttribute("class", "p-checkbox__label p-card--skill__title");
    span.setAttribute("id", "skill-card");
    span.textContent = skill.title;
    
    let p = document.createElement('p');
    p.setAttribute("class", "p-card--skill__tagline p-heading--6");
    p.innerText = skill.tagline;
    
    label.append(input);
    label.append(span);
    form.append(label);
    form.append(p);
    card.append(form);
    skillsContainer.append(card);
    
    p.addEventListener("click", function(e){
      let modal = document.getElementById(`modal-${skill.id}`)
      modal.classList.remove("u-hide")
    })

    input.addEventListener("click", function (e){
      if (input.checked) {
        handleSkillAdd(skill)
      } else {
        handleSkillRemove(skill)
      }
    })
  }

  function buildModal(skill) {
    const cardParent = document.querySelector(".js-skills");

    let modal = document.createElement("div")
    modal.setAttribute("class", "p-card--modal u-hide")
    modal.setAttribute("id", `modal-${skill.id}`)

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
    formDiv.setAttribute("class", "p-card--skill")
    
    let form = document.createElement("form")

    let label = document.createElement("label")
    label.setAttribute("class", "p-checkbox")
  
    let input = document.createElement('input')
    input.setAttribute("type", "checkbox")
    input.setAttribute("aria-labelledby", "skill-modal")
    input.setAttribute("class", "p-checkbox__input")
    input.setAttribute("data-skill", skill.id)
    
    let span = document.createElement('span')
    span.setAttribute("class", "p-checkbox__label")
    span.setAttribute("id", "skill-modal")
    span.textContent = skill.title

    let pTitle = document.createElement("p")
    pTitle.setAttribute("class", "u-text--muted p-card--skill__tagline p-heading--6")
    pTitle.innerText = skill.title

    let pDescription = document.createElement("p")
    pDescription.setAttribute("class", "u-text--muted p-card--skill__tagline")
    pDescription.innerText = skill.description

    let addButton = document.createElement("button");
    addButton.setAttribute("class", "p-button add-skill-button");
    addButton.innerText = "That's me";
  
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
      handleSkillAdd(skill)
    })

    input.addEventListener("click", function(e) {
      if (input.checked) {
        handleSkillAdd(skill)
      } else {
        handleSkillRemove(skill)
      }
    })
  }

  function handleSkillAdd(skill) {
    let skillCheckboxes = document.querySelectorAll(`[data-skill="${skill.id}"]`)
    let skillDivs = document.querySelectorAll(".selected-skills")

    if (selectedSkills.length < 5) {
      selectedSkills.push(skill.title)
      for (let i = 0; i < skillDivs.length;i++) {
        if (!skillDivs[i].innerText) {
          skillDivs[i].innerText = skill.title
          break;
        }
      }
    }
    // Check all boxes for given skill (modal and card)
    skillCheckboxes.forEach(box => {
      if (selectedSkills.includes(skill.title) && box.checked == false) {
        box.checked = true;
      }
    })

    toggleCTAs(skill)
  }

  function handleSkillRemove(skill) {
    let index = selectedSkills.indexOf(skill.title)
    let skillDiv = document.querySelector(`.selected-skills[id=selected-${index + 1}]`)

    selectedSkills.splice(index, 1)
    skillDiv.innerHTML = "";
    
    toggleCTAs(skill)
  }
  
  function toggleCTAs(skill) {
    let skillCheckboxes = document.querySelectorAll(`[data-skill="${skill.id}"]`)
    let allCheckboxes = document.querySelectorAll(".p-checkbox__input")
    let allModalButtons = document.querySelectorAll(".add-skill-button")

    if (selectedSkills.length == 5) {
      // Disable checkboxes/modal button if skill cap reached
      allCheckboxes.forEach(check => {
        if (!check.checked){
          check.disabled = true;
        }
      })
      allModalButtons.forEach(button => {
        button.setAttribute("disabled", "")
      })
      // Enable submit button
      submitButton.removeAttribute("disabled")
    } 

    if (selectedSkills.length < 5) {
      // Re-enable checkboxes/modal button
      allCheckboxes.forEach(check => {
        if (check.disabled == true){
          check.disabled = false;
        }
      })
      allModalButtons.forEach(button => {
        button.removeAttribute("disabled")
      })
      // Disable submit button
      submitButton.setAttribute("disabled", "true")
    }
    // Make sure both checkboxes match
    if (skillCheckboxes[0].checked == false && skillCheckboxes[1].checked) {
      skillCheckboxes[1].checked = false
    }
  }

  function handleSubmit() {
    submitButton.addEventListener("click", function () {
      var skillsString = "";

      [].forEach.call(selectedSkills, function (skill) {
        skillsString += skill;

        if (skill !== selectedSkills[selectedSkills.length - 1]) {
          skillsString += ",";
        }
      });

      location.href = "results?core-skills=" + skillsString;
    });
  }
}

window.addEventListener("DOMContentLoaded", function () {
  initCareersGame();
});
