import React from "react";
import { Skill } from "../../../types";
import SelectableCard from "../SelectableCard/SelectableCard";

function SelectableCards({ selectionComplete, onChange, skillsData }) {
  return (
    <div className="row">
      {skillsData.map((skill: Skill) => {
        return (
          <SelectableCard
            skill={skill}
            selectionComplete={selectionComplete}
            onChange={onChange}
            key={skill.id}
          />
        );
      })}
    </div>
  );
}

export default SelectableCards;
