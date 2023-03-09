import "@testing-library/jest-dom";
import { render, screen } from "@testing-library/react";
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

  it("renders", () => {
    render(
      <SelectableCard
        skill={skill}
        selectionComplete={selectionComplete}
        onChange={onChange}
      />
    );
    expect(screen.getByText("Test")).toBeInTheDocument();
  });
});
