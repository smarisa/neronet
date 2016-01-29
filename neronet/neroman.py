# -*- coding: utf-8 -*-
"""This module defines Neroman.

To work with Neroman each experiment must have the following attributes
defined in its config:

* experiment_id: The unique identifier for the experiment
* run_command_prefix: The run command of the experiment
* main_code_file: The code file to be run
* destination_folder: Folder that the experiment is run in on the cluster.
* parameters: The definition of the experiment parameters
* parameters_format: The format of the experiment parameters
* logoutput: The location the experiment outputs its output
* state: A tuple of the experiment state which is set to 'defined' by this
  function and the time changed
* cluster: The cluster that the experiment is running on. Set to
  None by this function
* time_created: Sets the current time as the creation time
* time_modified: The time the experiment was last modified. Sets
  this time to the same as the time created
* path: The absolute path to the folder

"""

import os
import time
import datetime
import os.path
import collections
import pickle
import shutil

import neronet.core
import neronet.config_parser

DATABASE_FILENAME = 'default.yaml'
PREFERENCES_FILENAME = 'preferences.yaml'
CLUSTERS_FILENAME = 'clusters.yaml'

class Neroman:

    """The part of Neronet that handles user side things.

    Attributes:
        clusters (Dict): A dictionary containing the specified clusters
        database (Dict): A dictionary containing the specified experiments
        preferences (Dict): A dictionary containing the preferences
    """

    def __init__(self):
        """Initializes Neroman

        Reads the contents of its attributes from yaml files or creates them
        """
        self.config_parser = neronet.config_parser.ConfigParser()
        self.clusters, self.preferences, self.database = \
            self.config_parser.load_configurations(CLUSTERS_FILENAME, \
                            PREFERENCES_FILENAME, DATABASE_FILENAME)

    def clean(self):
        """Removes all neronet related data"""
        self.config_parser.remove_data()

    def specify_cluster(
            self,
            cluster_name,
            ssh_address,
            cluster_type,
            portnumber=22):
        """Specify clusters so that Neroman is aware of them.

        Writes cluster name, address and type to the clusters config file

        Args:
            cluster_name (str): The name of the cluster, should be unique
            ssh_address (str): SSH address of the cluster
            cluster_type (str): Type of the cluster. Either slurm or unmanaged

        Raises:
            FormatError: if the cluster type isn't unmanaged or slurm

        """
        if cluster_type != 'slurm' and cluster_type != 'unmanaged':
            raise neronet.config_parser.FormatError( \
                        "Cluster type should be slurm or unmanaged")

        self.clusters['clusters'][cluster_name] = {'ssh_address': ssh_address,
                                                   'type': cluster_type,
                                                   'port': portnumber}

        self.config_parser.save_clusters(CLUSTERS_FILENAME, self.clusters)

    def specify_experiments(self, folder):
        """Specify experiments so that Neroman is aware of them.

        Reads the contents of the experiment from a config file inside the
        specified folder.

        Args:
            folder (str): The path of the folder that includes
                the experiment that's being specified.

        Raises:
            IOError: If the folder doesn't exists or the config file
                doesn't exists
            FormatError: If the config file is badly formated
        """


        experiments = self.config_parser.parse_experiments(folder)
        for experiment in experiments:
            if experiment.id in self.database:
                raise IOError("Experiment named %s already in the database" \
                                % experiment.id)
            else: self.database[experiment.id] = experiment
        self.config_parser.save_database(DATABASE_FILENAME, \
                                        self.database)

    def specify_user(self, name, email, default_cluster = ""):
        """Update user data"""
        self.preferences['name'] = name
        self.preferences['email'] = email
        self.preferences['default_cluster'] = default_cluster
        self.config_parser.save_preferences(PREFERENCES_FILENAME, \
                                            self.preferences)

    def delete_experiment(self, experiment_id):
        """Deletes the experiment with the given experiment id

        Parameters:
            experiment_id (str): id of the experiment to be deleted
        Raises:
            KeyError: if the experiment with the given id doesn't exist
        """
        self.database.pop(experiment_id)
        self.config_parser.save_database(DATABASE_FILENAME, \
                                        self.database)

    def get_experiment_results(self, experiment_id, remote_dir, local_dir):
        """Get the experiment results from neromum

        Args:
            experiment_id (str): the experiment ID.
            remote_dir (str): the file path to results folder on the remote
                machine.
            local_dir (str): the file path to results folder on the local
                machine.
        """
        experiment = self.database[experiment_id]
        cluster_ID = experiment.cluster
        cluster_port = self.clusters['clusters'][cluster_ID]['port']
        cluster_address = self.clusters['clusters'][cluster_ID]['ssh_address']
        neronet.core.osrun(
            'rsync -az -e "ssh -p%s" "%s:%s" "%s"'
            % (cluster_port, cluster_address,
                remote_dir, local_dir))

    def status_gen(self, arg):
        """Creates a generator that generates the polled status

        Yields:
            str: A line of neroman status
        """
        if arg != 'all':
            if arg in self.database:
                experiment = self.database[arg]
                for line in experiment.as_gen():
                    yield line
                raise StopIteration
            else:
                raise IOError('No experiment named %s' % arg)
        yield "================Neroman=================\n"
        yield "\n"
        yield "================User====================\n"
        yield "Name: %s\n" % self.preferences['name']
        yield "Email: %s\n" % self.preferences['email']
        if self.preferences['default_cluster']:
            yield "Default Cluster: %s\n" % self.preferences['default_cluster']
        yield "\n"
        yield "================Clusters================\n"
        if not self.clusters['clusters']:
            yield "No clusters defined\n"
        else:
            clusters = self.clusters['clusters']
            for cluster in clusters:
                cluster_name = cluster
                cluster = clusters[cluster]
                address = cluster['ssh_address']
                type = cluster['type']
                yield "%s:\n" % cluster_name
                yield "  Address: %s\n" % address
                yield "  Type: %s\n" % type 
                for key, value in cluster.iteritems():
                    if key != 'ssh_address' and key != 'type':
                        yield "  %s: %s\n" % (key.capitalize(), value)
        yield "\n"
        yield "================Experiments=============\n"
        if not len(self.database):
            yield "No experiments defined\n"
        else:
            experiments_by_state = self._partition_by_state(self.database)
            current = ""
            for state, experiments in sorted(experiments_by_state.iteritems()):
                yield "%s:\n" % state.capitalize()
                for experiment in sorted(experiments, key=lambda e: e.id):
                    yield "  %s\n" % experiment.id

    def _partition_by_state(self, experiments):
        """Partitions the experiments in the database by state"""
        experiments_by_state = collections.defaultdict(list)
        for experiment in experiments.values():
            experiments_by_state[experiment.state].append(experiment)
        return experiments_by_state

    def submit(self, exp_id, cluster_id=""):
        """Main loop of neroman.

        Start the experiment in the cluster using ssh.

        Args:
            local_exp_path (str): the file path to experiment folder in local machine.
            experiment_destination (str): the file path to experiment folder on the remote cluster.
            experiment (str): the name of the experiment.
            cluster_address (str): the address of the cluster.
            cluster_port (int): ssh port number of the cluster.
        """
        if not cluster_id:
            cluster_id = self.preferences['default_cluster']
            
        if cluster_id not in self.clusters['clusters']:
            raise IOError('The given cluster ID or default cluster is not valid')
        
        exp = self.database[exp_id]
        # Update experiment info
        exp.cluster = cluster_id
        exp.update_state(neronet.core.Experiment.State.submitted)
        # Define local path, where experiment currently exists
        local_exp_path = exp.path
        # Define the remote path into which the files will be transferred to,
        # assuming it will be under the user's home directory
        remote_dir = neronet.core.USER_DATA_DIR
        # Define a temporary folder to contain all the required files
        local_tmp_dir = '/tmp/.neronet-%s' % (exp.id)
        # Define a folder for the files required by the experiment
        local_tmp_exp_dir = os.path.join(local_tmp_dir, 'experiments', exp.id)
        # Create the local temporary directories
        os.makedirs(local_tmp_exp_dir)
        # Define paths to required Neronet files
        neronet_root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        neronet_code_dir = os.path.join(neronet_root_dir, 'neronet')
        neronet_bin_dir = os.path.join(neronet_root_dir, 'bin')
        # Add Neronet source code files to the temporary dir
        neronet.core.osrun('rsync -az "%s" "%s"' %
                (neronet_code_dir, local_tmp_dir))
        # Second, add Neronet executables
        neronet.core.osrun('rsync -az "%s" "%s"' %
                (neronet_bin_dir, local_tmp_dir))
        # Third, add the experiment files
        for file_path in exp.required_files + [exp.main_code_file]:
            neronet.core.osrun('cp -p "%s" "%s"' %
                (os.path.join(local_exp_path, file_path), local_tmp_exp_dir))
        # Finally, serialize the experiment object into the experiment folder
        neronet.core.write_file(os.path.join(local_tmp_exp_dir, 'exp.pickle'),
                pickle.dumps(exp))
        # Read cluster address and port
        cluster = self.clusters["clusters"][cluster_id]
        cluster_address = cluster["ssh_address"]
        cluster_port = cluster["port"]
        # Transfer the files to the remote server
        neronet.core.osrun('rsync -az -e "ssh -p%s" "%s/" "%s:%s"' %
            (cluster_port,
             local_tmp_dir,
             cluster_address,
             remote_dir))
        # Remove the temporary directory
        shutil.rmtree(local_tmp_dir)
        # Find out the user's home folder in the remote machine
        #neronet.core.osrun('ssh -p%s %s echo ~' % (cluster_port, cluster_address))
        # Unless already running, start the neromum, and submit the new
        # experiment to it
        # Magic do NOT touch:
        neronet.core.osrun(
            'ssh -p%s %s "cd %s; PATH="%s/bin:/usr/local/bin:/usr/bin:/bin" PYTHONPATH="%s" neromum --start"' %
            (cluster_port, cluster_address, remote_dir, remote_dir,
             remote_dir))
        self.config_parser.save_database(DATABASE_FILENAME, \
                                        self.database)