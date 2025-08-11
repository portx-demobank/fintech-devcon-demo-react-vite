function transformData(sourceSchemas) {
  // Early return if source schema doesn't exist
  if (!sourceSchemas || !sourceSchemas["FiservPersonE2eTest"]) {
    return {};
  }

  const source = sourceSchemas["FiservPersonE2eTest"];
  const target = {
    id: "",
    firstName: "",
    lastName: "",
    emailAddresses: [],
    phoneNumbers: [],
    addresses: []
  };

  // Copy Customer's full legal name from FiservPersonE2eTest.name to ORCA_Person.fullName
  if (source?.name !== undefined) {
    target.fullName = source.name;
  }

  // Copy Customer's family name from FiservPersonE2eTest.structuredName.lastName to ORCA_Person.lastName
  if (source?.structuredName?.lastName !== undefined) {
    target.lastName = source.structuredName.lastName;
  }

  // Copy Customer's given name from FiservPersonE2eTest.structuredName.firstName to ORCA_Person.firstName
  if (source?.structuredName?.firstName !== undefined) {
    target.firstName = source.structuredName.firstName;
  }

  // Copy Customer's middle name from FiservPersonE2eTest.structuredName.middleName to ORCA_Person.middleName
  if (source?.structuredName?.middleName !== undefined) {
    target.middleName = source.structuredName.middleName;
  }

  // Copy Name suffix or generation from FiservPersonE2eTest.structuredName.suffix to ORCA_Person.suffix
  if (source?.structuredName?.suffix !== undefined) {
    target.suffix = source.structuredName.suffix;
  }

  // Copy customer gender designation from FiservPersonE2eTest.gender to ORCA_Person.gender
  if (source?.gender !== undefined) {
    // Map the gender values from number to string
    if (source.gender === "1") {
      target.gender = "Male";
    } else if (source.gender === "2") {
      target.gender = "Female";
    }
  }

  // Copy Customer date of birth from FiservPersonE2eTest.placeAndDateOfBirth.birthDate to ORCA_Person.birthDate
  if (source?.placeAndDateOfBirth?.birthDate !== undefined) {
    target.birthDate = source.placeAndDateOfBirth.birthDate;
  }

  // Copy Customer date of birth from FiservPersonE2eTest.placeAndDateOfBirth.birthDate to ORCA_Person.placeAndDateOfBirth.birthDate
  if (source?.placeAndDateOfBirth?.birthDate !== undefined) {
    if (!target.placeAndDateOfBirth) {
      target.placeAndDateOfBirth = {};
    }
    target.placeAndDateOfBirth.birthDate = source.placeAndDateOfBirth.birthDate;
  }

  // Copy Birth information from FiservPersonE2eTest.placeAndDateOfBirth to ORCA_Person.placeAndDateOfBirth
  if (source?.placeAndDateOfBirth) {
    if (!target.placeAndDateOfBirth) {
      target.placeAndDateOfBirth = {};
    }
    // We already handled birthDate above, so we don't need to copy it again
  }

  // Copy Tax identification number from FiservPersonE2eTest.taxInformation.tin to ORCA_Person.taxId
  if (source?.taxInformation?.tin !== undefined) {
    target.taxId = source.taxInformation.tin;
  }

  // Copy Customer tax status from FiservPersonE2eTest.taxInformation.taxStatus to ORCA_Person.taxStatus
  if (source?.taxInformation?.taxStatus !== undefined) {
    target.taxStatus = source.taxInformation.taxStatus;
  }

  // Copy Customer classification code from FiservPersonE2eTest.customerType to ORCA_Person.customerType
  if (source?.customerType !== undefined) {
    // Map numeric customer type to string enum
    switch (source.customerType) {
      case 1:
        target.customerType = "Personal";
        break;
      case 2:
        target.customerType = "Business";
        break;
      default:
        // Leave undefined if not matching
        break;
    }
  }

  // Copy job title of the person from FiservPersonE2eTest.contact.phones.comment to TargetSchema.jobTitle
  if (source?.contact?.phones && source.contact.phones.length > 0 && source.contact.phones[0]?.comment !== undefined) {
    target.jobTitle = source.contact.phones[0].comment;
  }

  // Copy customer account status from FiservPersonE2eTest.audit.status to ORCA_Person.status
  if (source?.audit?.status !== undefined) {
    target.status = source.audit.status;
  }

  // Copy Customer's preferred language from FiservPersonE2eTest.contact.preferredLanguage to ORCA_Person.preferredLanguage
  if (source?.contact?.preferredLanguage !== undefined) {
    target.preferredLanguage = source.contact.preferredLanguage;
  }

  // Copy record creation timestamp from FiservPersonE2eTest.audit.creationDate to ORCA_Person.audit.creationDate
  if (source?.audit?.creationDate !== undefined) {
    if (!target.audit) {
      target.audit = {};
    }
    target.audit.creationDate = source.audit.creationDate;
  }

  // Copy last updated timestamp from FiservPersonE2eTest.audit.lastModificationDate to ORCA_Person.audit.lastModificationDate
  if (source?.audit?.lastModificationDate !== undefined) {
    if (!target.audit) {
      target.audit = {};
    }
    target.audit.lastModificationDate = source.audit.lastModificationDate;
  }

  // Copy last modification method from FiservPersonE2eTest.audit.lastModificationChannel to ORCA_Person.audit.lastModificacionChannel
  if (source?.audit?.lastModificationChannel !== undefined) {
    if (!target.audit) {
      target.audit = {};
    }
    target.audit.lastModificacionChannel = source.audit.lastModificationChannel;
  }

  // Copy Email address from FiservPersonE2eTest.contact.emails[].emailAddress to ORCA_Person.emailAddresses[].address
  if (source?.contact?.emails && Array.isArray(source.contact.emails)) {
    source.contact.emails.forEach(email => {
      if (email?.emailAddress !== undefined) {
        const targetEmail = {
          address: email.emailAddress
        };
        if (email?.emailPurpose) {
          // Map purpose to type if available
          switch (email.emailPurpose.toLowerCase()) {
            case "personal":
              targetEmail.type = "Personal";
              break;
            case "business":
              targetEmail.type = "Work";
              break;
            default:
              targetEmail.type = "Other";
              break;
          }
        }
        target.emailAddresses.push(targetEmail);
      }
    });
  }

  // Copy Phone number from FiservPersonE2eTest.contact.phones[].number to ORCA_Person.phoneNumbers[].number
  // Copy Type of phone from FiservPersonE2eTest.contact.phones[].phoneType to ORCA_Person.phoneNumbers[].type
  if (source?.contact?.phones && Array.isArray(source.contact.phones)) {
    source.contact.phones.forEach(phone => {
      if (phone?.number !== undefined) {
        const targetPhone = {
          number: phone.number
        };
        if (phone?.phoneType !== undefined) {
          // Map phone types
          switch (phone.phoneType.toLowerCase()) {
            case "home":
              targetPhone.type = "Home";
              break;
            case "mobile":
              targetPhone.type = "Mobile";
              break;
            case "work":
              targetPhone.type = "Work";
              break;
            default:
              targetPhone.type = "Other";
              break;
          }
        }
        target.phoneNumbers.push(targetPhone);
      }
    });
  }

  // Copy Street address lines from FiservPersonE2eTest.contact.postalAddresses[].addressLines[] to ORCA_Person.addresses[].line1
  // Copy Country code from FiservPersonE2eTest.contact.postalAddresses[].country to ORCA_Person.addresses[].country
  // Copy Postal or ZIP code from FiservPersonE2eTest.contact.postalAddresses[].postCode to ORCA_Person.addresses[].postalCode
  if (source?.contact?.postalAddresses && Array.isArray(source.contact.postalAddresses)) {
    source.contact.postalAddresses.forEach((address, index) => {
      const targetAddress = {
        addressId: `A${1000 + index}`, // Generate an address ID
        line1: "",
        city: "", // Required field but no source mapping
        state: "", // Required field but no source mapping
        postalCode: ""
      };

      if (address?.addressLines && Array.isArray(address.addressLines) && address.addressLines.length > 0) {
        targetAddress.line1 = address.addressLines[0];
        if (address.addressLines.length > 1) {
          targetAddress.line2 = address.addressLines[1];
        }
      }

      if (address?.country !== undefined) {
        targetAddress.country = address.country;
      }

      if (address?.postCode !== undefined) {
        targetAddress.postalCode = address.postCode;
      }

      target.addresses.push(targetAddress);
    });
  }

  // Copy Customer identification documents from FiservPersonE2eTest.identifiers to ORCA_Person.identifiers
  // Copy ID document number from FiservPersonE2eTest.identifiers[].number to ORCA_Person.identifiers[].number
  // Copy Type of identification from FiservPersonE2eTest.identifiers[].schemeName to ORCA_Person.identifiers[].schemeName
  // Copy Issuing authority from FiservPersonE2eTest.identifiers[].issuer to ORCA_Person.identifiers[].issuer
  // Copy Date ID was issued from FiservPersonE2eTest.identifiers[].issueDate to ORCA_Person.identifiers[].issueDate
  // Copy Date ID expires from FiservPersonE2eTest.identifiers[].expirationDate to ORCA_Person.identifiers[].expirationDate
  if (source?.identifiers && Array.isArray(source.identifiers)) {
    target.identifiers = source.identifiers.map(identifier => {
      const targetIdentifier = {
        number: identifier.number || "",
        schemeName: identifier.schemeName || ""
      };

      if (identifier.issuer !== undefined) {
        targetIdentifier.issuer = identifier.issuer;
      }

      if (identifier.issueDate !== undefined) {
        targetIdentifier.issueDate = identifier.issueDate;
      }

      if (identifier.expirationDate !== undefined) {
        targetIdentifier.expirationDate = identifier.expirationDate;
      }

      return targetIdentifier;
    });
  }

  // Copy Customer communication preferences from FiservPersonE2eTest.communicationChannels to ORCA_Person.communicationChannels
  // Copy Communication channel name from FiservPersonE2eTest.communicationChannels[].name to ORCA_Person.communicationChannels[].channel
  // Copy Indicates primary contact method from FiservPersonE2eTest.communicationChannels[].primaryContactIndicator to ORCA_Person.communicationChannels[].primaryIndicator
  if (source?.communicationChannels && Array.isArray(source.communicationChannels)) {
    target.communicationChannels = source.communicationChannels.map(channel => {
      const targetChannel = {};

      if (channel.name !== undefined) {
        targetChannel.channel = channel.name;
      }

      if (channel.primaryContactIndicator !== undefined) {
        targetChannel.primaryIndicator = channel.primaryContactIndicator;
      }

      return targetChannel;
    });
  }

  return target;
}