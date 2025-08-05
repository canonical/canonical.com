import React from "react";
import { useSignForm } from "../../contexts/SignForm";
import { AgreementType } from "../../utils/constants";
import IndividualContactForm from "./IndividualContactForm";
import OrganizationContactForm from "./OrganizationContactForm";

const ContactDetailsForm = () => {
  const { agreementType } = useSignForm();
  const contactForm: Record<AgreementType, () => React.ReactElement> = {
    individual: IndividualContactForm,
    organization: OrganizationContactForm,
  };
  if (!agreementType) {
    return null;
  }
  return (
    <fieldset>
      <legend className="p-heading--3">Your contact details</legend>
      {contactForm[agreementType]()}
    </fieldset>
  );
};

export default ContactDetailsForm;
