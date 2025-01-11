import "@testing-library/cypress/add-commands";

Cypress.Commands.add("acceptCookiePolicy", () => {
  cy.findByRole("button", { name: "Accept all and visit site" }).click();
});
