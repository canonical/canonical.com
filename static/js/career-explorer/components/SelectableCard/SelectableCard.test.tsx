import { render, screen } from "@testing-library/react";
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

  it("renders", () => {
    render(<SelectableCard skill={skill} />);
    expect(screen.getByText("Test")).toBeInTheDocument();
  });
});
