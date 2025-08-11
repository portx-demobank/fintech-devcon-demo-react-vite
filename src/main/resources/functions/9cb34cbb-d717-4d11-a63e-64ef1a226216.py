function transformData(sourceSchemas) {
  if (!sourceSchemas || typeof sourceSchemas !== 'object') {
    return null;
  }

  const fiservPerson = sourceSchemas["FiservPersonE2eTest"];
  if (!fiservPerson) {
    return null;
  }

  const result = {
    id: "",
    firstName: "",
    lastName: "",
    emailAddresses: [],
    phoneNumbers: [],
    addresses: []
  };

  // Copy customer's first name
  if (fiservPerson?.structuredName?.firstName) {
    result.firstName = fiservPerson.structuredName.firstName;
  }

  // Copy customer's last name
  if (fiservPerson?.structuredName?.lastName) {
    result.lastName = fiservPerson.structuredName.lastName;
  }

  // Copy name suffix
  if (fiservPerson?.structuredName?.suffix) {
    result.suffix = fiservPerson.structuredName.suffix;
  }

  // Copy customer's middle name
  if (fiservPerson?.structuredName?.middleName) {
    result.middleName = fiservPerson.structuredName.middleName;
  }

  // Copy customer's full legal name
  if (fiservPerson?.name) {
    result.fullName = fiservPerson.name;
  }

  // Copy customer's gender designation
  if (fiservPerson?.gender) {
    const genderMap = {
      "1": "Male",
      "2": "Female",
      "M": "Male",
      "F": "Female"
    };
    result.gender = genderMap[fiservPerson.gender] || fiservPerson.gender;
  }

  // Copy customer's date of birth
  if (fiservPerson?.placeAndDateOfBirth?.birthDate) {
    result.birthDate = fiservPerson.placeAndDateOfBirth.birthDate;
  }

  // Copy tax identification number
  if (fiservPerson?.taxInformation?.tin) {
    result.taxId = fiservPerson.taxInformation.tin;
  }

  // Copy customer's tax filing status
  if (fiservPerson?.taxInformation?.taxStatus) {
    result.taxStatus = fiservPerson.taxInformation.taxStatus;
  }

  // Copy customer classification category
  if (fiservPerson?.customerType) {
    const typeMap = {
      1: "Personal",
      2: "Business"
    };
    result.customerType = typeMap[fiservPerson.customerType] || String(fiservPerson.customerType);
  }

  // Copy customer's preferred language
  if (fiservPerson?.contact?.preferredLanguage) {
    result.preferredLanguage = fiservPerson.contact.preferredLanguage;
  }

  // Copy job title
  if (fiservPerson?.jobTitle) {
    result.jobTitle = fiservPerson.jobTitle;
  }

  // Copy audit information
  if (fiservPerson?.audit) {
    result.audit = {};
    
    // Copy current record status
    if (fiservPerson.audit.status) {
      result.audit.status = fiservPerson.audit.status;
    }
    
    // Copy timestamp of record creation
    if (fiservPerson.audit.creationDate) {
      result.audit.creationDate = fiservPerson.audit.creationDate;
    }
    
    // Copy timestamp of last modification
    if (fiservPerson.audit.lastModificationDate) {
      result.audit.lastModificationDate = fiservPerson.audit.lastModificationDate;
    }
    
    // Copy channel used for last update
    if (fiservPerson.audit.lastModificationChannel) {
      result.audit.lastModificacionChannel = fiservPerson.audit.lastModificationChannel;
    }
  }

  // Copy email addresses
  if (Array.isArray(fiservPerson?.contact?.emails)) {
    result.emailAddresses = fiservPerson.contact.emails.map(email => {
      const emailObj = { address: "" };
      
      if (email?.emailAddress) {
        emailObj.address = email.emailAddress;
      }
      
      if (email?.emailPurpose) {
        emailObj.type = email.emailPurpose;
      }
      
      return emailObj;
    }).filter(email => email.address);
  }

  // Copy phone numbers
  if (Array.isArray(fiservPerson?.contact?.phones)) {
    result.phoneNumbers = fiservPerson.contact.phones.map(phone => {
      const phoneObj = { number: "" };
      
      if (phone?.number) {
        phoneObj.number = phone.number;
      }
      
      if (phone?.phoneType) {
        phoneObj.type = phone.phoneType;
      }
      
      return phoneObj;
    }).filter(phone => phone.number);
  }

  // Copy postal addresses
  if (Array.isArray(fiservPerson?.contact?.postalAddresses)) {
    result.addresses = fiservPerson.contact.postalAddresses.map((address, index) => {
      const addressObj = {
        addressId: `A${index + 1000}`,
        line1: "",
        city: "",
        state: "",
        postalCode: ""
      };
      
      if (Array.isArray(address?.addressLines) && address.addressLines[0]) {
        addressObj.line1 = address.addressLines[0];
      }
      
      if (Array.isArray(address?.addressLines) && address.addressLines[1]) {
        addressObj.line2 = address.addressLines[1];
      }
      
      if (address?.postCode) {
        addressObj.postalCode = address.postCode;
      }
      
      if (address?.country) {
        addressObj.country = address.country;
      }
      
      return addressObj;
    });
  }

  // Copy identification documents
  if (Array.isArray(fiservPerson?.identifiers)) {
    result.identifiers = fiservPerson.identifiers.map(id => {
      const idObj = {
        number: "",
        schemeName: ""
      };
      
      if (id?.number) {
        idObj.number = id.number;
      }
      
      if (id?.schemeName) {
        idObj.schemeName = id.schemeName;
      }
      
      if (id?.issuer) {
        idObj.issuer = id.issuer;
      }
      
      if (id?.issueDate) {
        idObj.issueDate = id.issueDate;
      }
      
      if (id?.expirationDate) {
        idObj.expirationDate = id.expirationDate;
      }
      
      return idObj;
    });
  }

  // Copy communication channels
  if (Array.isArray(fiservPerson?.communicationChannels)) {
    result.communicationChannels = fiservPerson.communicationChannels.map(channel => {
      const channelObj = {};
      
      if (channel?.name) {
        channelObj.channel = channel.name;
      }
      
      if (channel?.primaryContactIndicator !== undefined) {
        channelObj.primaryIndicator = channel.primaryContactIndicator;
      }
      
      return channelObj;
    });
  }

  // Copy customer's birth date to placeAndDateOfBirth
  if (fiservPerson?.placeAndDateOfBirth?.birthDate) {
    result.placeAndDateOfBirth = {
      birthDate: fiservPerson.placeAndDateOfBirth.birthDate
    };
  }

  return result;
}