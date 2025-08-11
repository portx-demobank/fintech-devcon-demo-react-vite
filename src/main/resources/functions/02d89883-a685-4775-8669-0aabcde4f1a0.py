function transformData(sourceSchemas) {
  const fiserv = sourceSchemas["FiservPersonE2eTest"];
  const result = {
    id: "",
    firstName: "",
    lastName: "",
    emailAddresses: [],
    phoneNumbers: [],
    addresses: []
  };

  // Copy Customer's full legal name from FiservPersonE2eTest.name to ORCA_Person.fullName
  if (fiserv?.name !== undefined) {
    result.fullName = fiserv.name;
  }

  // Copy Customer's family name from FiservPersonE2eTest.structuredName.lastName to ORCA_Person.lastName
  if (fiserv?.structuredName?.lastName !== undefined) {
    result.lastName = fiserv.structuredName.lastName;
  }

  // Copy Customer's given name from FiservPersonE2eTest.structuredName.firstName to ORCA_Person.firstName
  if (fiserv?.structuredName?.firstName !== undefined) {
    result.firstName = fiserv.structuredName.firstName;
  }

  // Copy customer gender designation from FiservPersonE2eTest.gender to ORCA_Person.gender
  if (fiserv?.gender !== undefined) {
    result.gender = fiserv.gender;
  }

  // Copy Customer's middle name from FiservPersonE2eTest.structuredName.middleName to ORCA_Person.middleName
  if (fiserv?.structuredName?.middleName !== undefined) {
    result.middleName = fiserv.structuredName.middleName;
  }

  // Copy Name suffix or generation from FiservPersonE2eTest.structuredName.suffix to ORCA_Person.suffix
  if (fiserv?.structuredName?.suffix !== undefined) {
    result.suffix = fiserv.structuredName.suffix;
  }

  // Copy Customer date of birth from FiservPersonE2eTest.placeAndDateOfBirth.birthDate to ORCA_Person.birthDate
  if (fiserv?.placeAndDateOfBirth?.birthDate !== undefined) {
    result.birthDate = fiserv.placeAndDateOfBirth.birthDate;
  }

  // Copy Birth information from FiservPersonE2eTest.placeAndDateOfBirth to ORCA_Person.placeAndDateOfBirth
  if (fiserv?.placeAndDateOfBirth !== undefined) {
    result.placeAndDateOfBirth = {
      birthDate: fiserv.placeAndDateOfBirth.birthDate
    };
  }

  // Copy Customer date of birth from FiservPersonE2eTest.placeAndDateOfBirth.birthDate to ORCA_Person.placeAndDateOfBirth.birthDate
  if (fiserv?.placeAndDateOfBirth?.birthDate !== undefined && result.placeAndDateOfBirth) {
    result.placeAndDateOfBirth.birthDate = fiserv.placeAndDateOfBirth.birthDate;
  }

  // Copy Tax identification number from FiservPersonE2eTest.taxInformation.tin to ORCA_Person.taxId
  if (fiserv?.taxInformation?.tin !== undefined) {
    result.taxId = fiserv.taxInformation.tin;
  }

  // Copy Customer tax status from FiservPersonE2eTest.taxInformation.taxStatus to ORCA_Person.taxStatus
  if (fiserv?.taxInformation?.taxStatus !== undefined) {
    result.taxStatus = fiserv.taxInformation.taxStatus;
  }

  // Copy Customer classification code from FiservPersonE2eTest.customerType to ORCA_Person.customerType
  if (fiserv?.customerType !== undefined) {
    result.customerType = String(fiserv.customerType);
  }

  // Copy customer account status from FiservPersonE2eTest.audit.status to ORCA_Person.status
  if (fiserv?.audit?.status !== undefined) {
    result.status = fiserv.audit.status;
  }

  // Copy Customer's preferred language from FiservPersonE2eTest.contact.preferredLanguage to ORCA_Person.preferredLanguage
  if (fiserv?.contact?.preferredLanguage !== undefined) {
    result.preferredLanguage = fiserv.contact.preferredLanguage;
  }

  // Copy job title of the person from FiservPersonE2eTest.contact.phones.comment to TargetSchema.jobTitle
  if (fiserv?.jobTitle !== undefined) {
    result.jobTitle = fiserv.jobTitle;
  }

  // Copy Email address from FiservPersonE2eTest.contact.emails[].emailAddress to ORCA_Person.emailAddresses[].address
  if (fiserv?.contact?.emails && Array.isArray(fiserv.contact.emails)) {
    result.emailAddresses = fiserv.contact.emails.map(email => ({
      address: email.emailAddress
    })).filter(item => item.address !== undefined);
  }

  // Copy Phone number from FiservPersonE2eTest.contact.phones[].number to ORCA_Person.phoneNumbers[].number
  if (fiserv?.contact?.phones && Array.isArray(fiserv.contact.phones)) {
    result.phoneNumbers = fiserv.contact.phones.map(phone => ({
      number: phone.number,
      type: phone.phoneType
    })).filter(item => item.number !== undefined);
  }

  // Copy Type of phone from FiservPersonE2eTest.contact.phones[].phoneType to ORCA_Person.phoneNumbers[].type
  // (handled in the above mapping)

  // Copy Street address lines from FiservPersonE2eTest.contact.postalAddresses[].addressLines[] to ORCA_Person.addresses[].line1
  if (fiserv?.contact?.postalAddresses && Array.isArray(fiserv.contact.postalAddresses)) {
    result.addresses = fiserv.contact.postalAddresses.map((address, index) => {
      const newAddress = {
        addressId: `A${index + 1001}`,
        line1: Array.isArray(address.addressLines) && address.addressLines.length > 0 ? address.addressLines[0] : "",
        line2: Array.isArray(address.addressLines) && address.addressLines.length > 1 ? address.addressLines[1] : "",
        city: "",
        state: "",
        postalCode: address.postCode,
        country: address.country
      };
      return newAddress;
    }).filter(addr => addr.line1 !== undefined && addr.postalCode !== undefined);
  }

  // Copy Country code from FiservPersonE2eTest.contact.postalAddresses[].country to ORCA_Person.addresses[].country
  // (handled in the above mapping)

  // Copy Postal or ZIP code from FiservPersonE2eTest.contact.postalAddresses[].postCode to ORCA_Person.addresses[].postalCode
  // (handled in the above mapping)

  // Copy Customer identification documents from FiservPersonE2eTest.identifiers to ORCA_Person.identifiers
  if (fiserv?.identifiers && Array.isArray(fiserv.identifiers)) {
    result.identifiers = fiserv.identifiers.map(identifier => ({
      number: identifier.number,
      schemeName: identifier.schemeName,
      issuer: identifier.issuer,
      issueDate: identifier.issueDate,
      expirationDate: identifier.expirationDate
    })).filter(item => item.number !== undefined && item.schemeName !== undefined);
  }

  // Copy Customer communication preferences from FiservPersonE2eTest.communicationChannels to ORCA_Person.communicationChannels
  if (fiserv?.communicationChannels && Array.isArray(fiserv.communicationChannels)) {
    result.communicationChannels = fiserv.communicationChannels.map(channel => ({
      channel: channel.name,
      primaryIndicator: channel.primaryContactIndicator
    })).filter(item => item.channel !== undefined);
  }

  // Copy Communication channel name from FiservPersonE2eTest.communicationChannels[].name to ORCA_Person.communicationChannels[].channel
  // (handled in the above mapping)

  // Copy Indicates primary contact method from FiservPersonE2eTest.communicationChannels[].primaryContactIndicator to ORCA_Person.communicationChannels[].primaryIndicator
  // (handled in the above mapping)

  // Copy audit information
  if (fiserv?.audit) {
    result.audit = {};
    
    // Copy record creation timestamp from FiservPersonE2eTest.audit.creationDate to ORCA_Person.audit.creationDate
    if (fiserv.audit.creationDate !== undefined) {
      result.audit.creationDate = fiserv.audit.creationDate;
    }
    
    // Copy last updated timestamp from FiservPersonE2eTest.audit.lastModificationDate to ORCA_Person.audit.lastModificationDate
    if (fiserv.audit.lastModificationDate !== undefined) {
      result.audit.lastModificationDate = fiserv.audit.lastModificationDate;
    }
    
    // Copy last modification method from FiservPersonE2eTest.audit.lastModificationChannel to ORCA_Person.audit.lastModificacionChannel
    if (fiserv.audit.lastModificationChannel !== undefined) {
      result.audit.lastModificacionChannel = fiserv.audit.lastModificationChannel;
    }
    
    // Copy customer account status from FiservPersonE2eTest.audit.status to ORCA_Person.audit.status
    if (fiserv.audit.status !== undefined) {
      result.audit.status = fiserv.audit.status;
    }
  }

  return result;
}