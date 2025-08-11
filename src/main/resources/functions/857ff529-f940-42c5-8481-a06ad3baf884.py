
function transformData(sourceSchemas) {
  const source = sourceSchemas?.["FiservPersonE2eTest"];
  if (!source) {
    return {};
  }

  const target = {
    emailAddresses: [],
    phoneNumbers: [],
    addresses: [],
    identifiers: [],
    communicationChannels: []
  };

  // Copy customer's full name from FiservPersonE2eTest.name to ORCA Person.fullName
  if (source?.name !== undefined) {
    target.fullName = source.name;
  }

  // Copy customer's given name from FiservPersonE2eTest.structuredName.firstName to ORCA Person.firstName
  if (source?.structuredName?.firstName !== undefined) {
    target.firstName = source.structuredName.firstName;
  }

  // Copy customer's family name from FiservPersonE2eTest.structuredName.lastName to ORCA Person.lastName
  if (source?.structuredName?.lastName !== undefined) {
    target.lastName = source.structuredName.lastName;
  }

  // Copy customer's middle name from FiservPersonE2eTest.structuredName.middleName to ORCA Person.middleName
  if (source?.structuredName?.middleName !== undefined) {
    target.middleName = source.structuredName.middleName;
  }

  // Copy name suffix or generation from FiservPersonE2eTest.structuredName.suffix to ORCA Person.suffix
  if (source?.structuredName?.suffix !== undefined) {
    target.suffix = source.structuredName.suffix;
  }

  // Copy customer gender code from FiservPersonE2eTest.gender to ORCA Person.gender
  if (source?.gender !== undefined) {
    target.gender = source.gender;
  }

  // Copy date of birth from FiservPersonE2eTest.placeAndDateOfBirth.birthDate to ORCA Person.birthDate
  if (source?.placeAndDateOfBirth?.birthDate !== undefined) {
    target.birthDate = source.placeAndDateOfBirth.birthDate;
  }

  // Copy birth information from FiservPersonE2eTest.placeAndDateOfBirth to ORCA Person.placeAndDateOfBirth
  if (source?.placeAndDateOfBirth) {
    target.placeAndDateOfBirth = {};
    if (source.placeAndDateOfBirth.birthDate !== undefined) {
      target.placeAndDateOfBirth.birthDate = source.placeAndDateOfBirth.birthDate;
    }
  }

  // Copy tax identification number from FiservPersonE2eTest.taxInformation.tin to ORCA Person.taxId
  if (source?.taxInformation?.tin !== undefined) {
    target.taxId = source.taxInformation.tin;
  }

  // Copy customer tax status classification from FiservPersonE2eTest.taxInformation.taxStatus to ORCA Person.taxStatus
  if (source?.taxInformation?.taxStatus !== undefined) {
    target.taxStatus = source.taxInformation.taxStatus;
  }

  // Copy customer classification code from FiservPersonE2eTest.customerType to ORCA Person.customerType
  if (source?.customerType !== undefined) {
    target.customerType = source.customerType.toString();
  }

  // Copy customer's language preference from FiservPersonE2eTest.contact.preferredLanguage to ORCA Person.preferredLanguage
  if (source?.contact?.preferredLanguage !== undefined) {
    target.preferredLanguage = source.contact.preferredLanguage;
  }

  // Copy job title of the person from FiservPersonE2eTest.contact.phones.comment to TargetSchema.jobTitle
  if (source?.contact?.phones?.[0]?.comment !== undefined) {
    target.jobTitle = source.contact.phones[0].comment;
  }

  // Copy customer email addresses from FiservPersonE2eTest.contact.emails[].emailAddress to ORCA Person.emailAddresses[].address
  if (Array.isArray(source?.contact?.emails)) {
    source.contact.emails.forEach(email => {
      if (email?.emailAddress !== undefined) {
        const targetEmail = { address: email.emailAddress };
        
        // Copy purpose of email address from FiservPersonE2eTest.contact.emails[].emailPurpose to ORCA Person.emailAddresses[].type
        if (email?.emailPurpose !== undefined) {
          targetEmail.type = email.emailPurpose;
        }
        
        target.emailAddresses.push(targetEmail);
      }
    });
  }

  // Copy phone number from FiservPersonE2eTest.contact.phones[].number to ORCA Person.phoneNumbers[].number
  if (Array.isArray(source?.contact?.phones)) {
    source.contact.phones.forEach(phone => {
      if (phone?.number !== undefined) {
        const targetPhone = { number: phone.number };
        
        // Copy type of phone from FiservPersonE2eTest.contact.phones[].phoneType to ORCA Person.phoneNumbers[].type
        if (phone?.phoneType !== undefined) {
          targetPhone.type = phone.phoneType;
        }
        
        target.phoneNumbers.push(targetPhone);
      }
    });
  }

  // Copy address lines and process postal addresses
  if (Array.isArray(source?.contact?.postalAddresses)) {
    source.contact.postalAddresses.forEach((address, index) => {
      const targetAddress = { addressId: `A${index + 1000}` };
      
      // Copy address line components
      if (Array.isArray(address?.addressLines) && address.addressLines.length > 0) {
        targetAddress.line1 = address.addressLines[0];
        if (address.addressLines.length > 1) {
          targetAddress.line2 = address.addressLines[1];
        }
      }
      
      // Copy postal or ZIP code
      if (address?.postCode !== undefined) {
        targetAddress.postalCode = address.postCode;
      }
      
      // Copy country code
      if (address?.country !== undefined) {
        targetAddress.country = address.country;
      }
      
      // Default required fields to ensure validity
      targetAddress.city = targetAddress.city || "";
      targetAddress.state = targetAddress.state || "";
      
      target.addresses.push(targetAddress);
    });
  }

  // Copy customer identification documents from FiservPersonE2eTest.identifiers to ORCA Person.identifiers
  if (Array.isArray(source?.identifiers)) {
    source.identifiers.forEach(identifier => {
      const targetIdentifier = {};
      
      // Copy identification number
      if (identifier?.number !== undefined) {
        targetIdentifier.number = identifier.number;
      }
      
      // Copy type of identification document
      if (identifier?.schemeName !== undefined) {
        targetIdentifier.schemeName = identifier.schemeName;
      }
      
      // Copy issuing authority
      if (identifier?.issuer !== undefined) {
        targetIdentifier.issuer = identifier.issuer;
      }
      
      // Copy date document was issued
      if (identifier?.issueDate !== undefined) {
        targetIdentifier.issueDate = identifier.issueDate;
      }
      
      // Copy date document expires
      if (identifier?.expirationDate !== undefined) {
        targetIdentifier.expirationDate = identifier.expirationDate;
      }
      
      // Only add if required fields are present
      if (targetIdentifier.number !== undefined && targetIdentifier.schemeName !== undefined) {
        target.identifiers.push(targetIdentifier);
      }
    });
  }

  // Copy customer communication preferences from FiservPersonE2eTest.communicationChannels to ORCA Person.communicationChannels
  if (Array.isArray(source?.communicationChannels)) {
    source.communicationChannels.forEach(channel => {
      const targetChannel = {};
      
      // Copy communication channel name
      if (channel?.name !== undefined) {
        targetChannel.channel = channel.name;
      }
      
      // Copy primary contact method indicator
      if (channel?.primaryContactIndicator !== undefined) {
        targetChannel.primaryIndicator = channel.primaryContactIndicator;
      }
      
      target.communicationChannels.push(targetChannel);
    });
  }

  // Copy audit information
  if (source?.audit) {
    target.audit = {};
    
    // Copy record status
    if (source.audit.status !== undefined) {
      target.audit.status = source.audit.status;
    }
    
    // Copy record creation timestamp
    if (source.audit.creationDate !== undefined) {
      target.audit.creationDate = source.audit.creationDate;
    }
    
    // Copy last record modification timestamp
    if (source.audit.lastModificationDate !== undefined) {
      target.audit.lastModificationDate = source.audit.lastModificationDate;
    }
    
    // Copy channel used for modification
    if (source.audit.lastModificationChannel !== undefined) {
      target.audit.lastModificacionChannel = source.audit.lastModificationChannel;
    }
  }

  // Generate ID if missing
  target.id = target.id || "P12345";

  return target;
}
