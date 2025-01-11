import React from "react";
import { Skill } from "../../../types";

interface SelectedSkillsProps {
  selectedSkills: number[];
  skillsData: Skill[];
}

export default function SelectedSkills({ selectedSkills, skillsData }: SelectedSkillsProps) {
  const getSkillDetail = (id: number): Skill | undefined => {
    return skillsData.find((skill: Skill) => skill.id === id);
  };

  const handleSubmit = (): void => {
    let skillsCombined = "";
    let comma = "";

    selectedSkills.forEach((id) => {
      skillsCombined += `${getSkillDetail(id)?.title}${comma}`;
      comma = ",";
    });

    location.href = "results?core-skills=" + skillsCombined;
  };

  const getUnselectedSkills = (): Array<string> => {
    let count = 5 - selectedSkills.length;
    const unselectedArray = [];
    while (count) {
      unselectedArray.push(`unselected-${count}`);
      count--;
    }
    return unselectedArray;
  };

  return (
    <>
      <p className="u-text--muted">
        Choose 5 that best describe your strengths and ambition:
      </p>
      <ul role="list" className="p-inline-list--selection">
        {selectedSkills.map((id: number) => {
          return (
            <li
              role="listitem"
              className="p-inline-list__item"
              data-testid="selected"
              key={id}
            >
              {getSkillDetail(id)?.title}
            </li>
          );
        })}
        {getUnselectedSkills().map((key: string) => {
          return (
            <li
              role="listitem"
              className="p-inline-list__item--empty"
              key={key}
              data-testid="empty"
            >
              &nbsp;
            </li>
          );
        })}
      </ul>
      <button
        className="p-button--positive"
        disabled={selectedSkills.length < 5}
        onClick={() => handleSubmit()}
        data-testid="submit"
      >
        Submit choices
      </button>
      <p>
        Or, <a href="/careers/all">see all available roles.</a>
      </p>
    </>
  );
}
