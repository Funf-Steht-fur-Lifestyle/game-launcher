import os
import shutil

class Exporter():
    def create_csv_file(self, filename, dataset):
        current_dir = os.getcwd()
        csv_dir = os.path.join(current_dir, 'game_launcher_csv/')

        if not os.path.exists(csv_dir):
            os.makedirs(csv_dir)

        csv_file = open(os.path.join(csv_dir, filename), 'w+')
        csv_file.write(dataset.csv)
        csv_file.close()


    def export_csv(self, filename, resource):
        dataset = resource.export()
        self.create_csv_file(filename, dataset)


    def delete_csv_dir(self):
        current_dir = os.getcwd()
        csv_dir = os.path.join(current_dir, 'game_launcher_csv/')

        shutil.rmtree(csv_dir)
