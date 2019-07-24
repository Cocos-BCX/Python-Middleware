def getExtensionObjectFromString(strExtension):
        try:
            assetID,tempData=strExtension.split("$")
            itemVER, tempData=tempData.split("@")
            itemID,tempData=tempData.split(";")
            return extensions(assetID,itemVER,itemID,tempData)
        except: return None

class extensions:
    def __init__(self, assetID, itemVER, itemID, data):
        if assetID and itemVER and itemID:
            self.assetID = assetID
            self.itemVER = itemVER
            self.itemID=itemID
            self.data= "%s$%s@%s;%s" % (self.assetID,self.itemVER,self.itemID, data)

    def string(self):
        return self.data

    def compareWithId(self,itemid):
        try:
            if(self.itemID==itemid):
                return True
            else:
                return False
        except:
            return False
    def compareWithVER(self,ver):
        try:
            if(self.itemVER==ver):
                return True
        except:
            return False
    







