import sqlite3

class Database:
    def __init__(self,):
        self.db = sqlite3.connect('DB/uvp_validator_rules.db')
        self.cursor = self.db.cursor()
    def GetProviderName(self,):  # Execute query

        sql = 'SELECT DISTINCT ProviderName FROM PROVIDER_BASE'
        self.cursor.execute(sql)
        list_tested = self.cursor.fetchall()  # Get query response and store in variable
        list_tested = [i for sub in list_tested for i in sub]  # Convert to list from tuple

        return list_tested

    def checkProvider(self,ProviderName,ProviderID):
        sql = 'SELECT COUNT(PK_ID) FROM PROVIDER_BASE WHERE ProviderID =(?) AND ProviderName =(?)'
        self.cursor.execute(sql, (ProviderID, ProviderName))
        list_tested = self.cursor.fetchone()  # Get query response and store in variable

        return list_tested[0]

    def check_playlist(self, DPLTemplateID):
        sql = 'SELECT COUNT(DPLTemplateID) FROM PROVIDER_DPL_TEMPLATES WHERE DPLTemplateID =(?)'
        self.cursor.execute(sql,(DPLTemplateID, ) )
        list_tested = self.cursor.fetchone()  # Get query response and store in variable

        return list_tested[0]

    def check_genre(self, genre, subGenre):
        sql = 'SELECT COUNT(GenreName) FROM GENRES WHERE Genre =(?) AND Subgenre =(?)'
        self.cursor.execute(sql,(genre, subGenre) )
        list_tested = self.cursor.fetchone()  # Get query response and store in variable

        return list_tested[0]

    def check_offertype(self, offerType, ProviderID):
        sql = 'SELECT COUNT(PK_ID) FROM PROVIDER_BASE WHERE OfferType =(?) AND ProviderID =(?) '
        self.cursor.execute(sql,(offerType, ProviderID) )
        list_tested = self.cursor.fetchone()  # Get query response and store in variable

        return list_tested[0]

    def close (self,):
        self.db.close()


