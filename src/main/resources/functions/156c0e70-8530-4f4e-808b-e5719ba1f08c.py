
function transformData(sourceSchemas) {
  const result = {
    id: "",
    firstName: "",
    lastName: "",
    emailAddresses: [],
    phoneNumbers: [],
    addresses: []
  };

  const source = sourceSchemas?.["FiservPersonE2eTest"];
  if (!source) return result;

  // Copy job title of the person
  if (source?.contact?.phones && Array.isArray(source.contact.phones)) {
    const phone = source.contact.phones[0];
    if (phone?.comment) {
      result.jobTitle = phone.comment;
    }
  }

  // Copy Current record status
  if (source?.audit?.status) {
    if (!result.audit) result.audit = {};
    result.audit.status = source.audit.status;
  }

  // Copy Service member classification
  if (source?.serviceMember?.insiderType !== undefined) {
    result.militaryMemberIndicator = !!source.serviceMember.insiderType;
  }

  // Copy identifiers
  if (source?.identifiers && Array.isArray(source.identifiers) && source.identifiers.length > 0) {
    result.identifiers = source.identifiers.map(identifier => {
      const targetIdentifier = {
        number: identifier.number || "",
        schemeName: identifier.schemeName || ""
      };
      
      if (identifier.issuer) {
        targetIdentifier.issuer = identifier.issuer;
      }
      
      if (identifier.issueDate) {
        targetIdentifier.issueDate = identifier.issueDate;
      }
      
      if (identifier.expirationDate) {
        targetIdentifier.expirationDate = identifier.expirationDate;
      }
      
      return targetIdentifier;
    });
  }

  // Copy communication channels
  if (source?.communicationChannels && Array.isArray(source.communicationChannels)) {
    result.communicationChannels = source.communicationChannels.map(channel => {
      const targetChannel = {};
      
      if (channel?.name) {
        targetChannel.channel = channel.name;
      }
      
      if (channel?.primaryContactIndicator !== undefined) {
        targetChannel.primaryIndicator = channel.primaryContactIndicator;
      }
      
      return targetChannel;
    });
  }

  // Copy Name suffix or generation
  if (source?.structuredName?.suffix) {
    result.suffix = source.structuredName.suffix;
  }

  // Copy Customer's date of birth for placeAndDateOfBirth
  if (source?.placeAndDateOfBirth?.birthDate) {
    if (!result.placeAndDateOfBirth) result.placeAndDateOfBirth = {};
    result.placeAndDateOfBirth.birthDate = source.placeAndDateOfBirth.birthDate;
  }

  // Copy Type of phone device and number
  if (source?.contact?.phones && Array.isArray(source.contact.phones)) {
    result.phoneNumbers = source.contact.phones.map(phone => {
      const targetPhone = {
        number: phone.number || ""
      };
      
      if (phone?.phoneType) {
        targetPhone.type = phone.phoneType;
      }
      
      return targetPhone;
    });
  }

  // Copy Customer's first name
  if (source?.structuredName?.firstName) {
    result.firstName = source.structuredName.firstName;
  }

  // Copy Email address
  if (source?.contact?.emails && Array.isArray(source.contact.emails)) {
    result.emailAddresses = source.contact.emails.map(email => {
      return {
        address: email.emailAddress || ""
      };
    });
  }

  // Copy Customer's full name
  if (source?.name) {
    result.fullName = source.name;
  }

  // Copy Address information
  if (source?.contact?.postalAddresses && Array.isArray(source.contact.postalAddresses)) {
    result.addresses = source.contact.postalAddresses.map((address, index) => {
      const targetAddress = {
        addressId: `A${1000 + index}`,
        line1: "",
        city: "",
        state: "",
        postalCode: ""
      };
      
      if (address?.addressLines && Array.isArray(address.addressLines)) {
        if (address.addressLines[0]) {
          targetAddress.line1 = address.addressLines[0];
        }
        
        if (address.addressLines[1]) {
          targetAddress.line2 = address.addressLines[1];
        }
      }
      
      if (address?.postCode) {
        targetAddress.postalCode = address.postCode;
      }
      
      if (address?.country) {
        targetAddress.country = address.country;
      }
      
      return targetAddress;
    });
  }

  // Copy Customer's last name
  if (source?.structuredName?.lastName) {
    result.lastName = source.structuredName.lastName;
  }

  // Copy Customer's gender designation
  if (source?.gender) {
    if (source.gender === "1" || source.gender === "M") {
      result.gender = "Male";
    } else if (source.gender === "2" || source.gender === "F") {
      result.gender = "Female";
    }
  }

  // Copy Customer's tax status
  if (source?.taxInformation?.taxStatus) {
    result.taxStatus = source.taxInformation.taxStatus;
  }

  // Copy Date record was created
  if (source?.audit?.creationDate) {
    if (!result.audit) result.audit = {};
    result.audit.creationDate = source.audit.creationDate;
  }

  // Copy Tax identification number
  if (source?.taxInformation?.tin) {
    result.taxId = source.taxInformation.tin;
  }

  // Copy Date of last record update
  if (source?.audit?.lastModificationDate) {
    if (!result.audit) result.audit = {};
    result.audit.lastModificationDate = source.audit.lastModificationDate;
  }

  // Copy Channel used for last update
  if (source?.audit?.lastModificationChannel) {
    if (!result.audit) result.audit = {};
    result.audit.lastModificacionChannel = source.audit.lastModificationChannel;
  }

  // Copy Customer's middle name
  if (source?.structuredName?.middleName) {
    result.middleName = source.structuredName.middleName;
  }

  // Copy Customer's preferred language code
  if (source?.contact?.preferredLanguage) {
    result.preferredLanguage = source.contact.preferredLanguage;
  }

  // Copy Type classification for customer
  if (source?.customerType !== undefined) {
    if (source.customerType === 1) {
      result.customerType = "Personal";
    } else if (source.customerType === 2) {
      result.customerType = "Business";
    }
  }

  // Copy Customer's date of birth for root birthDate
  if (source?.placeAndDateOfBirth?.birthDate) {
    result.birthDate = source.placeAndDateOfBirth.birthDate;
  }

  // Copy OFAC reporting required
  if (source?.profile?.ofacReportingIndicator !== undefined) {
    result.taxReportingIndicator = source.profile.ofacReportingIndicator;
  }

  return result;
}
