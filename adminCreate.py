from businessOwnerAcc import register_business_owner as reg
from businessOwnerAcc import register_business
register_business(
    businessName="DemoBusiness",
    zipCode="33328",
    ID="1",
    address="12345 Street, City, FL",
    logoUrl="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSrexI4njqNA0rpA4tQQEGkqCEhH7FfVmw3Vg&s"
)

register_business(
    businessName="Kumart",
    zipCode="90210",
    ID="2",
    address="555 Beverly Hills Blvd, CA",
    logoUrl="https://sdmntprwestus2.oaiusercontent.com/files/00000000-a270-61f8-9f03-2ce8394800a2/raw?se=2025-04-30T23%3A57%3A06Z&sp=r&sv=2024-08-04&sr=b&scid=02c36dd1-b921-5ef1-b78c-159565496a63&skoid=b53ae837-f585-4db7-b46f-2d0322fce5a9&sktid=a48cca56-e6da-484e-a814-9c849652bcb3&skt=2025-04-30T04%3A47%3A48Z&ske=2025-05-01T04%3A47%3A48Z&sks=b&skv=2024-08-04&sig=NgLnv6w21GSjosNYc9lncX4IMyW%2BzrdHzGud5x9Dq1w%3D"
)

reg("johnadams","MyPassword!","John Adams","1999-99-99","1")
reg("akumar","MyPassword!","Final Boss of Computer Science, Ajoy Kumar","1999-99-99","2")

#print(businessInfoCollection.find_one({"businessID": businessID},{"businessName":1,"_id":0})["businessName"])