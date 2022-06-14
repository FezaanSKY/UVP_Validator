from Model import Model
from View import View
from Database import Database


class Controller:
    def __init__(self, ):
        self.view = View(self)
        self.database = Database()
        self.validationPassed = False

    def DisplayProvider(self, ):
        return self.database.GetProviderName()

    def start(self, ):
        self.view.start()

    def OnSubmitClicked(self, filelocation, ProviderName):
        model = Model(filelocation)
        self.Untar(model)
        self.authenticate(model)
        if not self.validationPassed:
            return
        self.pars(model)
        self.check_database(model.validationHolder(), ProviderName)


    def Untar(self, model):
        data = model.untarResult
        self.view.UpdateUntar(data)

    def authenticate(self, model):
        (self.validationPassed, data) = model.validate()
        self.view.Update_Authenticate(data)

    def pars(self, model):
        data = model.parse()
        self.view.Update_pars(data)

    def check_database(self,validationHolder,ProviderName ):
        self.view.Update_database_check()
        self.check_Provider(validationHolder.providerID, ProviderName)
        self.check_genre(validationHolder.genre)
        self.check_playlist(validationHolder.dplTemplateID)
        self.check_OfferType(validationHolder.offerType, validationHolder.providerID)


    def check_Provider(self, ProviderID, ProviderName):
        data = self.database.checkProvider(ProviderName, ProviderID)
        self.view.Update_ProviderCheck(data)

    def check_playlist(self,DPLTemplateID):
        data = self.database.check_playlist(DPLTemplateID)
        self.view.Update_PlaylistCheck(data)

    def check_genre(self, fullgenre):
        (genre, subGenre) = fullgenre.split(':')
        data = self.database.check_genre(genre, subGenre)
        self.view.Update_GenreCheck(data)

    def check_OfferType(self, offerType, ProviderID):
        data = self.database.check_offertype(offerType, ProviderID)
        self.view.Update_OfferTypeCheck(data)

    def onclose(self):
        self.database.close()


def Main():
    controller = Controller()
    controller.start()


if __name__ == "__main__":
    Main()
