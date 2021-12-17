import xml.etree.ElementTree as ET
from xmlschema.validators.exceptions import XMLSchemaDecodeError
from xmlschema import validate
import tarfile
import os

def untar(filelocation):
    # destination path
    #destination = os.path.dirname(filelocation)
    #os.chdir(destination)
    # declare filename
    filename = os.path.basename(filelocation)
    # open file in write mode
    file_obj = tarfile.open(str(filelocation), "r")
    # get the names of files in tar file
    namelist = file_obj.getnames()
    # print the filenames
    print("The following files are being extracted:")
    for name in namelist:
        print(name)
    # extract all files
    file = file_obj.extractall(f"{filename}_Extracted")
     # close file
    file_obj.close()



def xsd_validation(filelocation):
   # print("XSD_VALIDATION")
   # xml_location = filelocation.replace(".tar",".tar_Extracted/ADI.xml")
    file_name = str(filelocation).split('/')
    file_name = file_name[len(file_name)-1]
    xml_location = os.getcwd() + '\\' + file_name.replace(".tar",".tar_Extracted/ADI.xml")
    # print(xml_location)
    # print(file_name)
    # print(os.getcwd())
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
    xml_location = os.getcwd() + '\\' + file_name.replace(".tar", ".tar_Extracted/ADI.xml")
    # print(xml_location)
    # print(file_name)
    # print(os.getcwd())
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

    var+=makeline("=====General Info===== ")
    for ns in root.findall('xmlns:Title', namespace):
        for elem in ns.iter():
            # var+=makeline(elem)
            if ("EpisodeName" in elem.tag):
                var+=makeline("Episode Name:", elem.text)
        # Grabbing Title Medium
        for titleM in root.findall('xmlns:Title', namespace):
            for elem in titleM.iter():
                # var+=makeline(elem)
                if ("TitleMedium" in elem.tag):
                    var+=makeline("Title Medium:", elem.text)
        # Need to ensure the below are consistent across the ADI
        for title in root.findall('xmlns:Title', namespace):
            var+=makeline("Licence StartDateTime:", title.attrib['startDateTime'], "\n"
                "Licence EndDateTime:", title.attrib['endDateTime'], "\n"
                "Provider Version Number:", title.attrib['providerVersionNum'], "\n"
                "URIID:", title.attrib['uriId'])
        for times in root.findall('xmlns:Offer', namespace):
            var+=makeline("Offer StartDateTime:", times.attrib['startDateTime'], "\n"
                "Offer EndDateTime:", times.attrib['endDateTime'])
    for terms in root.findall('xmlns:Terms', namespace):
        for elem in terms.iter():
            # var+=makeline(elem)
            if ("TermType" in elem.tag):
                var+=makeline("OfferType:", elem.text)
    for offer in root.findall('xmlns:Offer', namespace):
        for elem in offer.iter():
            # var+=makeline(elem)
            if ("epgDateTime" in elem.attrib):
                var+=makeline(elem.attrib)
    for series in root.findall('xmlns:Title', namespace):
        for elem in series.iter():
            # var+=makeline(elem)
            if ("episodeNumber" in elem.attrib):
                var+=makeline(str(elem.attrib))
    # Checking Video Info
    var+=makeline("=====Video Info=====")
    for ns in root.findall('xmlns:Movie', namespace):
        for elem in ns.iter():
            # var+=makeline(elem)
            if ("playListTemplateId" in elem.tag):
                var+=makeline("playListTemplateId:", elem.text)
        for ns in root.findall('xmlns:Movie', namespace):
            for elem in ns.iter():
                # var+=makeline(elem)
                if ("numMidRolls" in elem.tag):
                    var+=makeline("numMidRolls:", elem.text)
        for ns in root.findall('xmlns:Movie', namespace):
            for elem in ns.iter():
                # var+=makeline(elem)
                if ("SourceUrl" in elem.tag):
                    var+=makeline("SourceUrl:", elem.text)
    for ns in root.findall('xmlns:Title', namespace):
        for elem in ns.iter():
            # var+=makeline(elem)
            if ("DisplayRunTime" in elem.tag):
                var+=makeline("DisplayRunTime:", elem.text)
        for ns in root.findall('xmlns:Movie', namespace):
            for elem in ns.iter():
                # var+=makeline(elem)
                if ("Duration" in elem.tag):
                    var+=makeline("Duration:", elem.text)
        for ns in root.findall('xmlns:Movie', namespace):
            for elem in ns.iter():
                # var+=makeline(elem)
                if ("IsHDContent" in elem.tag):
                    var+=makeline("IsHDContent:", elem.text)
    var+=makeline("===Checking Image info===")
    # Checking Image Info - ensure the checksums match and correct image sizes
    for ns in root.findall('xmlns:Thumbnail', namespace):
        for elem in ns.iter():
            # var+=makeline(elem)
            if ("SourceUrl" in elem.tag):
                var+=makeline("SourceUrl:", elem.text)
    for ns in root.findall('xmlns:Ext', namespace):
        for elem in ns.iter():
            # var+=makeline(elem)
            if ("SourceUrl" in elem.tag):
                var+=makeline("SourceUrl:", elem.text)
    return var
