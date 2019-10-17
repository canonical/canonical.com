(function () {
  window.onload = loadGame;
  var selectableDomCards = null; 
  var selectedCard = null;
  var lastClickedCard = null;
  var selectedSkills = [];
  const submitButton = document.querySelector(".js-submit-button");
  const container = document.querySelector(".js-selected-skills");

  function loadGame() {
    // Add click event listener to the submit button
    submitButton.addEventListener("click", function () {
      var skillsString = "";
      selectedSkills.forEach((skill,i) => {
        if (i === selectedSkills.length - 1 ) {
          skillsString += skill.name;
        } else {
          skillsString += `${skill.name},`;
        }
      });
      location.href = `results?coreSkills=${skillsString}`;
    });

    // Render empty selected skills cards
    renderSelectedSkills(selectedSkills);
    const cardContainer = document.querySelector(".js-allCards");
    const cardTree = document.createDocumentFragment();
    // Create 6 empty columns to host the cards
    const columnDiv = [];
    for (i = 0; i < 6; i++) {
      columnDiv[i] = document.createElement("div");
      columnDiv[i].classList.add("col-2", "col-medium-3");
    }
    // Create a card for each skill and add it to a column
    var j = 0; // Counts columns
    skills.forEach((el, i) => {
      const cardDiv = document.createElement("div");
      cardDiv.classList.add("p-card--game");
      cardDiv.setAttribute("data-skill", i);
      cardDiv.innerHTML = `
        <button class="has-icon u-hide js-add-button"><span>That's me</span><i class="p-icon--plus"></i></button>
        <h4 class="p-card--game__title">${el.name}</h4>
        <div class="p-card--game__content">
          <p>${el.description}</p>
          <p class="u-hide">${el.details}</p>
        </div>`
      if (j < 6) {
        columnDiv[j].appendChild(cardDiv);
        j++;
      } else {
        j = 0;
      }
    });
    // Add the html for each column to the parent container
    columnDiv.forEach(el => {
      cardTree.appendChild(el);
    });
    cardContainer.appendChild(cardTree);

    selectableDomCards = document.querySelectorAll(".p-card--game"); 

    // Add card click event listeners 
    selectableDomCards.forEach((el, i) => {
      el.setAttribute("data-card", i);
      el.addEventListener("click", function cardClickHandler(event){
        // Get the number of the card clicked
        if (event.target.dataset.card) {
          lastClickedCard = event.target.dataset.card;
        } else if (event.target.classList.value === "p-card--game__title") {
          lastClickedCard = event.target.parentElement.dataset.card;
        } else {
          lastClickedCard = event.target.parentElement.parentElement.dataset.card;
        }
        // Show card details on click
        if (selectedCard === null) {
          el.removeEventListener("click", cardClickHandler);
          el.classList.add("is-grey");
          el.children[0].classList.remove("u-hide");
          el.children[2].children[1].classList.remove("u-hide");
          selectedCard = el.dataset.card;
        } else {
          // Handle data related to the previously selected card
          selectableDomCards[selectedCard].classList.remove("is-grey");
          selectableDomCards[selectedCard].children[0].classList.add("u-hide");
          selectableDomCards[selectedCard].children[2].children[1].classList.add("u-hide");
          selectableDomCards[selectedCard].addEventListener("click", cardClickHandler);
          // Handle data related to the currently clicked card
          selectableDomCards[lastClickedCard].classList.add("is-grey");
          selectableDomCards[lastClickedCard].children[0].classList.remove("u-hide");
          selectableDomCards[lastClickedCard].children[2].children[1].classList.remove("u-hide");
          selectableDomCards[lastClickedCard].removeEventListener("click", cardClickHandler);
          selectedCard = lastClickedCard;
        }
      });
    });

    document.querySelectorAll(".js-add-button").forEach(button => {
      button.addEventListener("click", function (event) {
        const skillData = event.target.closest(".p-card--game").dataset;
        if (skillData) {
          if (selectedSkills.length < 5) {
            const skillObject = {...skills[skillData.skill], skill: skillData.skill, card: skillData.card};
            selectedSkills.push(skillObject);
            toggleCardVisibility(skillData.card); 
            renderSelectedSkills(selectedSkills);
          } else {
            alert("You have already selected 5 skills! Please click the 'Submit choises' button to see the list of roles suitable for you.");
          }
        } else {
          console.log("Error! We cannot find any card element with the specified class.");
        }
      });
    });
  };

  // Remove skill and show card
  function removeSelectedSkill(event) {
    const skillData = event.target.closest(".p-card--game-selected").dataset;
    if (skillData) { 
      selectedSkills = selectedSkills.filter(el => {
        return !(el.card === skillData.card); 
      });
      toggleCardVisibility(skillData.card);
      renderSelectedSkills(selectedSkills);
    } else {
      console.log("Error! We cannot find any card element with the specified class.");
    };
  }

  // Toggle visible/empty card
  function toggleCardVisibility(card) {
    if (selectableDomCards[card].classList.contains("p-card--game")) {
      selectableDomCards[card].classList.remove("p-card--game", "is-grey");
      selectableDomCards[card].classList.add("p-card--game-empty");
    } else {
      if (selectableDomCards[card].children[2].children[1].classList.contains("u-hide")){
        selectableDomCards[card].classList.remove("p-card--game-empty");
        selectableDomCards[card].classList.add("p-card--game");
      } else{
        selectableDomCards[card].classList.remove("p-card--game-empty");
        selectableDomCards[card].classList.add("p-card--game", "is-grey");
      }
    }
  };

  // Render selected skills 
  async function renderSelectedSkills(selectedSkills) {
    const cardTree = document.createDocumentFragment();
    // Empty the DOM
    while (container.children.length > 1) {
      container.removeChild(container.firstChild);
    }
    var disabledButton = false;
    for (i=0; i<5; i++) {
      if (selectedSkills[i]) {
        const card = document.createElement("div");
        card.classList.add("col-2", "col-medium-3");
        card.innerHTML = `<div class="p-card--game-selected" data-skill=${selectedSkills[i].skill} data-card=${selectedSkills[i].card}><button class="js-remove-button"><i class="p-icon--close"></i></button><h4 class="p-card--game-selected__title">${selectedSkills[i].name}</h4><div class="p-card--game-selected__content"><p>${selectedSkills[i].description}</p></div></div>`
        cardTree.appendChild(card);
      } else {
        const card = document.createElement("div");
        card.classList.add("col-2", "col-medium-3");
        card.innerHTML = `<div class="p-card--game-empty"></div>`
        cardTree.appendChild(card);
        disabledButton = true;
      }
    }
    container.insertBefore(cardTree, container.firstChild);
    // Add click event listener to skill remove buttons
    await document.querySelectorAll(".js-remove-button").forEach(button => {
      button.addEventListener("click", function (event) {
        removeSelectedSkill(event);
      });
    })
    // Enable submit button if 5 skills are selected
    if (!disabledButton) {
      submitButton.disabled = false;
    } else {
      submitButton.disabled = true;
    }
  };

  var skills = [
    {
      name: "Scientist",
      description: "Rigor. Insight. Discovery.",
      details: "I love figuring out how things work and testing the limits of possibility."
    },
    {
      name: "Developer",
      description: "Structure. Correctness. Efficiency.",
      details: "Building quality software in teams is where I find satisfaction."
    },
    {
      name: "Organiser",
      description: "Neat, Planned, Accurate.",
      details: "Figuring out how to steer action in the most efficient and most repeatable way possible."
    },
    {
      name: "Analyzer",
      description: "Data driven. Detailed. Sceptical.",
      details: "Understanding what’s really going on, measuring and testing are where I ground my decisions."
    },
    {
      name: "Manager",
      description: "Hiring. Feedback. Firing.",
      details: "Excellence comes from the whole team; balancing skills and requiring the utmost competence and commitment."
    },
    {
      name: "Helper",
      description: "Caring. Making a difference.",
      details: "Nobody is an expert in everything; sharing expertise and helping people over a hump makes all of us more effective."
    },
    {
      name: "Spokesperson",
      description: "Captivating. Imagineering. Representing.",
      details: "Great work needs great representation. I love to help people understand the new possibility."
    },
    {
      name: "Mentor",
      description: "Developing. Nurturing. Coaching.",
      details: "We all progress faster with the benefit of a trusted and insightful voice."
    },
    {
      name: "Planner",
      description: "Deliberate. Considered. Timely.",
      details: "Wasting time is wasting opportunity; having a great plan makes the most of our strengths."
    },
    {
      name: "Designer",
      description: "Taste. Truth. Delight. Zen.",
      details: "I seek the sweet intersection of purpose, priority and presentation. I make complexity disappear."
    },
    {
      name: "Teacher",
      description: "Understanding. Insights. Growth.",
      details: "We manage, measure, trust and improve what we understand. Spreading knowledge benefits every team."
    },
    {
      name: "Tester",
      description: "White Hat. Criminologist. Fiend. Bacon saver.",
      details: "I bring a proactive dose of cold hard reality, assessing the limits of design and implementation."
    },
    {
      name: "Fixer",
      description: "Triage. Analysis. Experience.",
      details: "I shine when things go sideways in a complex environment. Count on me for correct root cause analysis and rapid, helpful corrective measures."
    },
    {
      name: "Doer",
      description: "Action. Performance. Energy.",
      details: "I get things done, properly, quickly. Deeds count more than words. I raise the energy of everybody around me."
    },
    {
      name: "Seller",
      description: "Commitments. Delivery. Results. Relationships.",
      details: "The right proposition, at the right time, helps both parties. Relationships matter so I always take the long view."
    },
    {
      name: "Inventor",
      description: "Iteration. Perfection. Insight.",
      details: "People need new tools for new kinds of work. Everything can be improved. Count on me to find that better way."
    },
    {
      name: "Stalwart",
      description: "Solid. Productive. Gritty.",
      details: "There will be highs, there will be lows, but you can count on me to get things done and keep things moving regardless."
    },
    {
      name: "Leader",
      description: "Clarity. Mission. Direction.",
      details: "Big wins come to those who can rally their team to focus on something difficult. I earn their confidence and trust."
    },
    {
      name: "Contributor",
      description: "Generous. Open. Giving.",
      details: "We are part of a rising tide of open source because people have been willing to give ideas and work away. I want to be part of that."
    },
    {
      name: "Problem Solver",
      description: "Determined. Constructive.",
      details: "Nothing of consequence goes perfectly smoothly. I like to handle tough situations effectively. I keep cool, I keep priorities clear, I find a way."
    },
    {
      name: "Writer",
      description: "Perfectionist. Poet. Pedant.",
      details: "Words unleash imaginations and inspire change. The right words at the right time will turn the tide of history. I’ll find those words."
    },
    {
      name: "Generalist",
      description: "Mastering mastery. Business, science, style and humanity.",
      details: "Depth is important. Breadth is where I shine - I get deep enough to hold my own with experts in many fields."
    },
    {
      name: "Competitor",
      description: "Situational awareness. Tactics. Agility. Toughness.",
      details: "I play fair and I play to win. The other guys are just as smart as me, but I know how to make the most of the cards I hold."
    },
    {
      name: "Entrepreneur",
      description: "Fortitude. Energy. Insight. Passion. Commerce.",
      details: "I love the business of science, the science of business, and the design of products and organizations."
    },
    {
      name: "Technologist",
      description: "Current. Complex. Ahead.",
      details: "The future arrives in pieces; I like to know what they mean and how they work."
    },
    {
      name: "Traveller",
      description: "Freedom. Exploration. Culture.",
      details: "It’s a small world and I intend to see much of it. Have passport, will travel."
    },
    {
      name: "Conscience",
      description: "The means determine the ends.",
      details: "I am who I am because of how I treat others. Success is only satisfying when it’s fairly won."
    },
  ]
})();