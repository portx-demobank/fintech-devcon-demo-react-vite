
function transformData(sourceSchemas) {
  const fiserv = sourceSchemas["FiservPersonE2eTest"];
  if (!fiserv) {
    return {};
  }

  const result = {
    id: "",
    firstName: "",
    lastName: "",
    emailAddresses: [],
    phoneNumbers: [],
    addresses: []
  };

  // Copy customer's full legal name from FiservPersonE2eTest.name to ORCA_Person.fullName
  if (fiserv?.name) {
    result.fullName = fiserv.name;
  }

  // Copy Customer's family name from FiservPersonE2eTest.structuredName.lastName to ORCA_Person.lastName
  if (fiserv?.structuredName?.lastName) {
    result.lastName = fiserv.structuredName.lastName;
  }

  // Copy customer gender designation from FiservPersonE2eTest.gender to ORCA_Person.gender
  if (fiserv?.gender) {
    result.gender = fiserv.gender === "1" ? "Male" : (fiserv.gender === "2" ? "Female" : fiserv.gender);
  }

  // Copy Customer's given name from FiservPersonE2eTest.structuredName.firstName to ORCA_Person.firstName
  if (fiserv?.structuredName?.firstName) {
    result.firstName = fiserv.structuredName.firstName;
  }

  // Copy Customer's middle name from FiservPersonE2eTest.structuredName.middleName to ORCA_Person.middleName
  if (fiserv?.structuredName?.middleName) {
    result.middleName = fiserv.structuredName.middleName;
  }

  // Copy Name suffix or generation from FiservPersonE2eTest.structuredName.suffix to ORCA_Person.suffix
  if (fiserv?.structuredName?.suffix) {
    result.suffix = fiserv.structuredName.suffix;
  }

  // Copy Tax identification number from FiservPersonE2eTest.taxInformation.tin to ORCA_Person.taxId
  if (fiserv?.taxInformation?.tin) {
    result.taxId = fiserv.taxInformation.tin;
  }

  // Copy Customer tax status from FiservPersonE2eTest.taxInformation.taxStatus to ORCA_Person.taxStatus
  if (fiserv?.taxInformation?.taxStatus) {
    result.taxStatus = fiserv.taxInformation.taxStatus;
  }

  // Copy customer account status from FiservPersonE2eTest.audit.status to ORCA_Person.status
  if (fiserv?.audit?.status) {
    result.status = fiserv.audit.status;
  }

  // Copy Customer date of birth from FiservPersonE2eTest.placeAndDateOfBirth.birthDate to ORCA_Person.birthDate
  if (fiserv?.placeAndDateOfBirth?.birthDate) {
    result.birthDate = fiserv.placeAndDateOfBirth.birthDate;
  }

  // Copy Customer date of birth from FiservPersonE2eTest.placeAndDateOfBirth.birthDate to ORCA_Person.placeAndDateOfBirth.birthDate
  if (fiserv?.placeAndDateOfBirth?.birthDate) {
    if (!result.placeAndDateOfBirth) {
      result.placeAndDateOfBirth = {};
    }
    result.placeAndDateOfBirth.birthDate = fiserv.placeAndDateOfBirth.birthDate;
  }

  // Copy Birth information from FiservPersonE2eTest.placeAndDateOfBirth to ORCA_Person.placeAndDateOfBirth
  if (fiserv?.placeAndDateOfBirth) {
    if (!result.placeAndDateOfBirth) {
      result.placeAndDateOfBirth = {};
    }
    // Only copy fields that exist in the source
    Object.keys(fiserv.placeAndDateOfBirth).forEach(key => {
      if (fiserv.placeAndDateOfBirth[key] !== undefined) {
        result.placeAndDateOfBirth[key] = fiserv.placeAndDateOfBirth[key];
      }
    });
  }

  // Copy Customer classification code from FiservPersonE2eTest.customerType to ORCA_Person.customerType
  if (fiserv?.customerType !== undefined) {
    // Map numeric customerType to string values
    const typeMap = {
      1: "Personal",
      2: "Business"
    };
    result.customerType = typeMap[fiserv.customerType] || String(fiserv.customerType);
  }

  // Copy Customer's preferred language from FiservPersonE2eTest.contact.preferredLanguage to ORCA_Person.preferredLanguage
  if (fiserv?.contact?.preferredLanguage) {
    result.preferredLanguage = fiserv.contact.preferredLanguage;
  }

  // Copy job title of the person from FiservPersonE2eTest.contact.phones.comment to TargetSchema.jobTitle
  if (fiserv?.contact?.phones?.[0]?.comment) {
    result.jobTitle = fiserv.contact.phones[0].comment;
  }

  // Copy Email address from FiservPersonE2eTest.contact.emails[].emailAddress to ORCA_Person.emailAddresses[].address
  if (fiserv?.contact?.emails && Array.isArray(fiserv.contact.emails)) {
    result.emailAddresses = fiserv.contact.emails
      .filter(email => email?.emailAddress)
      .map(email => ({
        address: email.emailAddress,
        type: email.emailPurpose === "Personal" ? "Personal" : 
              (email.emailPurpose === "Business" ? "Work" : "Other")
      }));
  }

  // Copy Phone number from FiservPersonE2eTest.contact.phones[].number to ORCA_Person.phoneNumbers[].number
  if (fiserv?.contact?.phones && Array.isArray(fiserv.contact.phones)) {
    result.phoneNumbers = fiserv.contact.phones
      .filter(phone => phone?.number)
      .map(phone => ({
        number: phone.number,
        type: phone.phoneType || "Other"
      }));
  }

  // Copy Customer identification documents from FiservPersonE2eTest.identifiers to ORCA_Person.identifiers
  if (fiserv?.identifiers && Array.isArray(fiserv.identifiers)) {
    result.identifiers = fiserv.identifiers.map(id => {
      const newId = {};
      
      // Copy ID document number
      if (id?.number) {
        newId.number = id.number;
      }
      
      // Copy Type of identification
      if (id?.schemeName) {
        newId.schemeName = id.schemeName;
      }
      
      // Copy Issuing authority
      if (id?.issuer) {
        newId.issuer = id.issuer;
      }
      
      // Copy Date ID was issued
      if (id?.issueDate) {
        newId.issueDate = id.issueDate;
      }
      
      // Copy Date ID expires
      if (id?.expirationDate) {
        newId.expirationDate = id.expirationDate;
      }
      
      return newId;
    });
  }

  // Copy Street address lines and postal address data
  if (fiserv?.contact?.postalAddresses && Array.isArray(fiserv.contact.postalAddresses)) {
    result.addresses = fiserv.contact.postalAddresses.map((addr, index) => {
      const newAddr = {
        addressId: `A${1000 + index}`,
        line1: "",
        city: "",
        state: "",
        postalCode: ""
      };
      
      // Copy Street address lines
      if (addr?.addressLines && Array.isArray(addr.addressLines) && addr.addressLines.length > 0) {
        newAddr.line1 = addr.addressLines[0] || "";
        if (addr.addressLines.length > 1) {
          newAddr.line2 = addr.addressLines[1] || "";
        }
      }
      
      // Copy Postal or ZIP code
      if (addr?.postCode) {
        newAddr.postalCode = addr.postCode;
      }
      
      // Copy Country code
      if (addr?.country) {
        newAddr.country = addr.country;
      }
      
      return newAddr;
    });
  }

  // Copy Customer communication preferences
  if (fiserv?.communicationChannels && Array.isArray(fiserv.communicationChannels)) {
    result.communicationChannels = fiserv.communicationChannels.map(channel => {
      const newChannel = {};
      
      // Copy Communication channel name
      if (channel?.name) {
        newChannel.channel = channel.name;
      }
      
      // Copy Indicates primary contact method
      if (channel?.primaryContactIndicator !== undefined) {
        newChannel.primaryIndicator = channel.primaryContactIndicator;
      }
      
      return newChannel;
    });
  }

  // Copy audit information
  if (fiserv?.audit) {
    result.audit = {};
    
    // Copy record creation timestamp
    if (fiserv.audit.creationDate) {
      result.audit.creationDate = fiserv.audit.creationDate;
    }
    
    // Copy last updated timestamp
    if (fiserv.audit.lastModificationDate) {
      result.audit.lastModificationDate = fiserv.audit.lastModificationDate;
    }
    
    // Copy last modification method
    if (fiserv.audit.lastModificationChannel) {
      result.audit.lastModificacionChannel = fiserv.audit.lastModificationChannel;
    }
    
    // Copy customer account status
    if (fiserv.audit.status) {
      result.audit.status = fiserv.audit.status;
    }
  }

  return result;
}
