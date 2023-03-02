import React, { useState } from "react";

const SelectableCard = ({ skill }) => {
  const [selected, setSelected] = useState(false);

  const getClassName = () => {
    return `col-3 p-selectable-card${selected ? "--selected" : ""}`;
  };

  return (
    <div className={getClassName()}>
      <form>
        <label className="p-checkbox">
          <input
            type="checkbox"
            id={skill.id}
            name="skill-card"
            className="p-checkbox__input"
            onChange={(e) => {
              setSelected(true);
            }}
          />
          <span className="p-checkbox__label p-card--skill__title">
            {skill.title}
          </span>
        </label>
        <p className="p-card--skill__tagline p-heading--6">{skill.tagline}</p>
      </form>
    </div>
  );
};

export default SelectableCard;
