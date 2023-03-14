import React from "react";
import { useState } from "react";

const SelectableCard = ({ skill, selectionComplete, onChange }) => {
  const [selected, setSelected] = useState(false);

  const onChangeHandler = () => {
    setSelected(true);
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
      className={`col-3 p-selectable-card${selected ? "--selected" : ""}`}
      data-testid="container"
    >
      <label className="p-checkbox">
        <input
          type="checkbox"
          id={skill.id}
          name="skill"
          className="p-checkbox__input"
          onChange={() => onChangeHandler()}
          disabled={isDisabled()}
          data-testid="input"
        />
        <span
          className="p-checkbox__label p-card--skill__title"
          data-testid="title"
        >
          {skill.title}
        </span>
        <p
          className="p-card--skill__tagline p-heading--6"
          data-testid="tagline"
        >
          {skill.tagline}
        </p>
      </label>
    </div>
  );
};

export default SelectableCard;
