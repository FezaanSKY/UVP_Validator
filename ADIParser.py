from common import *
import os
import xml.etree.ElementTree as ET
from checksums import calculate_md5_checksum_filesize

class db_Validation_Holder:
    providerID = ''
    dplTemplateID = ''
    genre = ''
    offerType = ''

class ADIParser:
    namespace = None
    environment = None
    validation_holder = db_Validation_Holder()
    def __init__(self, environment):
        self.namespace = {'xmlns': "http://www.cablelabs.com/namespaces/metadata/xsd/vod30/1",
                     'content': "http://www.cablelabs.com/namespaces/metadata/xsd/content/1",
                     'core': "http://www.cablelabs.com/namespaces/metadata/xsd/core/1",
                     'ext': "URN:NNDS:CMS:ADI3:01",
                     'ns0': "http://my.inbcu.com/singlecms/vodmetadata/1.0",
                     'offer': "http://www.cablelabs.com/namespaces/metadata/xsd/offer/1",
                     's': "http://schemas.xmlsoap.org/soap/envelope/",
                     'terms': "http://www.cablelabs.com/namespaces/metadata/xsd/terms/1",
                     'title_ns': "http://www.cablelabs.com/namespaces/metadata/xsd/title/1",
                     'vod30': "http://www.cablelabs.com/namespaces/metadata/xsd/vod30/1",
                     'xsi': "http://www.w3.org/2001/XMLSchema-instance"}

        self.environment = environment

    def __check_part__(self, asset):
        full_url = ""
        filesize = ""
        checksum = ""
        validation_result = ""
        result = ""
        for elem in asset.iter():

            if ("SourceUrl" in elem.tag):
                full_url = self.environment.getFilePath(elem.text)
                if os.path.exists(full_url) == False:
                    result += makeline(elem.text, " Not found in the uvp package")
                else:
                    result += makeline("SourceUrl:", elem.text)
                    filesize, checksum = calculate_md5_checksum_filesize(full_url)
            elif ("ContentFileSize" in elem.tag) and full_url != "":
                if elem.text == filesize:
                    validation_result += ("Content Filesize correct")
                else:
                    validation_result += ("Content Filesize incorrect")

            elif ("ContentCheckSum" in elem.tag) and full_url != "":
                if elem.text == checksum:
                    validation_result += (", ContentCheckSum correct ")
                else:
                    validation_result += (", ContentCheckSum incorrect")

        result += makeline(validation_result)
        return result

    def xmlparse(self):
        tree = ET.parse(self.environment.getFilePath("/ADI.xml"))
        root = tree.getroot()

        return self.__GeneralInfo__(root, self.namespace), self.__VideoInfo__(root, self.namespace), self.__ImageInfo__(root, self.namespace)

    def __GeneralInfo__(self, root, namespace):
        self.__populateValidationHolder__(root, namespace)
        self.__ProviderInfo__(root,namespace)
        result = ""
        result += makeline("=====General Info===== ")
        for ns in root.findall('xmlns:Title', namespace):
            for elem in ns.iter():
                if ("EpisodeName" in elem.tag):
                    result += makeline("Episode Name:", elem.text)

            # Grabbing Title Medium
            for titleM in root.findall('xmlns:Title', namespace):
                for elem in titleM.iter():
                    if ("TitleMedium" in elem.tag):
                        result += makeline("Title Medium:", elem.text)

            if self.validation_holder.providerID == "":
                result += makeline("ProviderID not found")
            else:
                result += makeline("ProviderID:", self.validation_holder.providerID)


            for title in root.findall('xmlns:Title', namespace):
                result += makeline("Licence StartDateTime:", title.attrib['startDateTime'], " ",
                                   self.__value_consistency__(root, 'startDateTime', title.attrib['startDateTime']), "\n"
                                    "Licence EndDateTime:", title.attrib['endDateTime'], " ",
                                   self.__value_consistency__(root, 'endDateTime', title.attrib['endDateTime']), "\n",
                                   self.__value_consistency__(root, 'providerVersionNum',     title.attrib['providerVersionNum']) )

        for times in root.findall('xmlns:Offer', namespace):
            result += makeline("Offer StartDateTime:", times.attrib['startDateTime'], "\n"
            "Offer EndDateTime:",times.attrib['endDateTime'],)


        for terms in root.findall('xmlns:Terms', namespace):
            for elem in terms.iter():
                if ("TermType" in elem.tag):
                    result += makeline("OfferType:", elem.text)

        if self.validation_holder.genre == "":
            result += makeline("Genre not found")
        else:
            result += makeline("Genre:", self.validation_holder.genre)


        for offer in root.findall('xmlns:Offer', namespace):
            for elem in offer.iter():
                if ("epgDateTime" in elem.attrib):
                    result += makeline(elem.attrib)
        for series in root.findall('xmlns:Title', namespace):
            for elem in series.iter():
                if ("episodeNumber" in elem.attrib):
                    result += makeline(str(elem.attrib))
        return result

    def __ProviderInfo__(self, root, namespace):
        self.validation_holder.providerID = root.find('xmlns:Title', namespace).attrib['uriId'].split('/')[0]

    def __DPLTemplateID__(self, root, namespace):
        self.validation_holder.dplTemplateID = root.find('xmlns:Movie', namespace)[0][0][0].text

    def __Genre__(self, root, namespace):
        self.validation_holder.genre = root.find('xmlns:Title', namespace)[5].text

    def __OfferType__(self, root, namespace):
        self.validation_holder.offerType = root.find('xmlns:Terms', namespace)[0][0].text

    def __populateValidationHolder__(self, root, namespace):
        self.__ProviderInfo__(root,namespace)
        self.__DPLTemplateID__(root, namespace)
        self.__Genre__(root, namespace)
        self.__OfferType__(root, namespace)



    def __VideoInfo__(self, root, namespace):
        result = ""
        # Checking Video Info
        result += makeline("=====Video Info=====")
        for ns in root.findall('xmlns:Movie', namespace):
            for elem in ns.iter():
                if ("playListTemplateId" in elem.tag):
                    result += makeline("playListTemplateId:", elem.text)
            for ns in root.findall('xmlns:Movie', namespace):
                for elem in ns.iter():
                    if ("numMidRolls" in elem.tag):
                        result += makeline("numMidRolls:", elem.text)

            for ns in root.findall('xmlns:Movie', namespace):
                for elem in ns.iter():
                    if ('assetPart' in elem.tag):
                        result += self.__check_part__(elem)

        for ns in root.findall('xmlns:Title', namespace):
            for elem in ns.iter():
                if ("DisplayRunTime" in elem.tag):
                    result += makeline("DisplayRunTime:", elem.text)
            for ns in root.findall('xmlns:Movie', namespace):
                for elem in ns.iter():
                    if ("Duration" in elem.tag):
                        result += makeline("Duration:", elem.text)
            for ns in root.findall('xmlns:Movie', namespace):
                for elem in ns.iter():
                    if ("IsHDContent" in elem.tag):
                        result += makeline("IsHDContent:", elem.text)
        return result


    def __ImageInfo__(self, root, namespace):
        result = ""

        result += makeline("===Checking Image info===")
        # Checking Image Info - ensure the checksums match and correct image sizes
        for ns in root.findall('xmlns:Thumbnail', namespace):
            for elem in ns.iter():
                if ("Thumbnail" in elem.tag):
                    # result += makeline("SourceUrl:", elem.text)
                    result += self.__check_part__(elem)

        for ns in root.findall('xmlns:Ext', namespace):
            for elem in ns.iter():
                if ("CategoryImage" in elem.tag or "PressPackImage" in elem.tag):
                    result += self.__check_part__(elem)

        return result

    def __value_consistency__(self, root, attribute, value):
        namespace = self.namespace

        for content in root.findall('xmlns:ContentGroup', namespace):
            if content.attrib[attribute] != value:
                return (attribute + " Not consistent across XML")
        for title in root.findall('xmlns:Title', namespace):
            if title.attrib[attribute] != value:
                return (attribute + " Not consistent across XML")
        for movie in root.findall('xmlns:Movie', namespace):
            if movie.attrib[attribute] != value:
                return (attribute + " Not consistent across XML")
        for thumbnail in root.findall('xmlns:Thumbnail', namespace):
            if thumbnail.attrib[attribute] != value:
                return (attribute + " Not consistent across XML")

        for ns in root.findall('xmlns:Ext', namespace):
            for elem in ns.iter():
                if ("CategoryImage" in elem.tag or "PressPackImage" in elem.tag):
                    if elem.attrib[attribute] != value:
                        return (attribute + " Not consistent across XML")

        return attribute + " is consistent across XML"







