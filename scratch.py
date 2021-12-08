from xmlschema import validate
#import xmlschema
print("===== XSD Validation===== ")
#import xmlschema
validate('ADI_DPL_Archive_EP.xml','MD-SP-VODContainer-I01.xsd' )

# import xmlschema
# # Baba script
# schema = xmlschema.XMLSchema('MD-SP-VODContainer-I01.xsd')
# schema.validate('ADI_DPL_Archive_EP.xml')



import xml.etree.ElementTree as ET
tree= ET.parse('ADI_DPL_Archive_EP.xml')
root = tree.getroot()
namespace = {'xmlns':"http://www.cablelabs.com/namespaces/metadata/xsd/vod30/1",
      'content':"http://www.cablelabs.com/namespaces/metadata/xsd/content/1",
      'core':"http://www.cablelabs.com/namespaces/metadata/xsd/core/1",
      'ext':"URN:NNDS:CMS:ADI3:01",
      'ns0':"http://my.inbcu.com/singlecms/vodmetadata/1.0",
      'offer':"http://www.cablelabs.com/namespaces/metadata/xsd/offer/1",
      's':"http://schemas.xmlsoap.org/soap/envelope/",
      'terms':"http://www.cablelabs.com/namespaces/metadata/xsd/terms/1",
      'title_ns':"http://www.cablelabs.com/namespaces/metadata/xsd/title/1",
      'vod30':"http://www.cablelabs.com/namespaces/metadata/xsd/vod30/1",
      'xsi':"http://www.w3.org/2001/XMLSchema-instance" }



print("=====General Info===== ")
for ns in root.findall('xmlns:Title', namespace):
    for elem in ns.iter():
        # print(elem)
        if("EpisodeName" in elem.tag):
            print("Episode Name:", elem.text)
    #Grabbing Title Medium
    for titleM in root.findall('xmlns:Title', namespace):
        for elem in titleM.iter():
            # print(elem)
            if("TitleMedium" in elem.tag):
                print("Title Medium:", elem.text)
    # Need to ensure the below are consistent across the ADI
    for title in root.findall('xmlns:Title', namespace):
        print("Licence StartDateTime:", title.attrib['startDateTime'], "\n"
              "Licence EndDateTime:", title.attrib['endDateTime'], "\n"
              "Provider Version Number:", title.attrib['providerVersionNum'], "\n"
             "URIID:", title.attrib['uriId'] )
    for times in root.findall('xmlns:Offer', namespace):
        print("Offer StartDateTime:", times.attrib['startDateTime'], "\n"
            "Offer EndDateTime:", times.attrib['endDateTime'])
for terms in root.findall('xmlns:Terms', namespace):
    for elem in terms.iter():
        #print(elem)
        if ("TermType" in elem.tag):
            print("OfferType:", elem.text)
for offer in root.findall('xmlns:Offer', namespace):
    for elem in offer.iter():
         # print(elem)
            if ("epgDateTime" in elem.attrib):
               print(elem.attrib)
for series in root.findall('xmlns:Title', namespace):
    for elem in series.iter():
         # print(elem)
            if ("episodeNumber" in elem.attrib):
               print(elem.attrib)
# Checking Video Info
print("=====Video Info=====")
for ns in root.findall('xmlns:Movie', namespace):
    for elem in ns.iter():
        #print(elem)
        if ("playListTemplateId" in elem.tag):
            print("playListTemplateId:", elem.text)
    for ns in root.findall('xmlns:Movie', namespace):
        for elem in ns.iter():
            # print(elem)
            if ("numMidRolls" in elem.tag):
                print("numMidRolls:", elem.text)
    for ns in root.findall('xmlns:Movie', namespace):
        for elem in ns.iter():
            # print(elem)
            if ("SourceUrl" in elem.tag):
                print("SourceUrl:", elem.text)
for ns in root.findall('xmlns:Title', namespace):
    for elem in ns.iter():
        # print(elem)
        if("DisplayRunTime" in elem.tag):
            print("DisplayRunTime:", elem.text)
    for ns in root.findall('xmlns:Movie', namespace):
            for elem in ns.iter():
                # print(elem)
                if ("Duration" in elem.tag):
                    print("Duration:", elem.text)
    for ns in root.findall('xmlns:Movie', namespace):
            for elem in ns.iter():
                # print(elem)
                if ("IsHDContent" in elem.tag):
                    print("IsHDContent:", elem.text)
print("===Checking Image info===")
# Checking Image Info - ensure the checksums match and correct image sizes
for ns in root.findall('xmlns:Thumbnail', namespace):
    for elem in ns.iter():
         # print(elem)
            if ("SourceUrl" in elem.tag):
               print("SourceUrl:", elem.text)
for ns in root.findall('xmlns:Ext', namespace):
    for elem in ns.iter():
         # print(elem)
            if ("SourceUrl" in elem.tag):
               print("SourceUrl:", elem.text)




# from scratches.validator import validate
# if validate("ADI.xml", "MD-SP-TITLE-I01.xsd"):
#     print('Valid! :)')
# else:
#     print('Not valid! :(')