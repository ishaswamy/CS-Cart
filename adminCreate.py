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
    logoUrl="https://upload.wikimedia.org/wikipedia/commons/thumb/4/47/PNG_transparency_demonstration_1.png/640px-PNG_transparency_demonstration_1.png"
)

reg("johnadams","MyPassword!","John Adams","1999-99-99","1")
reg("akumar","MyPassword!","Final Boss of Computer Science, Ajoy Kumar","1999-99-99","2")

#print(businessInfoCollection.find_one({"businessID": businessID},{"businessName":1,"_id":0})["businessName"])