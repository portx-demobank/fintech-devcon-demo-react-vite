function transformData(sourceSchemas) {
  if (!sourceSchemas || typeof sourceSchemas !== 'object') {
    return {};
  }

  const result = {
    id: '',
    firstName: '',
    lastName: '',
    emailAddresses: [],
    phoneNumbers: [],
    addresses: []
  };

  // Process id field
  if (sourceSchemas["FiservPerson1"]?.audit?.lastModificationDate !== null && 
      sourceSchemas["FiservPerson1"]?.audit?.lastModificationDate !== undefined) {
    result.id = sourceSchemas["FiservPerson1"]?.audit?.lastModificationDate;
  }

  // Ensure we have structured data for the required fields
  if (!result.emailAddresses.length) {
    result.emailAddresses = [{ address: '' }];
  }

  if (!result.phoneNumbers.length) {
    result.phoneNumbers = [{ number: '' }];
  }

  if (!result.addresses.length) {
    result.addresses = [{ 
      addressId: '',
      line1: '',
      city: '',
      state: '',
      postalCode: ''
    }];
  }

  return result;
}