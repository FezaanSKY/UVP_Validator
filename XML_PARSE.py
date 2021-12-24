import xml.etree.ElementTree as ET
from xmlschema.validators.exceptions import XMLSchemaDecodeError
from xmlschema import validate
import tarfile
import os
import hashlib

from checksums import calculate_md5_checksum_filesize


def untar(filelocation):
    # declare filename
    filename = os.path.basename(filelocation)
    # open file in write mode
    file_obj = tarfile.open(str(filelocation), "r")
    # get the names of files in tar file
    namelist = file_obj.getnames()
    # print the filenames
    inside_tar = ""
    message = ("The following files are being extracted:")
    for name in namelist:
        inside_tar += makeline(name)
    # extract all files
    file = file_obj.extractall(f"{filename}_Extracted")
     # close file
    file_obj.close()
    return message + "\n" + inside_tar


def xsd_validation(filelocation):
    file_name = str(filelocation).split('/')
    file_name = file_name[len(file_name)-1]
    xml_location = os.getcwd() + '\\' + file_name.replace(".uvp",".uvp_Extracted/ADI.xml")
    try:
        if validate(xml_location, 'ADI_XSD.xsd'):
            return ('XSD:Validation : \n Not valid! :(')
        else:
            return('XSD:Validation : \n Pass!')
    except XMLSchemaDecodeError as error:
        return(error.message, error)


def makeline(*args):
    result = ""
    for arg in args:
        result += arg

    result += "\n"
    return result

def xml_parse(filelocation):
    file_name = str(filelocation).split('/')
    file_name = file_name[len(file_name) - 1]
    dir_location = os.getcwd() + '\\' + file_name.replace(".uvp", ".uvp_Extracted/")
    xml_location = dir_location + "ADI.xml"
    tree = ET.parse(xml_location)
    root = tree.getroot()
    namespace = {'xmlns': "http://www.cablelabs.com/namespaces/metadata/xsd/vod30/1",
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

    var = ""


    var += makeline("=====General Info===== ")
    for ns in root.findall('xmlns:Title', namespace):
        for elem in ns.iter():
            # var+=makeline(elem)
            if ("EpisodeName" in elem.tag):
                var += makeline("Episode Name:", elem.text)

        # Grabbing Title Medium
        for titleM in root.findall('xmlns:Title', namespace):
            for elem in titleM.iter():
                if ("TitleMedium" in elem.tag):
                    var += makeline("Title Medium:", elem.text)

        # Need to ensure the below are consistent across the ADI
        ####
        for title in root.findall('xmlns:Title', namespace):
            var+=makeline("Licence StartDateTime:", title.attrib['startDateTime'], " ", value_consistency(root,'startDateTime',title.attrib['startDateTime']), "\n"
                "Licence EndDateTime:", title.attrib['endDateTime']," ",value_consistency(root,'endDateTime',title.attrib['endDateTime']), "\n"
                "Provider Version Number:", title.attrib['providerVersionNum']," ",value_consistency(root,'providerVersionNum',title.attrib['providerVersionNum']), "\n")
## Come back to this split up URID TO provider and asset id
 # "URIID:", title.attrib['uriId'], " ", value_consistency(root, 'uriId', title.attrib['uriId'])
        for times in root.findall('xmlns:Offer', namespace):
            var += makeline("Offer StartDateTime:", times.attrib['startDateTime'], "\n"
                "Offer EndDateTime:", times.attrib['endDateTime'])
    for terms in root.findall('xmlns:Terms', namespace):
        for elem in terms.iter():
            if ("TermType" in elem.tag):
                var += makeline("OfferType:", elem.text)
    for offer in root.findall('xmlns:Offer', namespace):
        for elem in offer.iter():
            if ("epgDateTime" in elem.attrib):
                var += makeline(elem.attrib)
    for series in root.findall('xmlns:Title', namespace):
        for elem in series.iter():
            if ("episodeNumber" in elem.attrib):
                var += makeline(str(elem.attrib))

    # Checking Video Info
    var+=makeline("=====Video Info=====")
    for ns in root.findall('xmlns:Movie', namespace):
        for elem in ns.iter():
            if ("playListTemplateId" in elem.tag):
                var += makeline("playListTemplateId:", elem.text)
        for ns in root.findall('xmlns:Movie', namespace):
            for elem in ns.iter():
                if ("numMidRolls" in elem.tag):
                    var += makeline("numMidRolls:", elem.text)

        for ns in root.findall('xmlns:Movie', namespace):
            for elem in ns.iter():
                if ('assetPart' in elem.tag):
                    var += check_part(elem, dir_location)



    for ns in root.findall('xmlns:Title', namespace):
        for elem in ns.iter():
            if ("DisplayRunTime" in elem.tag):
                var += makeline("DisplayRunTime:", elem.text)
        for ns in root.findall('xmlns:Movie', namespace):
            for elem in ns.iter():
                if ("Duration" in elem.tag):
                    var += makeline("Duration:", elem.text)
        for ns in root.findall('xmlns:Movie', namespace):
            for elem in ns.iter():
                if ("IsHDContent" in elem.tag):
                    var += makeline("IsHDContent:", elem.text)



    var+=makeline("===Checking Image info===")
    # Checking Image Info - ensure the checksums match and correct image sizes
    for ns in root.findall('xmlns:Thumbnail', namespace):
        for elem in ns.iter():
            if ("Thumbnail" in elem.tag):
                # var += makeline("SourceUrl:", elem.text)
                var += check_part(elem, dir_location)

    for ns in root.findall('xmlns:Ext', namespace):
        for elem in ns.iter():
            if ("CategoryImage" in elem.tag or "PressPackImage" in elem.tag):
                var += check_part(elem, dir_location)
    return var




def value_consistency(root,attribute,value):
    namespace = {'xmlns': "http://www.cablelabs.com/namespaces/metadata/xsd/vod30/1",
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

    return (attribute + " is consistent across XML")



def check_part(asset,dir_location):
    full_url = ""
    filesize = ""
    checksum = ""
    validation_result = ""
    result= ""
    for elem in asset.iter():

        if ("SourceUrl" in elem.tag):
            full_url = dir_location + elem.text
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






