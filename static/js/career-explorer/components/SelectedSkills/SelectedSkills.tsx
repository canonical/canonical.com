import { Skill } from "../../../types";
import { SkillsData } from "../../utils";

export default function SelectedSkills({ selectedSkills }) {
  const getSkillDetail = (id: number): Skill | undefined => {
    return SkillsData.find((skill: Skill) => skill.id === id);
  };

  return (
    <>
      <p className="u-text--muted">
        Choose 5 that best describe your strengths and ambition:
      </p>
      <ul className="p-inline-list--middot">
        {selectedSkills.map((id: number) => {
          return (
            <li className="p-inline-list__item">{getSkillDetail(id)?.title}</li>
          );
        })}
      </ul>
      <button
        className="p-button--positive js-submit-button"
        disabled={selectedSkills.length < 5}
      >
        Submit choices
      </button>
      <p>
        Or, <a href="/careers/all">see all available roles.</a>
      </p>
    </>
  );
}
