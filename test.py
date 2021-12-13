import xml.etree.ElementTree as ET

# I saved all of the namespaces provided into a dictionary to make life easier
ns = {
    'title_ns': 'http://www.cablelabs.com/namespaces/metadata/xsd/title/1',
    'xsi_ns': 'http://www.w3.org/2001/XMLSchema-instance',
    'vod30_ns': 'http://www.cablelabs.com/namespaces/metadata/xsd/vod30/1',
    'terms_ns': 'http://www.cablelabs.com/namespaces/metadata/xsd/terms/1',
    's_ns': 'http://schemas.xmlsoap.org/soap/envelope/',
    'offer_ns': 'http://www.cablelabs.com/namespaces/metadata/xsd/offer/1',
    'ns0_ns': 'http://my.inbcu.com/singlecms/vodmetadata/1.0',
    'ext_ns': 'URN:NNDS:CMS:ADI3:01',
    'core_ns': 'http://www.cablelabs.com/namespaces/metadata/xsd/core/1',
    'content_ns': 'http://www.cablelabs.com/namespaces/metadata/xsd/content/1',
    'xml_ns': 'http://www.cablelabs.com/namespaces/metadata/xsd/vod30/1',
}

# I think you understand this bit, but if not give me a shout
tree = ET.parse('ADI.xml')
root = tree.getroot()

# Generic solution, prints all values of the child elements. However, must iterate to the correct depth of the XML file
def process_elements(lt):
    for child in list(lt):
        print(child.text)
        print(child.attrib)

# More bespoke solution, iterates through the XML file, using the namespaces provided, this way I can specifcally find the...
# ... tag that you would be looking for and return the value. For a single piece of text, .text works fine, however for...
# ... dictionaries like the actors details, must use .attrib. Annoying .text works for specific things, and .attrib works for...
# ... others, but both have unique use cases and can't be used interchangeably

# Finds the Tag 'Title' in the XML file
for Title in root.findall('xml_ns:Title', ns):
    # print(Title.attrib)
    # Find the tag 'Ext' in the 'core' subelement of the 'Title' element
    for core in Title.findall('core_ns:Ext', ns):
        # Finds the 'LocalizableTitleExt' tag in the 'ext' subelement of the 'core' subelement of the the 'Title element'
        for lte in core.findall('ext_ns:LocalizableTitleExt', ns):
            # print(lte.attrib)
            # Finds the 'EpisodeName' tag in the 'LocalizableTitleExt subelement.
            for episodename in lte.findall('ext_ns:EpisodeName', ns):
                print(episodename.text)
    # This part goes back to the 'Title' element and finds the new subelement of 'LocalizableTitle' to then iterate over it
    for lt in Title.findall('title_ns:LocalizableTitle', ns):
        # print(lt.attrib)
        for titlebrief in lt.findall('title_ns:TitleBrief', ns):
            print(titlebrief.text)
        for titlemedium in lt.findall('title_ns:TitleMedium', ns):
            print(titlemedium.text)
        for titlelong in lt.findall('title_ns:TitleLong', ns):
            print(titlelong.text)
        for summaryshort in lt.findall('title_ns:SummaryShort', ns):
            print(summaryshort.text)
        for actor in lt.findall('title_ns:Actor', ns):
            print(actor.attrib)

    # print("Start of function")
    # process_elements(lt)
