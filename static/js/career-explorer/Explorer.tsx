import React from "react";
import SelectableCards from "./components/SelectableCards/SelectableCards";
import SelectedSkills from "./components/SelectedSkills/SelectedSkills";

function Explorer() {
  return (
    <>
      <section className="p-strip">
        <div className="row">
          <div className="col-6">
            <h1 className="p-heading--2">What kind of excellent are you?</h1>
          </div>
          <div className="col-6">
            <SelectedSkills />
          </div>
        </div>

        <SelectableCards />
      </section>
    </>
  );
}

export default Explorer;
