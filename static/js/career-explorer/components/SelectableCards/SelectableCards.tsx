import React from "react";
import { Skill } from "../../../types";
import SelectableCard from "../SelectableCard/SelectableCard";

interface SelectableCardsProps {
  selectionComplete: boolean;
  onChange: (value: number) => void;
  skillsData: Skill[];
}

function SelectableCards({ selectionComplete, onChange, skillsData }: SelectableCardsProps) {
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
