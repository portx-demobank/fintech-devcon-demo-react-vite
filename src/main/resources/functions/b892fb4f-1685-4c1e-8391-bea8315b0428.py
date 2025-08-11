
function transformData(sourceSchemas) {
  const target = {
    id: "",
    firstName: "",
    lastName: "",
    emailAddresses: [],
    phoneNumbers: [],
    addresses: []
  };

  // Copy unique identifier for the person
  if (sourceSchemas["FiservPerson1"]?.audit?.lastModificationDate !== undefined) {
    target.id = sourceSchemas["FiservPerson1"]?.audit?.lastModificationDate;
  }

  return target;
}
