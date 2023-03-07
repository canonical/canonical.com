import React, { useState } from "react";

const SelectableCard = ({ skill, selectedSkills, onChange }) => {
  const getClassName = (id) => {
    return `col-3 p-selectable-card${selectedSkills.map((skill) =>
      skill.id === id ? "--selected" : ""
    )}}`;
  };

  return (
    <div className={getClassName(selectedSkills.id)}>
      <form>
        <label className="p-checkbox">
          <input
            type="checkbox"
            id={skill.id}
            name="skill-card"
            className="p-checkbox__input"
            onChange={() => onChange(skill.id)}
          />
          <span className="p-checkbox__label p-card--skill__title">
            {skill.title}
          </span>
          <p className="p-card--skill__tagline p-heading--6">{skill.tagline}</p>
        </label>
      </form>
    </div>
  );
};

export default SelectableCard;
