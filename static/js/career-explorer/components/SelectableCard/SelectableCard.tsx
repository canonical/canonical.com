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
    <div className={`col-3 p-selectable-card${selected ? "--selected" : ""}`}>
      <form>
        <label className="p-checkbox">
          <input
            type="checkbox"
            id={skill.id}
            name="skill-card"
            className="p-checkbox__input"
            onChange={() => onChangeHandler()}
            disabled={isDisabled()}
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
