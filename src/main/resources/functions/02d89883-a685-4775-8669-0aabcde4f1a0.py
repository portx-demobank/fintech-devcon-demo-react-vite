
function transformData(sourceSchemas) {
  const fiservData = sourceSchemas["FiservPersonE2eTest"];
  if (!fiservData) {
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

  // Copy customer's full legal name
  if (fiservData?.name) {
    result.fullName = fiservData.name;
  }

  // Copy Customer's family name
  if (fiservData?.structuredName?.lastName) {
    result.lastName = fiservData.structuredName.lastName;
  }

  // Copy customer gender designation
  if (fiservData?.gender) {
    let genderValue = fiservData.gender;
    if (genderValue === "1" || genderValue === "M") {
      result.gender = "Male";
    } else if (genderValue === "2" || genderValue === "F") {
      result.gender = "Female";
    }
  }

  // Copy Customer's given name
  if (fiservData?.structuredName?.firstName) {
    result.firstName = fiservData.structuredName.firstName;
  }

  // Copy Name suffix or generation
  if (fiservData?.structuredName?.suffix) {
    result.suffix = fiservData.structuredName.suffix;
  }

  // Copy Customer's middle name
  if (fiservData?.structuredName?.middleName) {
    result.middleName = fiservData.structuredName.middleName;
  }

  // Copy customer account status
  if (fiservData?.audit?.status) {
    result.status = fiservData.audit.status;
  }

  // Copy Customer date of birth from placeAndDateOfBirth.birthDate to birthDate
  if (fiservData?.placeAndDateOfBirth?.birthDate) {
    result.birthDate = fiservData.placeAndDateOfBirth.birthDate;
  }

  // Copy Customer date of birth from placeAndDateOfBirth.birthDate to placeAndDateOfBirth.birthDate
  if (fiservData?.placeAndDateOfBirth?.birthDate) {
    if (!result.placeAndDateOfBirth) {
      result.placeAndDateOfBirth = {};
    }
    result.placeAndDateOfBirth.birthDate = fiservData.placeAndDateOfBirth.birthDate;
  }

  // Copy Birth information
  if (fiservData?.placeAndDateOfBirth) {
    if (!result.placeAndDateOfBirth) {
      result.placeAndDateOfBirth = {};
    }
    Object.assign(result.placeAndDateOfBirth, fiservData.placeAndDateOfBirth);
  }

  // Copy Customer classification code
  if (fiservData?.customerType) {
    const customerTypeMap = {
      1: "Personal",
      2: "Business"
    };
    result.customerType = customerTypeMap[fiservData.customerType] || String(fiservData.customerType);
  }

  // Copy Customer tax status
  if (fiservData?.taxInformation?.taxStatus) {
    result.taxStatus = fiservData.taxInformation.taxStatus;
  }

  // Copy Tax identification number
  if (fiservData?.taxInformation?.tin) {
    result.taxId = fiservData.taxInformation.tin;
  }

  // Copy Customer's preferred language
  if (fiservData?.contact?.preferredLanguage) {
    result.preferredLanguage = fiservData.contact.preferredLanguage;
  }

  // Copy job title of the person
  if (fiservData?.contact?.phones && Array.isArray(fiservData.contact.phones)) {
    const phone = fiservData.contact.phones[0];
    if (phone?.comment) {
      result.jobTitle = phone.comment;
    }
  }

  // Process Email addresses
  if (fiservData?.contact?.emails && Array.isArray(fiservData.contact.emails)) {
    result.emailAddresses = fiservData.contact.emails.map(email => {
      const resultEmail = { address: "" };
      if (email?.emailAddress) {
        resultEmail.address = email.emailAddress;
      }
      if (email?.emailPurpose) {
        resultEmail.type = email.emailPurpose === "Personal" ? "Personal" : 
                           email.emailPurpose === "Business" ? "Work" : "Other";
      }
      return resultEmail;
    });
  }

  // Process Phone numbers
  if (fiservData?.contact?.phones && Array.isArray(fiservData.contact.phones)) {
    result.phoneNumbers = fiservData.contact.phones.map(phone => {
      const resultPhone = { number: "" };
      if (phone?.number) {
        resultPhone.number = phone.number;
      }
      if (phone?.phoneType) {
        resultPhone.type = phone.phoneType;
      }
      return resultPhone;
    });
  }

  // Process Addresses
  if (fiservData?.contact?.postalAddresses && Array.isArray(fiservData.contact.postalAddresses)) {
    result.addresses = fiservData.contact.postalAddresses.map((address, index) => {
      const resultAddress = {
        addressId: `A${index + 1000}`,
        line1: "",
        city: "",
        state: "",
        postalCode: ""
      };
      
      if (address?.addressLines && Array.isArray(address.addressLines) && address.addressLines.length > 0) {
        resultAddress.line1 = address.addressLines[0];
        if (address.addressLines.length > 1) {
          resultAddress.line2 = address.addressLines[1];
        }
      }
      
      if (address?.country) {
        resultAddress.country = address.country;
      }
      
      if (address?.postCode) {
        resultAddress.postalCode = address.postCode;
      }
      
      return resultAddress;
    });
  }

  // Process Identifiers
  if (fiservData?.identifiers && Array.isArray(fiservData.identifiers)) {
    result.identifiers = fiservData.identifiers.map(identifier => {
      const resultIdentifier = {
        number: "",
        schemeName: ""
      };
      
      if (identifier?.number) {
        resultIdentifier.number = identifier.number;
      }
      
      if (identifier?.schemeName) {
        resultIdentifier.schemeName = identifier.schemeName;
      }
      
      if (identifier?.issuer) {
        resultIdentifier.issuer = identifier.issuer;
      }
      
      if (identifier?.issueDate) {
        resultIdentifier.issueDate = identifier.issueDate;
      }
      
      if (identifier?.expirationDate) {
        resultIdentifier.expirationDate = identifier.expirationDate;
      }
      
      return resultIdentifier;
    });
  }

  // Process Communication Channels
  if (fiservData?.communicationChannels && Array.isArray(fiservData.communicationChannels)) {
    result.communicationChannels = fiservData.communicationChannels.map(channel => {
      const resultChannel = {};
      
      if (channel?.name) {
        resultChannel.channel = channel.name;
      }
      
      if (channel?.primaryContactIndicator !== undefined) {
        resultChannel.primaryIndicator = channel.primaryContactIndicator;
      }
      
      return resultChannel;
    });
  }

  // Copy audit information
  if (!result.audit) {
    result.audit = {};
  }
  
  if (fiservData?.audit?.creationDate) {
    result.audit.creationDate = fiservData.audit.creationDate;
  }
  
  if (fiservData?.audit?.lastModificationDate) {
    result.audit.lastModificationDate = fiservData.audit.lastModificationDate;
  }
  
  if (fiservData?.audit?.lastModificationChannel) {
    result.audit.lastModificacionChannel = fiservData.audit.lastModificationChannel;
  }

  return result;
}
