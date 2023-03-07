import React, { useState } from "react";

export default function SelectedSkills({ selectedSkills }) {
  console.log("test", selectedSkills);

  return (
    <>
      <p className="u-text--muted">
        Choose 5 that best describe your strengths and ambition:
      </p>
      <p>{selectedSkills.length ? selectedSkills : "No Skills"}</p>
      <button className="p-button--positive js-submit-button" disabled={true}>
        Submit choices
      </button>
      <p>
        Or, <a href="/careers/all">see all available roles.</a>
      </p>
    </>
  );
}
