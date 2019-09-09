from hashlib import blake2b
import datetime
import xml.etree.ElementTree as ET

class DwCMetadata:

    def __init__(self, eml):
        self.allLines= []
        self.emls= eml

    def convert(self):
        self.valid=False
        try:
            self.allLines= []
            root = ET.fromstring(self.emls)
            dataset = root.find('./dataset')
            self._title(dataset.find('./title'))
            for ai in dataset.findall('./alternateIdentifier'):
                self._element(ai)
            self._element(dataset.find('./pubDate'))
            self._element(dataset.find('./language'))
            self._person(dataset.find('./creator'))
            self._person(dataset.find('./metadataProvider'))
            self._person(dataset.find('./associatedParty'))
            self._abstract(dataset.find('./abstract'))
            self._keywords(dataset)
            self._intellectualRigths(dataset)
            self._geographicCoverage(dataset.find('./coverage/geographicCoverage'))
            self._taxonomicCoverage(dataset.find('./coverage/taxonomicCoverage'))
            self._maintenance(dataset.find('./maintenance'))
            self._person(dataset.find('./contact'))
            self._methods(dataset.find('./methods'))
            self._project(dataset.find('./project'))
            self._additionalMetadata(root.find('./additionalMetadata'))
            hash =blake2b(key=b'FrictionlessDarwinCore', digest_size=16)
            for line in self.allLines:
                hash.update(line.encode('utf-8'))
            self._about()
            self.hexdigest= hash.hexdigest()
        except:
            print(eml)
        finally:
            self.valid=True
        return self.as_markdown()

    def as_markdown(self):
        s='\n\n'
        return s.join(self.allLines)

    def hexgigest(self):
        return self.hexdigest

    def _about(self):
        self._addLine('---')
        self._addLine('generated by [FrictionlessDarwinCore](https://github.com/frictionlessdata/FrictionlessDarwinCore)')

    def _addLine(self, line):
        self.allLines.append(line)

    def _title(self, element):
        self._addLine('# ' + element.text)

    def _element(self, element):
        self._addLine(element.tag + ': '+ element.text)

    def _abstract(self, element):
        if element != None:
            self._addLine('## '+ element.tag)
            for p in element.findall('./para'):
                self._addLine(p.text)

    def _keywords(self, element):
        if element != None:
            self._addLine('## Keywords')
            for k in element.findall('./keywordSet'):
                self._addLine('*'+ k.findtext('./keyword') + '* ' + k.findtext('./keywordThesaurus'))

    def _intellectualRigths(self, element):
        if element != None:
            ipr= element.find('./intellectualRights')
            if ipr != None:
                self._addLine('## Intellectual Property Rights')
                self._addLine(ipr.findtext('./para') + ' ['+ ipr.findtext('./para/ulink/citetitle') + ']('+ipr.findtext('./para/ulink') + ')')

    def _geographicCoverage(self, element):
        if element != None:
            self._addLine('## Geographic Coverage')
            self._addLine('Description: ' + element.findtext('./geographicDescription'))
            self._addLine('BoundingCoordinates: West:' + element.findtext('./boundingCoordinates/westBoundingCoordinate') +
                '°, East:' + element.findtext('./boundingCoordinates/eastBoundingCoordinate') +
                '°, North:' + element.findtext('./boundingCoordinates/northBoundingCoordinate') +
                '°, South:' + element.findtext('./boundingCoordinates/southBoundingCoordinate') + '°')

    def _taxonomicCoverage(self, element):
        if element != None:
            self._addLine('## Taxonomic Coverage')
            gtc=element.find('./generalTaxonomicCoverage')
            if gtc != None:
                self._element(gtc)
            self._addLine('### Classification')
            for tc in element.findall('./taxonomicClassification/*'):
                self._element(tc)

    def _maintenance(self, element):
        if element != None:
            self._addLine('## Maintenance')
            self._addLine(element.findtext('./description/para'))
            muf=element.find('./maintenanceUpdateFrequency')
            if muf != None:
                self._element(muf)

    def _methods(self, element):
        if element != None:
            self._addLine('## Methods')
            ms=element.findtext('./methodStep/description/para')
            if ms != None:
                self._addLine('methodStep: ' + ms)
            se=element.findtext('./sampling/studyExtent/description/para')
            if se != None:
                self._addLine('studyExtent: ' + se)
            sd=element.findtext('./sampling/samplingDescription/para')
            if sd != None:
                self._addLine('samplingDescription: ' + sd)

    def _project(self, element):
        if element != None:
            self._addLine('## Project')
            id=element.get('id')
            if id !=None:
                self._addLine('id='+element.get('id'))
            title = element.find('./title')
            if title != None:
                self._element(title)
            self._person(element.find('./personnel'))
            self._abstract(element.find('./abstract'))
            self._abstract(element.find('./funding'))
            sad=element.findtext('./studyAreaDescription/descriptor/descriptorValue')
            if sad != None:
                self._addLine('## study area description')
                self._addLine(sad)
            dd=element.findtext('./designDescription/description/para')
            if dd != None:
                self._addLine('## design description')
                self._addLine(dd)

    def _person(self, element):
        if element != None:
            self._addLine('## ' + element.tag)
            ind=element.find('./individualName')
            if ind != None :
                name=''
                if element.find('./givenName') != None:
                    name = element.find('./givenName') + ' '
                if element.find('./surName') != None:
                    element.findtext('./surName')
                self._addLine('Name:'+name)
            org=element.findtext('./organizationName')
            if org != None:
                self._addLine('Organization:'+ org)
            pos=element.findtext('./positionName')
            if pos != None:
                self._addLine('Position:'+ pos)
            email=element.findtext('./electronicMailAddress')
            if email != None:
                self._addLine('email:'+email)
            userid=element.find('./userId')
            if userid != None:
                self._addLine('userId:'+userid.text+ ' ('+ userid.get('directory') + ')')

    def _additionalMetadata(self, element):
        if element != None:
            self._addLine('## Additional Metadata')
            for am in element.findall('./metadata/gbif/*'):
                self._element(am)

