import "@testing-library/jest-dom";
import { render, screen } from "@testing-library/react";
import React from "react";
import { Skill } from "../../../types";
import SelectableCards from "./SelectableCards";

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
  ];
  const selectionComplete = false;
  const onChange = jest.fn();

  it("renders the correct amount of cards", async () => {
    render(
      <SelectableCards
        selectionComplete={selectionComplete}
        onChange={onChange}
        skillsData={skillsData}
      />
    );
    const cards = await screen.findAllByTestId("container");
    expect(cards).toHaveLength(3);
  });
});
