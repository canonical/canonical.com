import React from "react";
import { Skill } from "../../../types";
import { SkillsData } from "../../utils";
import SelectableCard from "../SelectableCard/SelectableCard";

function SelectableCards() {
  return (
    <div className="row">
      {SkillsData.map((skill: Skill) => {
        return <SelectableCard skill={skill} />;
      })}
    </div>
  );
}

export default SelectableCards;
