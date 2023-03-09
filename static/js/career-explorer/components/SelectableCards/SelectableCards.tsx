import { Skill } from "../../../types";
import { SkillsData } from "../../utils";
import SelectableCard from "../SelectableCard/SelectableCard";

function SelectableCards({ selectionComplete, onChange }) {
  return (
    <div className="row">
      {SkillsData.map((skill: Skill) => {
        return (
          <SelectableCard
            skill={skill}
            selectionComplete={selectionComplete}
            onChange={onChange}
          />
        );
      })}
    </div>
  );
}

export default SelectableCards;
