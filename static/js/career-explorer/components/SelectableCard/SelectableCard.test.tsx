import "@testing-library/jest-dom";
import { fireEvent, render, screen } from "@testing-library/react";
import React from "react";
import { Skill } from "../../../types";
import SelectableCard from "./SelectableCard";

describe("SelectableCard", () => {
  const skill: Skill = {
    id: 1,
    title: "Test",
    tagline: "tag1, tag2, tag3",
    description: "This is a selectable card element",
  };
  const selectionComplete = false;
  const onChange = jest.fn();

  it("renders the default state", () => {
    render(
      <SelectableCard
        skill={skill}
        selectionComplete={selectionComplete}
        onChange={onChange}
      />
    );
    expect(screen.getByTestId("title")).toHaveTextContent("Test");
    expect(screen.getByTestId("tagline")).toHaveTextContent("tag1, tag2, tag3");
    expect(screen.getByTestId("container")).toHaveClass("p-selectable-card");
    expect(screen.getByTestId("input")).not.toBeDisabled();
  });

  it("sets selected class when input checked", () => {
    render(
      <SelectableCard
        skill={skill}
        selectionComplete={selectionComplete}
        onChange={onChange}
      />
    );
    fireEvent.click(screen.getByTestId("input"));
    expect(screen.getByTestId("container")).toHaveClass(
      "p-selectable-card--selected"
    );
  });

  it("disbales selection when the selection is complete", () => {
    render(
      <SelectableCard
        skill={skill}
        selectionComplete={true}
        onChange={onChange}
      />
    );
    expect(screen.getByTestId("input")).toBeDisabled();
  });

  it("calls the callback when changed", () => {
    render(
      <SelectableCard
        skill={skill}
        selectionComplete={selectionComplete}
        onChange={onChange}
      />
    );
    fireEvent.click(screen.getByTestId("input"));
    expect(onChange).toHaveBeenCalled();
  });
});
