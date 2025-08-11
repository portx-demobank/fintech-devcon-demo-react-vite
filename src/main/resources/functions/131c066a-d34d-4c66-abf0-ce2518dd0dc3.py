
function transformData(sourceSchemas) {
  const fiservPerson = sourceSchemas["FiservPersonE2eTest"];
  const result = {
    id: "",
    firstName: "",
    lastName: "",
    emailAddresses: [],
    phoneNumbers: [],
    addresses: [],
    audit: {}
  };

  // Copy Record creation timestamp
  if (fiservPerson?.audit?.creationDate) {
    result.audit.creationDate = fiservPerson.audit.creationDate;
  }

  // Copy identifiers array with date of issuance
  if (fiservPerson?.identifiers && Array.isArray(fiservPerson.identifiers)) {
    result.identifiers = fiservPerson.identifiers.map(identifier => {
      const mappedIdentifier = {};
      
      if (identifier?.issueDate) {
        mappedIdentifier.issueDate = identifier.issueDate;
      }
      
      if (identifier?.schemeName) {
        mappedIdentifier.schemeName = identifier.schemeName;
      }
      
      if (identifier?.issuer) {
        mappedIdentifier.issuer = identifier.issuer;
      }
      
      if (identifier?.number) {
        mappedIdentifier.number = identifier.number;
      }
      
      if (identifier?.expirationDate) {
        mappedIdentifier.expirationDate = identifier.expirationDate;
      }
      
      return mappedIdentifier;
    });
  }

  // Copy email addresses with purpose mapping to type
  if (fiservPerson?.contact?.emails && Array.isArray(fiservPerson.contact.emails)) {
    result.emailAddresses = fiservPerson.contact.emails.map(email => {
      const mappedEmail = {};
      
      if (email?.emailPurpose) {
        mappedEmail.type = email.emailPurpose;
      }
      
      if (email?.emailAddress) {
        mappedEmail.address = email.emailAddress;
      }
      
      return mappedEmail;
    });
  }

  // Copy Last modified timestamp
  if (fiservPerson?.audit?.lastModificationDate) {
    result.audit.lastModificationDate = fiservPerson.audit.lastModificationDate;
  }

  // Copy Customer classification code
  if (fiservPerson?.customerType) {
    result.customerType = fiservPerson.customerType;
  }

  // Copy Current record status
  if (fiservPerson?.audit?.status) {
    result.audit.status = fiservPerson.audit.status;
  }

  // Copy Customer's birth date to placeAndDateOfBirth
  if (!result.placeAndDateOfBirth && fiservPerson?.placeAndDateOfBirth?.birthDate) {
    result.placeAndDateOfBirth = {
      birthDate: fiservPerson.placeAndDateOfBirth.birthDate
    };
  } else if (fiservPerson?.placeAndDateOfBirth?.birthDate) {
    result.placeAndDateOfBirth.birthDate = fiservPerson.placeAndDateOfBirth.birthDate;
  }

  // Copy Customer's middle name
  if (fiservPerson?.structuredName?.middleName) {
    result.middleName = fiservPerson.structuredName.middleName;
  }

  // Copy Customer's given name
  if (fiservPerson?.structuredName?.firstName) {
    result.firstName = fiservPerson.structuredName.firstName;
  }

  // Copy Customer's gender designation
  if (fiservPerson?.gender) {
    result.gender = fiservPerson.gender;
  }

  // Copy postal addresses with country and address lines
  if (fiservPerson?.contact?.postalAddresses && Array.isArray(fiservPerson.contact.postalAddresses)) {
    result.addresses = fiservPerson.contact.postalAddresses.map((address, index) => {
      const mappedAddress = {
        addressId: `A${index + 1001}` // Generate an addressId since it's required
      };
      
      if (address?.country) {
        mappedAddress.country = address.country;
      }
      
      if (address?.addressLines && address.addressLines.length > 0) {
        mappedAddress.line1 = address.addressLines[0];
      } else {
        mappedAddress.line1 = ""; // Required field
      }
      
      if (address?.addressLines && address.addressLines.length > 1) {
        mappedAddress.line2 = address.addressLines[1];
      }
      
      if (address?.postCode) {
        mappedAddress.postalCode = address.postCode;
      } else {
        mappedAddress.postalCode = ""; // Required field
      }
      
      // Add empty city and state as they're required fields
      mappedAddress.city = "";
      mappedAddress.state = "";
      
      return mappedAddress;
    });
  }

  // Copy Last modification channel
  if (fiservPerson?.audit?.lastModificationChannel) {
    result.audit.lastModificacionChannel = fiservPerson.audit.lastModificationChannel;
  }

  // Copy Communication channels
  if (fiservPerson?.communicationChannels && Array.isArray(fiservPerson.communicationChannels)) {
    result.communicationChannels = fiservPerson.communicationChannels.map(channel => {
      const mappedChannel = {};
      
      if (channel?.name) {
        mappedChannel.channel = channel.name;
      }
      
      if (channel?.primaryContactIndicator !== undefined) {
        mappedChannel.primaryIndicator = channel.primaryContactIndicator;
      }
      
      return mappedChannel;
    });
  }

  // Copy Customer's preferred language
  if (fiservPerson?.contact?.preferredLanguage) {
    result.preferredLanguage = fiservPerson.contact.preferredLanguage;
  }

  // Copy Customer's family name
  if (fiservPerson?.structuredName?.lastName) {
    result.lastName = fiservPerson.structuredName.lastName;
  }

  // Copy phone numbers with type
  if (fiservPerson?.contact?.phones && Array.isArray(fiservPerson.contact.phones)) {
    result.phoneNumbers = fiservPerson.contact.phones.map(phone => {
      const mappedPhone = {};
      
      if (phone?.phoneType) {
        mappedPhone.type = phone.phoneType;
      }
      
      if (phone?.number) {
        mappedPhone.number = phone.number;
      } else {
        mappedPhone.number = ""; // Required field
      }
      
      return mappedPhone;
    });
  }

  // Copy Customer tax filing status
  if (fiservPerson?.taxInformation?.taxStatus) {
    result.taxStatus = fiservPerson.taxInformation.taxStatus;
  }

  // Copy Tax identification number
  if (fiservPerson?.taxInformation?.tin) {
    result.taxId = fiservPerson.taxInformation.tin;
  }

  // Copy Customer's full name
  if (fiservPerson?.name) {
    result.fullName = fiservPerson.name;
  }

  // Copy job title
  if (fiservPerson?.contact?.phones && Array.isArray(fiservPerson.contact.phones)) {
    const phone = fiservPerson.contact.phones[0];
    if (phone?.comment) {
      result.jobTitle = phone.comment;
    }
  }

  // Copy Customer's birth date directly
  if (fiservPerson?.placeAndDateOfBirth?.birthDate) {
    result.birthDate = fiservPerson.placeAndDateOfBirth.birthDate;
  }

  // Copy Name suffix
  if (fiservPerson?.structuredName?.suffix) {
    result.suffix = fiservPerson.structuredName.suffix;
  }

  return result;
}
