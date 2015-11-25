import unittest
import tempfile
import os
import neroman

class TestSpecifyExperiments(unittest.TestCase):    
    
    def setUp(self):
        
        #Create a database
        self.database_file = "database.yaml"
        with open(self.database_file, 'w') as f:
            f.write("experiment1:\n"
                    "   run_command_prefix: python3\n"
                    "   main_code_file: party.py\n"
                    "   parameters:\n"
                    "        when: now\n"
                    "   parameters_format:\n"
                    "       'when'")
        
        #Initialize Neroman with database
        self.testman = neroman.Neroman(database=self.database_file)
        
        #Create an experiment folder
        self.folder = tempfile.mkdtemp()
        self.path = os.path.join(self.folder, neroman.CONFIG_FILENAME)
        with open(self.path, 'w') as f:
            f.write("run_command_prefix: python\n"
                    "main_code_file: sleep.py\n"
                    "parameters:\n"
                    "   count: 5\n"
                    "   interval: 5\n"
                    "parameters_format:\n"
                    "   'count interval'")
    
    def tearDown(self):
        os.remove(self.database_file)
        os.remove(self.path)
        os.removedirs(self.folder)
        

    def test_no_experiment_folder(self):
        """
        """
        with self.assertRaises(FileNotFoundError):
            self.testman.specify_experiments('/nonexistent')


    def test_no_config_file_in_folder(self):
        empty_folder = tempfile.mkdtemp()
        with self.assertRaises(FileNotFoundError):
            self.testman.specify_experiments(empty_folder)
        os.removedirs(empty_folder)

    def test_empty_config_file(self):
        open(self.path, 'w').close()
        with self.assertRaises(neroman.FormatError):
            self.testman.specify_experiments(self.folder)

    def test_read_experiment(self):
        self.testman.specify_experiments(self.folder)
        fields = ['run_command_prefix', 'main_code_file', 
                'parameters', 'parameters_format']
        values = ['python', 'sleep.py', {'count': 5, 'interval': 5}, 
                'count interval']
        for i, field in enumerate(fields):
            with self.subTest(field=field):
                self.assertEqual(values[i], 
                                self.testman.experiments[self.folder][field])

    def test_badly_formatted_config_file(self):
        with open(self.path, 'w') as f:
            f.write("run_command_prefix: python\n"
                    "parameters:\n"
                    "   count: 5\n"
                    "   interval: 5\n"
                    "parameters_format:\n"
                    "   'count interval'")
        with self.assertRaises(neroman.FormatError):
            self.testman.specify_experiments(self.folder)

if __name__ == '__main__':
    unittest.main()
