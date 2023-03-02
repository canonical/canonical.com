import React from "react";

function SelectedSkills() {
  return (
    <>
      <p className="u-text--muted">
        Choose 5 that best describe your strengths and ambition:
      </p>
      <ul className="row js-selected-skills">
        <li
          className="col-small-1 col-medium-1 col-1 selected-skills"
          id="selected-1"
        ></li>
        <li
          className="col-small-1 col-medium-1 col-1 selected-skills"
          id="selected-2"
        ></li>
        <li
          className="col-small-1 col-medium-1 col-1 selected-skills"
          id="selected-3"
        ></li>
        <li
          className="col-small-1 col-medium-1 col-1 selected-skills"
          id="selected-4"
        ></li>
        <li
          className="col-small-1 col-medium-1 col-1 selected-skills"
          id="selected-5"
        ></li>
      </ul>
      <button className="p-button--positive js-submit-button" disabled={true}>
        Submit choices
      </button>
      <p>
        Or, <a href="/careers/all">see all available roles.</a>
      </p>
    </>
  );
}

export default SelectedSkills;
