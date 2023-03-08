import React from "react";
import { Skill } from "../../../types";
import { SkillsData } from "../../utils";
import SelectableCard from "../SelectableCard/SelectableCard";

function SelectableCards({ selectedSkills, selectionComplete, onChange }) {
  return (
    <div className="row">
      {SkillsData.map((skill: Skill) => {
        return (
          <SelectableCard
            skill={skill}
            selectedSkills={selectedSkills}
            selectionComplete={selectionComplete}
            onChange={onChange}
          />
        );
      })}
    </div>
  );
}

export default SelectableCards;
