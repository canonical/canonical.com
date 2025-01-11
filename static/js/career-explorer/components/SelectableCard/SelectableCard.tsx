import React, { useState } from "react";
import { Skill } from "../../../types";

interface SelectableCardProps {
  skill: Skill;
  selectionComplete: boolean;
  onChange: (value: number) => void;
}

const SelectableCard = ({ skill, selectionComplete, onChange }: SelectableCardProps) => {
  const [selected, setSelected] = useState(false);

  const onChangeHandler = () => {
    setSelected(!selected);
    onChange(skill.id);
  };

  const isDisabled = () => {
    if (selectionComplete && !selected) {
      return true;
    } else {
      return false;
    }
  };

  return (
    <div
      className={`col-3 col-medium-3 p-selectable-card${
        selected ? "--selected" : ""
      }`}
      data-testid="container"
    >
      <label className="p-checkbox">
        <input
          type="checkbox"
          id={String(skill.id)}
          name="skill"
          className="p-checkbox__input"
          onChange={() => onChangeHandler()}
          disabled={isDisabled()}
          data-testid="input"
        />
        <strong className="p-checkbox__label" data-testid="title">
          {skill.title}
        </strong>
        <p className="p-selectable-card__tagline" data-testid="tagline">
          {skill.tagline}
        </p>
      </label>
    </div>
  );
};

export default SelectableCard;
