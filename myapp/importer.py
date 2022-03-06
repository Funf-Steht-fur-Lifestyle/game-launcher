from tablib import Dataset

class Importer():
    def import_csv_file(self, csv_data, resource):
        dataset = Dataset()
        importer_data = dataset.load(csv_data, format='csv')
        result = self.test_import(resource, dataset)

        if not result.has_errors():
            resource.import_data(dataset, dry_run=False)


    def test_import(self, resource, dataset):
        return resource.import_data(dataset, dry_run=True)
