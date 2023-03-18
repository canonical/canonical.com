import React from "react";
import { Skill } from "../../../types";

export default function SelectedSkills({ selectedSkills, skillsData }) {
  const getSkillDetail = (id: number): Skill | undefined => {
    return skillsData.find((skill: Skill) => skill.id === id);
  };

  const handleSubmit = () => {
    let skillsCombined = "";
    let comma = "";

    selectedSkills.forEach((id) => {
      skillsCombined += `${getSkillDetail(id)?.title}${comma}`;
      comma = ",";
    });

    location.href = "results?core-skills=" + skillsCombined;
  };

  return (
    <>
      <p className="u-text--muted">
        Choose 5 that best describe your strengths and ambition:
      </p>
      <ul role="list" className="p-inline-list--selection">
        {selectedSkills.map((id: number) => {
          return (
            <li role="listitem" className="p-inline-list__item" key={id}>
              {getSkillDetail(id)?.title}
            </li>
          );
        })}
      </ul>
      <button
        className="p-button--positive"
        disabled={selectedSkills.length < 5}
        onClick={() => handleSubmit()}
      >
        Submit choices
      </button>
      <p>
        Or, <a href="/careers/all">see all available roles.</a>
      </p>
    </>
  );
}
