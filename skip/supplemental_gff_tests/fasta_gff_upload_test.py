# -*- coding: utf-8 -*-
import os  # noqa: F401
import re
import shutil
import time
import unittest
from os import environ

from configparser import ConfigParser  # py3

from installed_clients.WorkspaceClient import Workspace as workspaceService
from GenomeFileUtil.GenomeFileUtilImpl import GenomeFileUtil
from GenomeFileUtil.GenomeFileUtilImpl import SDKConfig
from GenomeFileUtil.GenomeFileUtilServer import MethodContext
from GenomeFileUtil.authclient import KBaseAuth as _KBaseAuth
from GenomeFileUtil.core.FastaGFFToGenome import FastaGFFToGenome
from installed_clients.DataFileUtilClient import DataFileUtil


class FastaGFFToGenomeUploadTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.token = environ.get('KB_AUTH_TOKEN', None)
        config_file = environ.get('KB_DEPLOYMENT_CONFIG', None)
        cls.cfg = {}
        config = ConfigParser()
        config.read(config_file)  # type: ignore
        for nameval in config.items('GenomeFileUtil'):
            cls.cfg[nameval[0]] = nameval[1]
        authServiceUrl = cls.cfg.get('auth-service-url',
                                     "https://kbase.us/services/authorization/Sessions/Login")
        auth_client = _KBaseAuth(authServiceUrl)
        cls.user_id = auth_client.get_user(cls.token)
        cls.ctx = MethodContext(None)
        cls.ctx.update({'token': cls.token,
                        'user_id': cls.user_id,
                        'provenance': [
                            {'service': 'GenomeFileUtil',
                             'method': 'please_never_use_it_in_production',
                             'method_params': []
                             }],
                        'authenticated': 1})
        cls.wsURL = cls.cfg['workspace-url']
        cls.wsClient = workspaceService(cls.wsURL, token=cls.token)
        cls.serviceImpl = GenomeFileUtil(cls.cfg)
        cls.dfu = DataFileUtil(os.environ['SDK_CALLBACK_URL'], token=cls.token)
        cls.scratch = cls.cfg['scratch']
        cls.shockURL = cls.cfg['shock-url']
        cls.gfu_cfg = SDKConfig(cls.cfg)
        cls.prepare_data()

    @classmethod
    def tearDownClass(cls):
        if hasattr(cls, 'wsName'):
            cls.wsClient.delete_workspace({'workspace': cls.wsName})
            print('Test workspace was deleted')

    def getWsClient(self):
        return self.__class__.wsClient

    def getWsName(self):
        if hasattr(self.__class__, 'wsName'):
            return self.__class__.wsName
        suffix = int(time.time() * 1000)
        wsName = "test_GenomeFileUtil_" + str(suffix)
        ret = self.getWsClient().create_workspace({'workspace': wsName})  # noqa
        self.__class__.wsName = wsName
        return wsName

    def getImpl(self):
        return self.__class__.serviceImpl

    def getContext(self):
        return self.__class__.ctx

    @classmethod
    def prepare_data(cls):
        cls.importer = FastaGFFToGenome(cls.gfu_cfg)

        cls.gff_filename = 'Test_v1.0.gene.gff3.gz'
        cls.gff_path = os.path.join(cls.scratch, cls.gff_filename)
        shutil.copy(os.path.join("data", "fasta_gff", "JGI", "Plant_Data", cls.gff_filename), cls.gff_path)

        cls.fa_filename = 'Test_v1.0.fa.gz'
        cls.fa_path = os.path.join(cls.scratch, cls.fa_filename)
        shutil.copy(os.path.join("data", "fasta_gff", "JGI", "Plant_Data", cls.fa_filename), cls.fa_path)

        cls.fungal_gff_filename = 'Neucr2.filtered_proteins.BroadModels.gff3.gz'
        cls.fungal_gff_path = os.path.join(cls.scratch, cls.fungal_gff_filename)
        shutil.copy(os.path.join("data", "fasta_gff", "JGI", "Fungal_Data", cls.fungal_gff_filename),
                    cls.fungal_gff_path)

        cls.fungal_fa_filename = 'Neucr2_AssemblyScaffolds.fasta.gz'
        cls.fungal_fa_path = os.path.join(cls.scratch, cls.fungal_fa_filename)
        shutil.copy(os.path.join("data", "fasta_gff", "JGI", "Fungal_Data", cls.fungal_fa_filename),
                    cls.fungal_fa_path)

        cls.jgi_bacterial_gff_filename = '2547132501.gff.gz'
        cls.jgi_bacterial_gff_path = os.path.join(cls.scratch, cls.jgi_bacterial_gff_filename)
        shutil.copy(os.path.join("data", "fasta_gff", "JGI", "Bacterial_Data", cls.jgi_bacterial_gff_filename),
                    cls.jgi_bacterial_gff_path)      

        cls.jgi_bacterial_fa_filename = '2547132501.fna.gz'
        cls.jgi_bacterial_fa_path = os.path.join(cls.scratch, cls.jgi_bacterial_fa_filename)
        shutil.copy(os.path.join("data", "fasta_gff", "JGI", "Bacterial_Data", cls.jgi_bacterial_fa_filename),
                    cls.jgi_bacterial_fa_path)

        cls.jgi_bacterial_gff2_filename = '91705.assembled.gff'
        cls.jgi_bacterial_gff2_path = os.path.join(cls.scratch, cls.jgi_bacterial_gff2_filename)
        shutil.copy(os.path.join("data", "fasta_gff", "JGI", "Bacterial_Data", cls.jgi_bacterial_gff2_filename),
                    cls.jgi_bacterial_gff2_path)  

        cls.jgi_bacterial_fa2_filename = '91705.assembled.fna'
        cls.jgi_bacterial_fa2_path = os.path.join(cls.scratch, cls.jgi_bacterial_fa2_filename)
        shutil.copy(os.path.join("data", "fasta_gff", "JGI", "Bacterial_Data", cls.jgi_bacterial_fa2_filename),
                    cls.jgi_bacterial_fa2_path)

        cls.patric_bacterial_gff_filename = '1240778.3.PATRIC.gff.gz'
        cls.patric_bacterial_gff_path = os.path.join(cls.scratch, cls.patric_bacterial_gff_filename)
        shutil.copy(os.path.join("data", "fasta_gff", "PATRIC", "Ecoli_O104", cls.patric_bacterial_gff_filename),
                    cls.patric_bacterial_gff_path)

        cls.patric_bacterial_fa_filename = '1240778.3.fna.gz'
        cls.patric_bacterial_fa_path = os.path.join(cls.scratch, cls.patric_bacterial_fa_filename)
        shutil.copy(os.path.join("data", "fasta_gff", "PATRIC", "Ecoli_O104", cls.patric_bacterial_fa_filename),
                    cls.patric_bacterial_fa_path)

        cls.refseq_bacterial_gff_filename = 'NC_021490.gff.gz'
        cls.refseq_bacterial_gff_path = os.path.join(cls.scratch, cls.refseq_bacterial_gff_filename)
        shutil.copy(os.path.join("data", "fasta_gff", "RefSeq", "Bacterial_Data", cls.refseq_bacterial_gff_filename),
                    cls.refseq_bacterial_gff_path)

        cls.refseq_bacterial_fa_filename = 'NC_021490.fasta.gz'
        cls.refseq_bacterial_fa_path = os.path.join(cls.scratch, cls.refseq_bacterial_fa_filename)
        shutil.copy(os.path.join("data", "fasta_gff", "RefSeq", "Bacterial_Data", cls.refseq_bacterial_fa_filename),
                    cls.refseq_bacterial_fa_path)

    def check_minimal_items_exist(self, result):

        self.assertTrue('genome_info' in result)
        self.assertTrue('genome_ref' in result)

        genome_info = result['genome_info']
        self.assertEqual(genome_info[10]['Domain'], 'Unknown')
        self.assertEqual(genome_info[10]['Genetic code'], '11')
        self.assertEqual(genome_info[10]['Name'], 'unknown_taxon')
        self.assertEqual(genome_info[10]['Source'], 'Genbank')
        self.assertTrue('GC content' in genome_info[10])
        self.assertTrue(re.match("^\d+?\.\d+?$", genome_info[10]['GC content']) is not None)
        self.assertTrue('Number of Protein Encoding Genes' in genome_info[10])
        self.assertTrue(genome_info[10]['Number of Protein Encoding Genes'].isdigit())
        self.assertTrue('Size' in genome_info[10])
        self.assertTrue(genome_info[10]['Size'].isdigit())
        self.assertEqual(genome_info[10]['Taxonomy'], 'Unconfirmed Organism: unknown_taxon')

    def print_genome_warnings(self, result):
        data_file_cli = DataFileUtil(os.environ['SDK_CALLBACK_URL'])
        genome = data_file_cli.get_objects(
            {'object_refs': [result['genome_ref']]}
        )['data'][0]['data']
        if 'warnings' in genome:
            print("Genome warnings:" + str(genome['warnings']))

    def check_CDS_warnings(self, result, test_name):
        data_file_cli = DataFileUtil(os.environ['SDK_CALLBACK_URL'])
        genome = data_file_cli.get_objects(
            {'object_refs': [result['genome_ref']]}
        )['data'][0]['data']
        print("IN TEST NAME : " + str(test_name))
        cds_warning_count = 0
        cds_with_warning_count = 0
        if 'cdss' in genome:
            total_cds_count = len(genome['cdss'])
            for feature in genome['cdss']:
                if 'warnings' in feature:
                    if test_name == "test_jgi_bacterial_fasta_gff2_to_genome":
                        print(str(feature['id']) + " warnings:" + str(feature['warnings']))
                        print("Location: " + str(feature['location']))
                        print("Translation: " + feature['protein_translation'])
                        print("DNA Sequence: " + feature["dna_sequence"])
                    cds_with_warning_count = cds_with_warning_count + 1
                    cds_warning_count = cds_warning_count + len(feature['warnings'])

            print("Total CDS: " + str(total_cds_count))
            print("CDS Warning Count: " + str(cds_warning_count))
            print("CDSs with a warning Count: " + str(cds_with_warning_count))
            print("Percent CDS with warning: " + str((cds_with_warning_count/float(total_cds_count)) * 100))
    """
    def test_simple_fasta_gff_to_genome_w_null_params(self):

        input_params = {
            "fasta_file": {'path': self.fa_path},
            "gff_file": {'path': self.gff_path},
            "workspace_name": self.getWsName(),
            "genome_name": 'MyGenome',
            "scientific_name": None,
            "taxon_reference": None,
            "genetic_code": None,
            "source": None,
            "taxon_wsname": None,
            "release": None,
            "type": None
        }

        result = self.getImpl().fasta_gff_to_genome(self.getContext(), input_params)[0]

        self.assertTrue('genome_info' in result)
        self.assertTrue('genome_ref' in result)

        genome_info = result['genome_info']
        self.assertEqual(genome_info[10]['Domain'], 'Unknown')
        self.assertEqual(genome_info[10]['Genetic code'], '11')
        self.assertEqual(genome_info[10]['Name'], 'unknown_taxon')
        self.assertEqual(genome_info[10]['Source'], 'User')
        self.assertTrue('GC content' in genome_info[10])
        self.assertTrue(re.match("^\d+?\.\d+?$", genome_info[10]['GC content']) is not None)
        self.assertTrue('Number of Protein Encoding Genes' in genome_info[10])
        self.assertTrue(genome_info[10]['Number of Protein Encoding Genes'].isdigit())
        self.assertTrue('Size' in genome_info[10])
        self.assertTrue(genome_info[10]['Size'].isdigit())
        self.assertEqual(genome_info[10]['Taxonomy'], 'Unconfirmed Organism: unknown_taxon')

    def test_simple_fasta_gff_to_genome(self):
        input_params = {
            'fasta_file': {'path': self.fa_path},
            'gff_file': {'path': self.gff_path},
            'genome_name': 'Plant',
            'workspace_name': self.getWsName(),
            'source': 'Genbank',
            'type': 'Reference',
            'scientific_name': 'Populus trichocarpa'
        }

        result = self.getImpl().fasta_gff_to_genome(self.getContext(), input_params)[0]

        self.assertTrue('genome_info' in result)
        self.assertTrue('genome_ref' in result)

        genome_info = result['genome_info']
        self.assertEqual(genome_info[10]['Number of Protein Encoding Genes'], '1028')
        self.assertEqual(genome_info[10]['Domain'], 'Eukaryota')
        self.assertEqual(genome_info[10]['Genetic code'], '11')
        self.assertEqual(genome_info[10]['Name'], 'Populus trichocarpa')
        self.assertEqual(genome_info[10]['Source'], 'Genbank')
        self.assertTrue('GC content' in genome_info[10])
        self.assertTrue(re.match("^\d+?\.\d+?$", genome_info[10]['GC content']) is not None)
        self.assertTrue('Number of Protein Encoding Genes' in genome_info[10])
        self.assertTrue(genome_info[10]['Number of Protein Encoding Genes'].isdigit())
        self.assertTrue('Size' in genome_info[10])
        self.assertTrue(genome_info[10]['Size'].isdigit())
        self.assertEqual(genome_info[10]['Taxonomy'],
                          'cellular organisms; Eukaryota; Viridiplantae; Streptophyta; ' +
                          'Streptophytina; Embryophyta; Tracheophyta; Euphyllophyta; ' +
                          'Spermatophyta; Magnoliophyta; Mesangiospermae; eudicotyledons; ' +
                          'Gunneridae; Pentapetalae; rosids; fabids; Malpighiales; Salicaceae; ' +
                          'Saliceae; Populus')

    def test_taxon_reference_fasta_gff_to_genome(self):
        taxon_wsname = 'ReferenceTaxons'
        taxon_object_name = "unknown_taxon"
        taxon_info = self.dfu.get_objects({'object_refs': [taxon_wsname+"/"+taxon_object_name],
                                           'ignore_errors': 0})['data'][0]
        taxon_reference = "{}/{}/{}".format(taxon_info['info'][6],
                                            taxon_info['info'][0],
                                            taxon_info['info'][4])

        input_params = {
            'fasta_file': {'path': self.fa_path},
            'gff_file': {'path': self.gff_path},
            'genome_name': 'MyGenome',
            'workspace_name': self.getWsName(),
            'source': 'Genbank',
            'taxon_reference': taxon_reference,
            'type': 'Reference',
            'genetic_code': 1
        }

        result = self.getImpl().fasta_gff_to_genome(self.getContext(), input_params)[0]

        self.assertEqual(result['genome_info'][10]['Genetic code'], '1')
        self.check_CDS_warnings(result,"test_taxon_reference_fasta_gff_to_genome")

    def test_shock_fasta_gff_to_genome(self):
        gff_shock_id = self.dfu.file_to_shock({'file_path': self.gff_path})['shock_id']
        fa_shock_id = self.dfu.file_to_shock({'file_path': self.fa_path})['shock_id']

        input_params = {
            'workspace_name': self.getWsName(),
            'genome_name': 'MyGenome',
            'fasta_file': {'shock_id': fa_shock_id},
            'gff_file': {'shock_id': gff_shock_id},
            'source': 'Genbank',
            'type': 'Reference'
        }

        result = self.getImpl().fasta_gff_to_genome(self.getContext(), input_params)[0]

        self.check_minimal_items_exist(result)
        self.check_CDS_warnings(result,"test_shock_fasta_gff_to_genome")

    def test_fungal_fasta_gff_to_genome(self):
        input_params = {
            'workspace_name': self.getWsName(),
            'genome_name': 'jgi_fungal',
            'fasta_file': {'path': self.fungal_fa_path},
            'gff_file': {'path': self.fungal_gff_path},
            'source': 'Genbank',
            'type': 'Reference'
        }

        result = self.getImpl().fasta_gff_to_genome(self.getContext(), input_params)[0]

        self.check_minimal_items_exist(result)
        self.check_CDS_warnings(result,"test_fungal_fasta_gff_to_genome")

    def test_jgi_bacterial_fasta_gff_to_genome(self):
        input_params = {
            'workspace_name': self.getWsName(),
            'genome_name': 'jgi_bacterial',
            'fasta_file': {'path': self.jgi_bacterial_fa_path},
            'gff_file': {'path': self.jgi_bacterial_gff_path},
            'source': 'Genbank',
            'type': 'Reference',
            'generate_missing_genes': 1
        }

        result = self.getImpl().fasta_gff_to_genome(self.getContext(), input_params)[0]

        self.check_minimal_items_exist(result)
        self.check_CDS_warnings(result,"test_jgi_bacterial_fasta_gff_to_genome")

    def test_jgi_bacterial_fasta_gff2_to_genome(self):
        input_params = {
            'workspace_name': self.getWsName(),
            'genome_name': 'jgi_bacterial2',
            'fasta_file': {'path': self.jgi_bacterial_fa2_path},
            'gff_file': {'path': self.jgi_bacterial_gff2_path},
            'source': 'Genbank',
            'type': 'Reference',
            'generate_missing_genes': 1
        }

        result = self.getImpl().fasta_gff_to_genome(self.getContext(), input_params)[0]

        self.check_minimal_items_exist(result)
        self.check_CDS_warnings(result,"test_jgi_bacterial_fasta_gff2_to_genome")

    def test_refseq_bacterial_fasta_gff_to_genome(self):
        input_params = {
            'workspace_name': self.getWsName(),
            'genome_name': 'refseq',
            'fasta_file': {'path': self.refseq_bacterial_fa_path},
            'gff_file': {'path': self.refseq_bacterial_gff_path},
            'source': 'Genbank',
            'type': 'Reference'
        }

        result = self.getImpl().fasta_gff_to_genome(self.getContext(), input_params)[0]

        self.check_minimal_items_exist(result)
        self.check_CDS_warnings(result,"test_refseq_bacterial_fasta_gff_to_genome")

    def test_patric_bacterial_fasta_gff_to_genome(self):
        input_params = {
            'workspace_name': self.getWsName(),
            'genome_name': 'patric_bacterial',
            'fasta_file': {'path': self.patric_bacterial_fa_path},
            'gff_file': {'path': self.patric_bacterial_gff_path},
            'source': 'Genbank',
            'type': 'Reference',
            'generate_missing_genes': 1
        }

        result = self.getImpl().fasta_gff_to_genome(self.getContext(), input_params)[0]

        self.check_minimal_items_exist(result)
        self.check_CDS_warnings(result,"test_patric_bacterial_fasta_gff_to_genome")"""

    def test_bad_fasta_gff_to_genome_params(self):
        invalidate_input_params = {
          'missing_workspace_name': 'workspace_name',
          'genome_name': 'genome_name',
          'fasta_file': {'path': 'fasta_file'},
          'gff_file': {'path': 'gff_file'}
        }
        with self.assertRaisesRegex(
                    ValueError,
                    '"workspace_name" parameter is required, but missing'):
            self.getImpl().fasta_gff_to_genome(self.getContext(), invalidate_input_params)

        invalidate_input_params = {
          'workspace_name': 'workspace_name',
          'missing_genome_name': 'genome_name',
          'fasta_file': {'path': 'fasta_file'},
          'gff_file': {'path': 'gff_file'}
        }
        with self.assertRaisesRegex(
                    ValueError,
                    '"genome_name" parameter is required, but missing'):
            self.getImpl().fasta_gff_to_genome(self.getContext(), invalidate_input_params)

        invalidate_input_params = {
          'workspace_name': 'workspace_name',
          'genome_name': 'genome_name',
          'missing_fasta_file': {'path': 'fasta_file'},
          'gff_file': {'path': 'gff_file'}
        }
        with self.assertRaisesRegex(
                ValueError,
                '"fasta_file" parameter is required, but missing'):
            self.getImpl().fasta_gff_to_genome(self.getContext(), invalidate_input_params)

        invalidate_input_params = {
          'workspace_name': 'workspace_name',
          'genome_name': 'genome_name',
          'fasta_file': {'path': 'fasta_file'},
          'missing_gff_file': {'path': 'gff_file'}
        }
        with self.assertRaisesRegex(
                ValueError,
                '"gff_file" parameter is required, but missing'):
            self.getImpl().fasta_gff_to_genome(self.getContext(), invalidate_input_params)

        invalidate_input_params = {
          'workspace_name': 'workspace_name',
          'genome_name': 'genome_name',
          'fasta_file': 'not_a_dict',
          'gff_file': {'path': 'gff_file'}
        }
        with self.assertRaisesRegex(
                ValueError,
                'Required "fasta_file" field must be a map/dict'):
            self.getImpl().fasta_gff_to_genome(self.getContext(), invalidate_input_params)

        invalidate_input_params = {
          'workspace_name': 'workspace_name',
          'genome_name': 'genome_name',
          'fasta_file': {'path': 'fasta_file'},
          'gff_file': 'not_a_dict'
        }
        with self.assertRaisesRegex(
                ValueError,
                'Required "gff_file" field must be a map/dict'):
            self.getImpl().fasta_gff_to_genome(self.getContext(), invalidate_input_params)

        invalidate_input_params = {
          'workspace_name': 'workspace_name',
          'genome_name': 'genome_name',
          'fasta_file': {'path': 'fasta_file'},
          'gff_file': {'ftp_url': 'gff_file'}
        }
        with self.assertRaisesRegex(
                ValueError,
                'must include one source'):
            self.getImpl().fasta_gff_to_genome(self.getContext(), invalidate_input_params)

        invalidate_input_params = {
          'workspace_name': 'workspace_name',
          'genome_name': 'genome_name',
          'fasta_file': {'missing_path': 'fasta_file'},
          'gff_file': {'path': 'gff_file'}
        }
        with self.assertRaisesRegex(
                ValueError,
                'Required "fasta_file" field must include one source: path | shock_id'):
            self.getImpl().fasta_gff_to_genome(self.getContext(), invalidate_input_params)

        invalidate_input_params = {
          'workspace_name': 'workspace_name',
          'genome_name': 'genome_name',
          'fasta_file': {'path': 'fasta_file', 'shock_id': 'shock_id'},
          'gff_file': {'path': 'gff_file'}
        }
        with self.assertRaisesRegex(
                ValueError,
                'Required "fasta_file" field has too many sources specified: '):
            self.getImpl().fasta_gff_to_genome(self.getContext(), invalidate_input_params)

        invalidate_input_params = {
            'workspace_name': 'workspace_name',
            'genome_name': 'genome_name',
            'fasta_file': {'path': 'fasta_file'},
            'gff_file': {'path': 'gff_file'},
            'genetic_code': 'meh'
        }
        with self.assertRaisesRegex(
                ValueError,
                'Invalid genetic code specified'):
            self.getImpl().fasta_gff_to_genome(self.getContext(), invalidate_input_params)

        invalidate_input_params = {
            'workspace_name': self.getWsName(),
            'genome_name': 'MyGenome',
            'fasta_file': {'path': self.patric_bacterial_fa_path},
            'gff_file': {'path': self.patric_bacterial_gff_path},
            'source': 'Genbank',
            'type': 'Reference',
        }
        with self.assertRaisesRegex(
                ValueError, "generate_missing_genes"):
            self.getImpl().fasta_gff_to_genome(self.getContext(),
                                               invalidate_input_params)
    """
    def test_FastaGFFToGenome_stage_input(self):
        # test absolute file path
        input_params = {
            'workspace_name': self.getWsName(),
            'genome_name': 'MyGenome',
            'fasta_file': {'path': self.fa_path},
            'gff_file': {'path': self.gff_path},
        }

        input_directory = os.path.join(self.scratch, 'test_FastaGFFToGenome_stage_input')
        os.makedirs(input_directory)

        file_paths = self.importer._stage_input(input_params, input_directory)

        self.assertTrue(self.gff_filename.rpartition('.')[0] in os.listdir(input_directory))
        self.assertTrue(self.fa_filename.rpartition('.')[0] in os.listdir(input_directory))
        self.assertTrue('gff_file' in file_paths)
        self.assertTrue('fasta_file' in file_paths)
        self.assertEqual(file_paths.get('gff_file'),
                          os.path.join(input_directory, self.gff_filename).rpartition('.')[0])
        self.assertEqual(file_paths.get('fasta_file'),
                          os.path.join(input_directory, self.fa_filename).rpartition('.')[0])

        # test shock id
        gff_shock_id = self.dfu.file_to_shock({'file_path': self.gff_path})['shock_id']
        fa_shock_id = self.dfu.file_to_shock({'file_path': self.fa_path})['shock_id']

        input_params = {
            'workspace_name': self.getWsName(),
            'genome_name': 'MyGenome',
            'fasta_file': {'shock_id': fa_shock_id},
            'gff_file': {'shock_id': gff_shock_id},
        }
        shutil.rmtree(input_directory)
        os.makedirs(input_directory)

        file_paths = self.importer._stage_input(input_params, input_directory)

        self.assertTrue(self.gff_filename.rpartition('.')[0] in os.listdir(input_directory))
        self.assertTrue(self.fa_filename.rpartition('.')[0] in os.listdir(input_directory))
        self.assertTrue('gff_file' in file_paths)
        self.assertTrue('fasta_file' in file_paths)
        self.assertEqual(file_paths.get('gff_file'),
                          os.path.join(input_directory, self.gff_filename).rpartition('.')[0])
        self.assertEqual(file_paths.get('fasta_file'),
                          os.path.join(input_directory, self.fa_filename).rpartition('.')[0])

    def test_FastaGFFToGenome_set_parsed_params(self):
        input_params = {
            'workspace_name': self.getWsName(),
            'genome_name': 'MyGenome',
            'fasta_file': {'path': self.fa_path},
            'gff_file': {'path': self.gff_path},
            'source': 'Genbank',
            'type': 'Reference'
        }

        parsed_params = self.importer._set_parsed_params(input_params)

        expect_param_keys = {'source', 'taxon_wsname', 'taxon_reference', 'release',
                             'type', 'metadata', 'workspace_name', 'source_id',
                             'genome_name', 'scientific_name', 'gff_file', 'fasta_file'}
        self.assertEqual(set(parsed_params.keys()), expect_param_keys)
        self.assertEqual(parsed_params['genome_name'], 'MyGenome')
        self.assertEqual(parsed_params['source'], 'Genbank')
        self.assertEqual(parsed_params['type'], 'Reference')

    def test_FastaGFFToGenome_retrieve_gff_file(self):

        input_gff_file = self.dfu.unpack_file({'file_path': self.gff_path})['file_path']

        feature_list = self.importer._retrieve_gff_file(input_gff_file)

        self.assertIsInstance(feature_list, dict)

    def test_update_phytozome(self):

        features_identifiers_list = {'Chr01': [{'end': 8201443,
                                                'Name': 'Potri.001G102800',
                                                'start': 8200895,
                                                'score': '.',
                                                'phase': '.',
                                                'contig': 'Chr01',
                                                'type': 'gene',
                                                'ID': 'Potri.001G102800.v3.0',
                                                'strand': '-'},
                                               {'end': 8201443,
                                                'Name': 'Potri.001G102800.1',
                                                'Parent': 'Potri.001G102800.v3.0',
                                                'pacid': '27047128',
                                                'start': 8200895,
                                                'score': '.',
                                                'longest': '1',
                                                'phase': '.',
                                                'contig': 'Chr01',
                                                'type': 'mRNA',
                                                'ID': 'Potri.001G102800.1.v3.0',
                                                'strand': '-'},
                                               {'end': 8201443,
                                                'Parent': 'Potri.001G102800.1.v3.0',
                                                'pacid': '27047128',
                                                'start': 8200895,
                                                'score': '.',
                                                'phase': '0',
                                                'contig': 'Chr01',
                                                'type': 'CDS',
                                                'ID': 'Potri.001G102800.1.v3.0.CDS.1',
                                                'strand': '-'}]}
        updated_features_list = self.importer._update_identifiers(
            features_identifiers_list)
        self.assertEqual(updated_features_list['Chr01'][-1]['ID'],
                         'Potri.001G102800.1.v3.0.CDS')

    def test_FastaGFFToGenome_update_feature_identifiers(self):

        features_identifiers_list = {'Chr01':[{'end': 8201443,
                                      'Name': 'Potri.001G102800',
                                      'start': 8200895,
                                      'score': '.',
                                      'phase': '.',
                                      'contig': 'Chr01',
                                      'type': 'gene',
                                      'ID': 'Potri.001G102800.v3.0',
                                      'strand': '-'},
                                     {'end': 8201443,
                                      'Name': 'Potri.001G102800.1',
                                      'Parent': 'Potri.001G102800.v3.0',
                                      'pacid': '27047128',
                                      'start': 8200895,
                                      'score': '.',
                                      'longest': '1',
                                      'phase': '.',
                                      'contig': 'Chr01',
                                      'type': 'mRNA',
                                      'ID': 'Potri.001G102800.1.v3.0',
                                      'strand': '-'},
                                     {'end': 8201443,
                                      'Parent': 'Potri.001G102800.1.v3.0',
                                      'pacid': '27047128',
                                      'start': 8200895,
                                      'score': '.',
                                      'phase': '0',
                                      'contig': 'Chr01',
                                      'type': 'CDS',
                                      'ID': 'Potri.001G102800.1.v3.0.CDS',
                                      'strand': '-'}]}

        updated_features_list = self.importer._update_identifiers(features_identifiers_list)
        self.assertEqual(updated_features_list, features_identifiers_list)"""
