import traceback

from xmlschema.validators.exceptions import XMLSchemaDecodeError
from xmlschema import validate

class Validator:


    def validate (self,filelocation):
        return self.__xsd_validation__(filelocation)

    ## Private
    def __xsd_validation__(self, xml_location):
        try:
            if validate(xml_location, 'ADI_XSD.xsd'):
                return ('XSD:Validation : \n Not valid! :(')
            else:
                return ('XSD:Validation : \n Pass!')
        except XMLSchemaDecodeError as error:
            return "%s\n%s" % (error.message, traceback.format_exc())