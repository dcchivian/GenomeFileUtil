import unittest
import os
import time
from uuid import uuid4
from configparser import ConfigParser

from GenomeFileUtil.GenomeFileUtilServer import MethodContext
from GenomeFileUtil.GenomeFileUtilImpl import GenomeFileUtil
from installed_clients.WorkspaceClient import Workspace

_DATA_PATH = "/kb/module/test/data"


class IntegrationTest(unittest.TestCase):
    """
    Basic integration tests on a small genome.
    """

    @classmethod
    def setUpClass(cls):
        token = os.environ.get('KB_AUTH_TOKEN', None)
        # WARNING: don't call any logging methods on the context object,
        # it'll result in a NoneType error
        cls.ctx = MethodContext(None)
        cls.ctx.update({'token': token,
                        'provenance': [
                            {'service': 'GenomeFileUtil',
                             'method': 'please_never_use_it_in_production',
                             'method_params': []
                             }],
                        'authenticated': 1})
        config_file = os.environ.get('KB_DEPLOYMENT_CONFIG', None)
        cls.cfg = {}
        config = ConfigParser()
        config.read(config_file)  # type: ignore
        for nameval in config.items('GenomeFileUtil'):
            cls.cfg[nameval[0]] = nameval[1]
        cls.wsURL = cls.cfg['workspace-url']
        cls.ws = Workspace(cls.wsURL, token=token)
        cls.gfu = GenomeFileUtil(cls.cfg)
        # create one WS for all tests
        suffix = int(time.time() * 1000)
        cls.ws_name = "test_GenomeAnnotationAPI_" + str(suffix)
        ws_info = cls.ws.create_workspace({'workspace': cls.ws_name})
        cls.ws_id = ws_info[0]

    def test_genbank_to_genome_taxonomy(self):
        """
        Test the `save_one_genome` method.
        Pass a taxon ID in the parameters.
        """
        result = self.gfu.genbank_to_genome(self.ctx, {
            'workspace_name': self.ws_name,
            'generate_ids_if_needed': 'true',  # why is this a string
            'taxon_id': '3702',
            'file': {
                'path': f"{_DATA_PATH}/wigglesworthia/genome.gb"
            },
            'genome_name': str(uuid4()),
        })
        ('result', result)
        ref = result[0]['genome_ref']
        self.assertTrue(ref, 'Genome ref exists')
        info = result[0]['genome_info']
        typ = info[2]
        self.assertTrue(typ.startswith('KBaseGenomes.Genome'))
        info_details = info[-1]
        self.assertEqual(info_details['Taxonomy'], (
            "cellular organisms;Eukaryota;Viridiplantae;"
            "Streptophyta;Streptophytina;Embryophyta;Tracheophyta;"
            "Euphyllophyta;Spermatophyta;Magnoliopsida;Mesangiospermae;"
            "eudicotyledons;Gunneridae;Pentapetalae;rosids;malvids;"
            "Brassicales;Brassicaceae;Camelineae;Arabidopsis"
        ))
        self.assertEqual(info_details['Size'], '697724')
        self.assertEqual(info_details['Source'], 'Genbank')
        self.assertEqual(info_details['Name'], 'Wigglesworthia glossinidia endosymbiont of Glossina brevipalpis')
        self.assertEqual(info_details['GC content'], '0.22479')
        self.assertEqual(info_details['Genetic code'], '11')
        self.assertEqual(info_details['Number of Genome Level Warnings'], '1')
        self.assertEqual(info_details['Source ID'], 'BA000021')
        self.assertEqual(info_details['Number of Protein Encoding Genes'], '20')
        self.assertEqual(info_details['Domain'], 'Eukaryota')
        self.assertTrue(info_details['Assembly Object'])
        self.assertEqual(info_details['Number contigs'], '1')
        self.assertEqual(info_details['Number of CDS'], '20')
        self.assertTrue(info_details['MD5'])

    @unittest.skip('TODO')
    def test_genbank_to_genome_invalid_taxon_id(self):
        """
        Test the `save_one_genome` method.
        Pass a taxon ID in the parameters.
        """
        result = self.gfu.genbank_to_genome(self.ctx, {
            'workspace_name': self.ws_name,
            'generate_ids_if_needed': 'true',  # why is this a string
            'taxon_id': '9999999999',
            'file': {
                'path': f"{_DATA_PATH}/wigglesworthia/genome.gb"
            },
            'genome_name': str(uuid4()),
        })
        print('test_genbank_to_genome_invalid_taxon_id result', result)
