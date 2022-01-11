describe("Canonical home page", () => {
  it("should go to the Canonical homepage and accept the cookie policy", () => {
    cy.visit("/");
    cy.acceptCookiePolicy();
  });
});
