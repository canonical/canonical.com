import React, { useState } from "react";
import SelectableCards from "./components/SelectableCards/SelectableCards";
import SelectedSkills from "./components/SelectedSkills/SelectedSkills";

export default function Explorer() {
  const [selectedSkills, setSelectedSkills] = useState([] as number[]);
  const [selectionComplete, setselectionComplete] = useState(false);
  const handleOnChange = (position: number) => {
    let updatedSkills = [...selectedSkills];
    const index = updatedSkills.indexOf(position);
    if (index !== -1) {
      updatedSkills.splice(index, 1);
    } else {
      updatedSkills.push(position);
    }
    if (updatedSkills.length >= 5) {
      setselectionComplete(true);
    } else {
      setselectionComplete(false);
    }
    setSelectedSkills(updatedSkills);
  };

  return (
    <>
      <section className="p-strip">
        <div className="row">
          <div className="col-6">
            <h1 className="p-heading--2">What kind of excellent are you?</h1>
          </div>
          <div className="col-6">
            <SelectedSkills selectedSkills={selectedSkills} />
          </div>
        </div>
        <SelectableCards
          selectedSkills={selectedSkills}
          selectionComplete={selectionComplete}
          onChange={handleOnChange}
        />
      </section>
    </>
  );
}
