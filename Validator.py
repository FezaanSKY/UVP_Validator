import traceback

from xmlschema.validators.exceptions import XMLSchemaDecodeError, XMLSchemaValidationError
from xmlschema import validate

class Validator:


    def validate (self,filelocation):
        return self.__xsd_validation__(filelocation)

    ## Private
    def __xsd_validation__(self, xml_location):
        try:
            if validate(xml_location, 'schemas/ADI_XSD.xsd'):
                return (True, 'XSD:Validation : \n Not valid! :(')
            else:
                return (True, 'XSD:Validation : \n Pass!')
        except XMLSchemaDecodeError as error:
            return (False, 'XSD:Validation : \n Not valid! :(')
        except XMLSchemaValidationError as error:
            return (False, 'XSD:Validation : \n Not valid! :(')
