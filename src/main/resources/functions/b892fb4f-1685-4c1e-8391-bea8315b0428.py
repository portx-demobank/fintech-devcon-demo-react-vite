
function transformData(sourceSchemas) {
  const fiservData = sourceSchemas["FiservPerson1"];
  const result = {
    id: null,
    firstName: null,
    lastName: null,
    emailAddresses: [],
    phoneNumbers: [],
    addresses: []
  };
  
  // RULE: Copy unique identifier for the person from FiservPerson1.audit.lastModificationDate to TargetSchema.id
  if (fiservData?.audit?.lastModificationDate !== undefined) {
    result.id = fiservData.audit.lastModificationDate;
  }
  
  // Extract other required fields from structured name
  if (fiservData?.structuredName?.firstName !== undefined) {
    result.firstName = fiservData.structuredName.firstName;
  }
  
  if (fiservData?.structuredName?.lastName !== undefined) {
    result.lastName = fiservData.structuredName.lastName;
  }
  
  // Set up empty arrays for required fields even if source doesn't have data
  if (fiservData?.emails && Array.isArray(fiservData.emails)) {
    result.emailAddresses = fiservData.emails.map(email => {
      return {
        address: email?.emailAddress || '',
        type: email?.emailPurpose === 'Personal' ? 'Personal' : 
              email?.emailPurpose === 'Business' ? 'Work' : 'Other'
      };
    });
  }
  
  if (fiservData?.phones && Array.isArray(fiservData.phones)) {
    result.phoneNumbers = fiservData.phones.map(phone => {
      return {
        number: phone?.number || '',
        type: phone?.phoneType === 'Home' ? 'Home' : 
              phone?.phoneType === 'Work' ? 'Work' : 
              phone?.phoneType === 'Mobile' ? 'Mobile' : 'Other'
      };
    });
  }
  
  if (fiservData?.postalAddresses && Array.isArray(fiservData.postalAddresses)) {
    result.addresses = fiservData.postalAddresses.map((address, index) => {
      const addressObj = {
        addressId: `A${1000 + index}`,
        line1: Array.isArray(address?.addressLines) && address.addressLines.length > 0 ? 
              address.addressLines[0] : '',
        line2: Array.isArray(address?.addressLines) && address.addressLines.length > 1 ? 
              address.addressLines[1] : '',
        city: '',
        state: '',
        postalCode: address?.postCode || ''
      };
      return addressObj;
    });
  }
  
  // Ensure we have at least one entry in each required array field
  if (result.emailAddresses.length === 0) {
    result.emailAddresses.push({ address: '' });
  }
  
  if (result.phoneNumbers.length === 0) {
    result.phoneNumbers.push({ number: '' });
  }
  
  if (result.addresses.length === 0) {
    result.addresses.push({
      addressId: 'A1001',
      line1: '',
      city: '',
      state: '',
      postalCode: ''
    });
  }
  
  return result;
}
