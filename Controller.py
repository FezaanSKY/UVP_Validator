from ADIParser import ADIParser
from Environment import Environment
from Validator import Validator


class Controller:
    untarResult = ""
    environment = None
    validator = None
    xml_parser = None

    def __init__(self,filelocation):
        self.environment = Environment(filelocation)
        self.untarResult = self.environment.new_directory()
        self.validator = Validator()
        self.xml_parser = ADIParser(self.environment)

    def validate(self):
        return self.validator.validate(self.environment.working_environment + "ADI.xml")

    def parse(self):
        string1, string2, string3 = self.xml_parser.xmlparse()

        return str(string1) + "\n" + str(string2) + "\n" + str(string3)
