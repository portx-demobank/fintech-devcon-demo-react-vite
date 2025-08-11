
function transformData(sourceSchemas) {
  const fiservData = sourceSchemas?.["FiservPersonE2eTest"];
  if (!fiservData) {
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

  // Copy fullName
  if (fiservData?.name) {
    result.fullName = fiservData.name;
  }

  // Copy lastName
  if (fiservData?.structuredName?.lastName) {
    result.lastName = fiservData.structuredName.lastName;
  }

  // Copy firstName
  if (fiservData?.structuredName?.firstName) {
    result.firstName = fiservData.structuredName.firstName;
  }

  // Copy gender
  if (fiservData?.gender) {
    const genderMap = {
      "1": "Male",
      "2": "Female"
    };
    result.gender = genderMap[fiservData.gender] || fiservData.gender;
  }

  // Copy birthDate from placeAndDateOfBirth
  if (fiservData?.placeAndDateOfBirth?.birthDate) {
    result.birthDate = fiservData.placeAndDateOfBirth.birthDate;
    
    // Copy placeAndDateOfBirth
    if (!result.placeAndDateOfBirth) {
      result.placeAndDateOfBirth = {};
    }
    result.placeAndDateOfBirth.birthDate = fiservData.placeAndDateOfBirth.birthDate;
  }

  // Copy customerType
  if (fiservData?.customerType !== undefined) {
    const customerTypeMap = {
      1: "Personal",
      2: "Business"
    };
    result.customerType = customerTypeMap[fiservData.customerType] || fiservData.customerType.toString();
  }

  // Copy middleName
  if (fiservData?.structuredName?.middleName) {
    result.middleName = fiservData.structuredName.middleName;
  }

  // Copy suffix
  if (fiservData?.structuredName?.suffix) {
    result.suffix = fiservData.structuredName.suffix;
  }

  // Copy taxId
  if (fiservData?.taxInformation?.tin) {
    result.taxId = fiservData.taxInformation.tin;
  }

  // Copy taxStatus
  if (fiservData?.taxInformation?.taxStatus) {
    result.taxStatus = fiservData.taxInformation.taxStatus;
  }

  // Copy jobTitle from comment
  if (fiservData?.contact?.phones?.[0]?.comment) {
    result.jobTitle = fiservData.contact.phones[0].comment;
  }

  // Copy status
  if (fiservData?.audit?.status) {
    result.status = fiservData.audit.status;
  }

  // Copy preferredLanguage
  if (fiservData?.contact?.preferredLanguage) {
    result.preferredLanguage = fiservData.contact.preferredLanguage;
  }

  // Copy identifiers
  if (fiservData?.identifiers && Array.isArray(fiservData.identifiers)) {
    result.identifiers = fiservData.identifiers.map(identifier => {
      const mappedIdentifier = {};
      
      if (identifier.issuer) {
        mappedIdentifier.issuer = identifier.issuer;
      }
      
      if (identifier.number) {
        mappedIdentifier.number = identifier.number;
      }
      
      if (identifier.issueDate) {
        mappedIdentifier.issueDate = identifier.issueDate;
      }
      
      if (identifier.schemeName) {
        mappedIdentifier.schemeName = identifier.schemeName;
      }
      
      if (identifier.expirationDate) {
        mappedIdentifier.expirationDate = identifier.expirationDate;
      }
      
      return mappedIdentifier;
    });
  }

  // Copy emailAddresses
  if (fiservData?.contact?.emails && Array.isArray(fiservData.contact.emails)) {
    result.emailAddresses = fiservData.contact.emails.map(email => {
      const mappedEmail = {
        address: email.emailAddress || ""
      };
      
      if (email.emailPurpose) {
        const emailTypeMap = {
          "Personal": "Personal",
          "Business": "Work"
        };
        mappedEmail.type = emailTypeMap[email.emailPurpose] || "Other";
      }
      
      return mappedEmail;
    });
  }

  // Copy phoneNumbers
  if (fiservData?.contact?.phones && Array.isArray(fiservData.contact.phones)) {
    result.phoneNumbers = fiservData.contact.phones.map(phone => {
      const mappedPhone = {
        number: phone.number || ""
      };
      
      if (phone.phoneType) {
        const phoneTypeMap = {
          "Home": "Home",
          "Mobile": "Mobile",
          "Work": "Work"
        };
        mappedPhone.type = phoneTypeMap[phone.phoneType] || "Other";
      }
      
      return mappedPhone;
    });
  }

  // Copy addresses
  if (fiservData?.contact?.postalAddresses && Array.isArray(fiservData.contact.postalAddresses)) {
    result.addresses = fiservData.contact.postalAddresses.map((address, index) => {
      const mappedAddress = {
        addressId: `A${index + 1001}`,
        line1: "",
        city: "",
        state: "",
        postalCode: ""
      };
      
      if (address.addressLines && Array.isArray(address.addressLines) && address.addressLines.length > 0) {
        mappedAddress.line1 = address.addressLines[0];
        
        if (address.addressLines.length > 1) {
          mappedAddress.line2 = address.addressLines[1];
        }
      }
      
      if (address.country) {
        mappedAddress.country = address.country;
      }
      
      if (address.postCode) {
        mappedAddress.postalCode = address.postCode;
      }
      
      return mappedAddress;
    });
  }

  // Copy communicationChannels
  if (fiservData?.communicationChannels && Array.isArray(fiservData.communicationChannels)) {
    result.communicationChannels = fiservData.communicationChannels.map(channel => {
      const mappedChannel = {};
      
      if (channel.name) {
        mappedChannel.channel = channel.name;
      }
      
      if (channel.primaryContactIndicator !== undefined) {
        mappedChannel.primaryIndicator = channel.primaryContactIndicator;
      }
      
      return mappedChannel;
    });
  }

  // Copy audit information
  if (fiservData?.audit) {
    result.audit = {};
    
    if (fiservData.audit.creationDate) {
      result.audit.creationDate = fiservData.audit.creationDate;
    }
    
    if (fiservData.audit.lastModificationDate) {
      result.audit.lastModificationDate = fiservData.audit.lastModificationDate;
    }
    
    if (fiservData.audit.lastModificationChannel) {
      result.audit.lastModificacionChannel = fiservData.audit.lastModificationChannel;
    }
    
    if (fiservData.audit.status) {
      result.audit.status = fiservData.audit.status;
    }
  }

  return result;
}
