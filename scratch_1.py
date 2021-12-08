import xml.etree.ElementTree as ET
tree= ET.parse('ADI_DPL_CUTV_EP.xml')
root = tree.getroot()

namespace = {'xmlns':"http://www.cablelabs.com/namespaces/metadata/xsd/vod30/1",
      'xmlns:content':"http://www.cablelabs.com/namespaces/metadata/xsd/content/1",
      'xmlns:core':"http://www.cablelabs.com/namespaces/metadata/xsd/core/1",
      'xmlns:ext':"URN:NNDS:CMS:ADI3:01",
      'xmlns:ns0':"http://my.inbcu.com/singlecms/vodmetadata/1.0",
      'xmlns:offer':"http://www.cablelabs.com/namespaces/metadata/xsd/offer/1",
      'xmlns:s':"http://schemas.xmlsoap.org/soap/envelope/",
      'xmlns:terms':"http://www.cablelabs.com/namespaces/metadata/xsd/terms/1",
      'xmlns:title':"http://www.cablelabs.com/namespaces/metadata/xsd/title/1",
      'xmlns:vod30':"http://www.cablelabs.com/namespaces/metadata/xsd/vod30/1",
      'xmlns:xsi':"http://www.w3.org/2001/XMLSchema-instance" }
#
# for Title in root.findall('xmlns:Title', namespace):
#      print(Title.attrib)

for elem in root:
      print (elem)
      for elem1 in elem:
            print(elem1)
            for elem2 in elem1:
                  print(elem2)











# import xml.etree.ElementTree as ET
# tree=ET.parse('ADI.xml')
# root = tree.getroot()
# # episodes = tree.findall('.//EpisodeName')
# # for episode in episodes:
# #  print(episode.text)
# #
# for elem in root.iter():
#       print(elem)
#




# import xml.dom.minidom
#
# docs = xml.dom.minidom.parse("ADI.xml")
# prettyxml = docs.toprettyxml()
#
# #print(prettyxml)
#
# Title = docs.getElementsByTagName('Title')
# for info in Title:
#     end_time = info.getAttribute('endDateTime')
#     start_time = info.getAttribute('startDateTime')
#     pvn = info.getAttribute('providerVersionNum')
#     print(' StartDateTime: ' + start_time + '\t EndDateTime: ' + end_time + '\t ProviderVersionNumber: '+ pvn)
#

# import xml.etree.ElementTree as ET
# root = ET.parse('ADI.xml').getroot()
# #print(root)
# for element in root:
#    #print(element)
#    for next1 in element:
#        #print(next1)
#        for next2 in next1:
#            print(next2.text)
#