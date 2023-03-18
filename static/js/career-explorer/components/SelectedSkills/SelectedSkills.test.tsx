import "@testing-library/jest-dom";
import { render, screen } from "@testing-library/react";
import React from "react";
import { Skill } from "../../../types";
import SelectedSkills from "./SelectedSkills";

describe("SelectableCard", () => {
  const skillsData: Skill[] = [
    {
      id: 1,
      title: "Red",
      tagline: "ball, flag",
      description: "This is the red electable card element",
    },
    {
      id: 2,
      title: "Green",
      tagline: "grass, apple, tree",
      description: "This is the green selectable card element",
    },
    {
      id: 3,
      title: "White",
      tagline: "snow, paper",
      description: "This is the white selectable card element",
    },
    {
      id: 4,
      title: "Blue",
      tagline: "sea, whale",
      description: "This is the blue selectable card element",
    },
    {
      id: 5,
      title: "Black",
      tagline: "sky, ink",
      description: "This is the black selectable card element",
    },
  ];

  it("renders no skills when none are selected", () => {
    render(<SelectedSkills selectedSkills={[]} skillsData={skillsData} />);
    const selected = screen.queryAllByRole("listitem");
    expect(selected).toHaveLength(0);
  });

  it("renders one skills when one is selected", () => {
    render(<SelectedSkills selectedSkills={[1]} skillsData={skillsData} />);
    expect(screen.getByRole("listitem")).toHaveTextContent("Red");
  });

  it("renders many skills when many are selected", () => {
    render(<SelectedSkills selectedSkills={[1, 3]} skillsData={skillsData} />);
    const selected = screen.getAllByRole("listitem");
    expect(selected).toHaveLength(2);
    const selectedSkills = selected.map((item) => item.textContent);
    expect(selectedSkills).toMatchInlineSnapshot(`
        [
          "Red",
          "White",
        ]
      `);
  });

  it("handles onSubmit correctly", () => {
    render(
      <SelectedSkills
        selectedSkills={[1, 2, 3, 4, 5]}
        skillsData={skillsData}
      />
    );
  });
});
