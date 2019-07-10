from datapackage import Package, Resource
from pathlib import Path
from FrictionlessDarwinCore import DwCResource

import zipfile

class DwCPackage(Package):
    def __init__(self, dwca,base_path=None):
        Package.__init__(self,base_path=base_path)
        self.dwca_path = Path(dwca)

    def infer(self):
        zf = zipfile.ZipFile(self.dwca_path)
        fdp_folder = Path(self.dwca_path).parent / 'datapackage'
        fdp_folder.mkdir(0o777, False, True)
        Package.base_path=str(fdp_folder)
        for info in zf.infolist():
            ofile = fdp_folder / info.filename
            if ofile.suffix == '.txt':
                ofile = ofile.with_suffix('.csv')
            ofile.touch()
            ofile.write_bytes(zf.read(info.filename))
            r= DwCResource({'path': str(ofile.name)},base_path=self.base_path)
            r.infer()
            Package.add_resource(self,r.descriptor)

if __name__ == '__main__':
    p = DwCPackage('../tmp/dwca-rbins_saproxilyc_beetles-v9.37.zip', '../tmp/dwca-rbins_saproxilyc_beetles-v9.37')
    p.infer()
    p.save('../tmp/fdwc.zip')
    p2= Package('../tmp/fdwc.zip')
    print(p.valid)