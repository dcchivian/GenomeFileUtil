# -*- coding: utf-8 -*-
#BEGIN_HEADER

import json
import logging
import os
import shutil
from pprint import pprint

from GenomeFileUtil.core.FastaGFFToGenome import FastaGFFToGenome
from GenomeFileUtil.core.GenbankToGenome import GenbankToGenome
from GenomeFileUtil.core.GenomeFeaturesToFasta import GenomeFeaturesToFasta
from GenomeFileUtil.core.GenomeInterface import GenomeInterface
from GenomeFileUtil.core.GenomeToGFF import GenomeToGFF
from GenomeFileUtil.core.GenomeToGenbank import GenomeToGenbank
from installed_clients.AssemblyUtilClient import AssemblyUtil
from installed_clients.DataFileUtilClient import DataFileUtil
from installed_clients.WorkspaceClient import Workspace


# Used to store and pass around configuration URLs more easily
class SDKConfig:
    def __init__(self, config):
        self.workspaceURL = config['workspace-url']
        self.shockURL = config['shock-url']
        self.handleURL = config['handle-service-url']
        self.callbackURL = os.environ['SDK_CALLBACK_URL']
        self.sharedFolder = config['scratch']
        self.srvWizURL = config['srv-wiz-url']
        self.token = os.environ['KB_AUTH_TOKEN']
        self.authServiceUrl = config['auth-service-url']
        self.re_api_url = config['re-api-url']
        self.raw = config

#END_HEADER


class GenomeFileUtil:
    '''
    Module Name:
    GenomeFileUtil

    Module Description:

    '''

    ######## WARNING FOR GEVENT USERS ####### noqa
    # Since asynchronous IO can lead to methods - even the same method -
    # interrupting each other, you must be *very* careful when using global
    # state. A method could easily clobber the state set by another while
    # the latter method is running.
    ######################################### noqa
    VERSION = "0.8.14"
    GIT_URL = "https://github.com/kbaseapps/GenomeFileUtil"
    GIT_COMMIT_HASH = "97a0c33e1e85c5c3351638513e1a5b324d8e5e93"

    #BEGIN_CLASS_HEADER
    #END_CLASS_HEADER

    # config contains contents of config file in a hash or None if it couldn't
    # be found
    def __init__(self, config):
        #BEGIN_CONSTRUCTOR
        self.cfg = SDKConfig(config)
        logging.basicConfig(format='%(created)s %(levelname)s: %(message)s',
                            level=logging.INFO)
        #END_CONSTRUCTOR
        pass


    def genbank_to_genome(self, ctx, params):
        """
        :param params: instance of type "GenbankToGenomeParams" (genome_name
           - becomes the name of the object workspace_name - the name of the
           workspace it gets saved to. source - Source of the file typically
           something like RefSeq or Ensembl taxon_ws_name - where the
           reference taxons are : ReferenceTaxons taxon_id - if defined, will
           try to link the Genome to the specified taxonomy id in lieu of
           performing the lookup during upload release - Release or version
           number of the data per example Ensembl has numbered releases of
           all their data: Release 31 generate_ids_if_needed - If field used
           for feature id is not there, generate ids (default behavior is
           raising an exception) genetic_code - Genetic code of organism.
           Overwrites determined GC from taxon object scientific_name - will
           be used to set the scientific name of the genome and link to a
           taxon generate_missing_genes - If the file has CDS or mRNA with no
           corresponding gene, generate a spoofed gene. use_existing_assembly
           - Supply an existing assembly reference) -> structure: parameter
           "file" of type "File" -> structure: parameter "path" of String,
           parameter "shock_id" of String, parameter "ftp_url" of String,
           parameter "genome_name" of String, parameter "workspace_name" of
           String, parameter "source" of String, parameter "taxon_wsname" of
           String, parameter "taxon_id" of String, parameter "release" of
           String, parameter "generate_ids_if_needed" of String, parameter
           "genetic_code" of Long, parameter "scientific_name" of String,
           parameter "metadata" of type "usermeta" -> mapping from String to
           String, parameter "generate_missing_genes" of type "boolean" (A
           boolean - 0 for false, 1 for true. @range (0, 1)), parameter
           "use_existing_assembly" of String
        :returns: instance of type "GenomeSaveResult" -> structure: parameter
           "genome_ref" of String
        """
        # ctx is the context object
        # return variables are: result
        #BEGIN genbank_to_genome
        print('genbank_to_genome -- paramaters = ')
        pprint(params)

        importer = GenbankToGenome(self.cfg)
        result = importer.refactored_import(ctx, params)

        print('import complete -- result = ')
        pprint(result)
        #END genbank_to_genome

        # At some point might do deeper type checking...
        if not isinstance(result, dict):
            raise ValueError('Method genbank_to_genome return value ' +
                             'result is not type dict as required.')
        # return the results
        return [result]

    def genome_to_gff(self, ctx, params):
        """
        :param params: instance of type "GenomeToGFFParams" (is_gtf -
           optional flag switching export to GTF format (default is 0, which
           means GFF) target_dir - optional target directory to create file
           in (default is temporary folder with name 'gff_<timestamp>'
           created in scratch)) -> structure: parameter "genome_ref" of
           String, parameter "ref_path_to_genome" of list of String,
           parameter "is_gtf" of type "boolean" (A boolean - 0 for false, 1
           for true. @range (0, 1)), parameter "target_dir" of String
        :returns: instance of type "GenomeToGFFResult" (from_cache is 1 if
           the file already exists and was just returned, 0 if the file was
           generated during this call.) -> structure: parameter "file_path"
           of String, parameter "from_cache" of type "boolean" (A boolean - 0
           for false, 1 for true. @range (0, 1))
        """
        # ctx is the context object
        # return variables are: result
        #BEGIN genome_to_gff
        print('genome_to_gff -- paramaters = ')
        pprint(params)

        exporter = GenomeToGFF(self.cfg)
        result = exporter.export(ctx, params)

        print('export complete -- result = ')
        pprint(result)
        #END genome_to_gff

        # At some point might do deeper type checking...
        if not isinstance(result, dict):
            raise ValueError('Method genome_to_gff return value ' +
                             'result is not type dict as required.')
        # return the results
        return [result]

    def metagenome_to_gff(self, ctx, params):
        """
        :param params: instance of type "MetagenomeToGFFParams" (is_gtf -
           optional flag switching export to GTF format (default is 0, which
           means GFF) target_dir - optional target directory to create file
           in (default is temporary folder with name 'gff_<timestamp>'
           created in scratch)) -> structure: parameter "genome_ref" of
           String, parameter "ref_path_to_genome" of list of String,
           parameter "is_gtf" of type "boolean" (A boolean - 0 for false, 1
           for true. @range (0, 1)), parameter "target_dir" of String
        :returns: instance of type "MetagenomeToGFFResult" -> structure:
           parameter "file_path" of String, parameter "from_cache" of type
           "boolean" (A boolean - 0 for false, 1 for true. @range (0, 1))
        """
        # ctx is the context object
        # return variables are: result
        #BEGIN metagenome_to_gff
        print('metagenome_to_gff -- paramaters = ')
        pprint(params)

        exporter = GenomeToGFF(self.cfg)
        result = exporter.export(ctx, params)

        print('export complete -- result = ')
        pprint(result)
        #END metagenome_to_gff

        # At some point might do deeper type checking...
        if not isinstance(result, dict):
            raise ValueError('Method metagenome_to_gff return value ' +
                             'result is not type dict as required.')
        # return the results
        return [result]

    def genome_to_genbank(self, ctx, params):
        """
        :param params: instance of type "GenomeToGenbankParams" -> structure:
           parameter "genome_ref" of String, parameter "ref_path_to_genome"
           of list of String
        :returns: instance of type "GenomeToGenbankResult" (from_cache is 1
           if the file already exists and was just returned, 0 if the file
           was generated during this call.) -> structure: parameter
           "genbank_file" of type "GBFile" -> structure: parameter
           "file_path" of String, parameter "from_cache" of type "boolean" (A
           boolean - 0 for false, 1 for true. @range (0, 1))
        """
        # ctx is the context object
        # return variables are: result
        #BEGIN genome_to_genbank
        print('genome_to_genbank -- paramaters = ')
        pprint(params)

        exporter = GenomeToGenbank(self.cfg)
        result = exporter.export(ctx, params)

        print('export complete -- result = ')
        pprint(result)
        #END genome_to_genbank

        # At some point might do deeper type checking...
        if not isinstance(result, dict):
            raise ValueError('Method genome_to_genbank return value ' +
                             'result is not type dict as required.')
        # return the results
        return [result]

    def genome_features_to_fasta(self, ctx, params):
        """
        :param params: instance of type "GenomeFeaturesToFastaParams"
           (Produce a FASTA file with the nucleotide sequences of features in
           a genome. string genome_ref: reference to a genome object
           list<string> feature_lists: Optional, which features lists
           (features, mrnas, cdss, non_coding_features) to provide sequences.
           Defaults to "features". list<string> filter_ids: Optional, if
           provided only return sequences for matching features. boolean
           include_functions: Optional, add function to header line. Defaults
           to True. boolean include_aliases: Optional, add aliases to header
           line. Defaults to True.) -> structure: parameter "genome_ref" of
           String, parameter "feature_lists" of list of String, parameter
           "filter_ids" of list of String, parameter "include_functions" of
           type "boolean" (A boolean - 0 for false, 1 for true. @range (0,
           1)), parameter "include_aliases" of type "boolean" (A boolean - 0
           for false, 1 for true. @range (0, 1))
        :returns: instance of type "FASTAResult" -> structure: parameter
           "file_path" of String
        """
        # ctx is the context object
        # return variables are: result
        #BEGIN genome_features_to_fasta
        logging.info(f"Running genome_features_to_fasta with the following params: {params}")
        exporter = GenomeFeaturesToFasta(self.cfg)
        result = exporter.export(ctx, params, protein=False)
        #END genome_features_to_fasta

        # At some point might do deeper type checking...
        if not isinstance(result, dict):
            raise ValueError('Method genome_features_to_fasta return value ' +
                             'result is not type dict as required.')
        # return the results
        return [result]

    def genome_proteins_to_fasta(self, ctx, params):
        """
        :param params: instance of type "GenomeProteinToFastaParams" (Produce
           a FASTA file with the protein sequences of CDSs in a genome.
           string genome_ref: reference to a genome object list<string>
           filter_ids: Optional, if provided only return sequences for
           matching features. boolean include_functions: Optional, add
           function to header line. Defaults to True. boolean
           include_aliases: Optional, add aliases to header line. Defaults to
           True.) -> structure: parameter "genome_ref" of String, parameter
           "filter_ids" of list of String, parameter "include_functions" of
           type "boolean" (A boolean - 0 for false, 1 for true. @range (0,
           1)), parameter "include_aliases" of type "boolean" (A boolean - 0
           for false, 1 for true. @range (0, 1))
        :returns: instance of type "FASTAResult" -> structure: parameter
           "file_path" of String
        """
        # ctx is the context object
        # return variables are: result
        #BEGIN genome_proteins_to_fasta
        logging.info(f"Running genome_proteins_to_fasta with the following params: {params}")
        exporter = GenomeFeaturesToFasta(self.cfg)
        result = exporter.export(ctx, params, protein=True)
        #END genome_proteins_to_fasta

        # At some point might do deeper type checking...
        if not isinstance(result, dict):
            raise ValueError('Method genome_proteins_to_fasta return value ' +
                             'result is not type dict as required.')
        # return the results
        return [result]

    def export_genome_as_genbank(self, ctx, params):
        """
        :param params: instance of type "ExportParams" (input and output
           structure functions for standard downloaders) -> structure:
           parameter "input_ref" of String
        :returns: instance of type "ExportOutput" -> structure: parameter
           "shock_id" of String
        """
        # ctx is the context object
        # return variables are: output
        #BEGIN export_genome_as_genbank
        print('export_genome_as_genbank -- paramaters = ')

        # validate parameters
        if 'input_ref' not in params:
            raise ValueError('Cannot run export_genome_as_genbank- no "input_ref" field defined.')

        # get WS metadata to get ws_name and obj_name
        ws = Workspace(url=self.cfg.workspaceURL)
        info = ws.get_object_info_new({'objects': [{'ref': params['input_ref']}],
                                       'includeMetadata': 0, 'ignoreErrors': 0})[0]

        genome_to_genbank_params = {
            'genome_ref': params['input_ref']
        }

        # export to file (building from KBase Genome Object)
        result = self.genome_to_genbank(ctx, genome_to_genbank_params)[0]['genbank_file']

        # create the output directory and move the file there
        export_package_dir = os.path.join(self.cfg.sharedFolder, info[1])
        os.makedirs(export_package_dir)
        shutil.move(
          result['file_path'],
          os.path.join(export_package_dir, os.path.basename(result['file_path'])))

        # export original uploaded GenBank file if it existed.
        exporter = GenomeToGenbank(self.cfg)
        original_result_full = exporter.export_original_genbank(ctx, genome_to_genbank_params)
        if original_result_full is not None:
            original_result = original_result_full['genbank_file']
            shutil.move(
              original_result['file_path'],
              os.path.join(export_package_dir, os.path.basename(original_result['file_path'])))

        # Make warning file about genes only.
        warning_filename = "README.txt"
        with open(os.path.join(export_package_dir, warning_filename), 'w') as temp_file:
            temp_file.write('This directory includes the KBase-derived GenBank file and also ' +
                            '(if you originally uploaded the genome from an annotated ' +
                            'GenBank file) the original GenBank input.')

        # package it up and be done
        dfUtil = DataFileUtil(self.cfg.callbackURL)
        package_details = dfUtil.package_for_download({
                                    'file_path': export_package_dir,
                                    'ws_refs': [ params['input_ref'] ]
                                })

        output = { 'shock_id': package_details['shock_id'] }

        print('export complete -- result = ')
        pprint(output)
        #END export_genome_as_genbank

        # At some point might do deeper type checking...
        if not isinstance(output, dict):
            raise ValueError('Method export_genome_as_genbank return value ' +
                             'output is not type dict as required.')
        # return the results
        return [output]

    def export_genome_as_gff(self, ctx, params):
        """
        :param params: instance of type "ExportParams" (input and output
           structure functions for standard downloaders) -> structure:
           parameter "input_ref" of String
        :returns: instance of type "ExportOutput" -> structure: parameter
           "shock_id" of String
        """
        # ctx is the context object
        # return variables are: output
        #BEGIN export_genome_as_gff
        if 'input_ref' not in params:
            raise ValueError('Cannot run export_genome_as_gff- no "input_ref" '
                             'field defined.')

        # get WS metadata to get ws_name and obj_name
        ws = Workspace(url=self.cfg.workspaceURL)
        info = ws.get_objects2({'objects': [{
            'ref': params['input_ref'],
            'included':['/assembly_ref', '/contigset_ref', '/id', '/gff_handle_ref']}
        ]})['data'][0]['data']

        # export to file (building from KBase Genome Object)
        result = self.genome_to_gff(ctx, {
            'genome_ref': params['input_ref']
        })[0]

        # get assembly
        if 'assembly_ref' in info:
            assembly_ref = info['assembly_ref']
        else:
            assembly_ref = info['contigset_ref']
        print(('Assembly reference = ' + assembly_ref))
        print('Downloading assembly')
        au = AssemblyUtil(self.cfg.callbackURL)
        assembly_file_path = au.get_assembly_as_fasta(
            {'ref': params['input_ref'] + ";" + assembly_ref}
        )['path']

        # create the output directory and move the files there
        export_package_dir = os.path.join(self.cfg.sharedFolder, info['id'])
        os.makedirs(export_package_dir)
        shutil.move(
            result['file_path'],
            os.path.join(export_package_dir,
                         'KBase_derived_' + os.path.basename(result['file_path'])))
        shutil.move(
            assembly_file_path,
            os.path.join(export_package_dir,
                         os.path.basename(assembly_file_path)))

        # add cached genome if appropriate
        exporter = GenomeToGFF(self.cfg)
        cached = exporter.get_gff_handle(info, export_package_dir)

        # package it up
        dfUtil = DataFileUtil(self.cfg.callbackURL)
        package_details = dfUtil.package_for_download({
                                    'file_path': export_package_dir,
                                    'ws_refs': [params['input_ref']]
                                })

        output = {'shock_id': package_details['shock_id']}
        #END export_genome_as_gff

        # At some point might do deeper type checking...
        if not isinstance(output, dict):
            raise ValueError('Method export_genome_as_gff return value ' +
                             'output is not type dict as required.')
        # return the results
        return [output]

    def export_genome_features_protein_to_fasta(self, ctx, params):
        """
        :param params: instance of type "ExportParams" (input and output
           structure functions for standard downloaders) -> structure:
           parameter "input_ref" of String
        :returns: instance of type "ExportOutput" -> structure: parameter
           "shock_id" of String
        """
        # ctx is the context object
        # return variables are: output
        #BEGIN export_genome_features_protein_to_fasta
        print('export_genome_features_protein_to_fasta -- paramaters = ')

        # validate parameters
        if 'input_ref' not in params:
            raise ValueError('Cannot run export_genome_features_protein_to_fasta - no "input_ref" field defined.')

        # get WS metadata to get ws_name and obj_name
        ws = Workspace(url=self.cfg.workspaceURL)
        info = ws.get_object_info_new({'objects': [{'ref': params['input_ref']}],
                                       'includeMetadata': 0, 'ignoreErrors': 0})[0]

        genome_to_protein_fasta_params = {
            'genome_ref': params['input_ref']
        }

        # export to file (building from KBase Genome Object)
        result = self.genome_to_genbank(ctx, genome_to_protein_fasta_params)[0]['genbank_file']



        #END export_genome_features_protein_to_fasta

        # At some point might do deeper type checking...
        if not isinstance(output, dict):
            raise ValueError('Method export_genome_features_protein_to_fasta return value ' +
                             'output is not type dict as required.')
        # return the results
        return [output]

    def fasta_gff_to_genome(self, ctx, params):
        """
        :param params: instance of type "FastaGFFToGenomeParams" (genome_name
           - becomes the name of the object workspace_name - the name of the
           workspace it gets saved to. source - Source of the file typically
           something like RefSeq or Ensembl taxon_ws_name - where the
           reference taxons are : ReferenceTaxons taxon_id - if defined, will
           try to link the Genome to the specified taxonomy id in lieu of
           performing the lookup during upload release - Release or version
           number of the data per example Ensembl has numbered releases of
           all their data: Release 31 genetic_code - Genetic code of
           organism. Overwrites determined GC from taxon object
           scientific_name - will be used to set the scientific name of the
           genome and link to a taxon generate_missing_genes - If the file
           has CDS or mRNA with no corresponding gene, generate a spoofed
           gene. Off by default) -> structure: parameter "fasta_file" of type
           "File" -> structure: parameter "path" of String, parameter
           "shock_id" of String, parameter "ftp_url" of String, parameter
           "gff_file" of type "File" -> structure: parameter "path" of
           String, parameter "shock_id" of String, parameter "ftp_url" of
           String, parameter "genome_name" of String, parameter
           "workspace_name" of String, parameter "source" of String,
           parameter "taxon_wsname" of String, parameter "taxon_id" of
           String, parameter "release" of String, parameter "genetic_code" of
           Long, parameter "scientific_name" of String, parameter "metadata"
           of type "usermeta" -> mapping from String to String, parameter
           "generate_missing_genes" of type "boolean" (A boolean - 0 for
           false, 1 for true. @range (0, 1))
        :returns: instance of type "GenomeSaveResult" -> structure: parameter
           "genome_ref" of String
        """
        # ctx is the context object
        # return variables are: returnVal
        #BEGIN fasta_gff_to_genome
        print('--->\nRunning GenomeFileUtil.fasta_gff_to_genome\nparams:')
        print(json.dumps(params, indent=1))

        for key in list(params.keys()):
            if params[key] is None:
                del params[key]

        for key, value in params.items():
            if isinstance(value, str):
                params[key] = value.strip()

        importer = FastaGFFToGenome(self.cfg)
        returnVal = importer.import_file(params)
        #END fasta_gff_to_genome

        # At some point might do deeper type checking...
        if not isinstance(returnVal, dict):
            raise ValueError('Method fasta_gff_to_genome return value ' +
                             'returnVal is not type dict as required.')
        # return the results
        return [returnVal]

    def fasta_gff_to_genome_json(self, ctx, params):
        """
        As above but returns the genome instead
        :param params: instance of type "FastaGFFToGenomeParams" (genome_name
           - becomes the name of the object workspace_name - the name of the
           workspace it gets saved to. source - Source of the file typically
           something like RefSeq or Ensembl taxon_ws_name - where the
           reference taxons are : ReferenceTaxons taxon_id - if defined, will
           try to link the Genome to the specified taxonomy id in lieu of
           performing the lookup during upload release - Release or version
           number of the data per example Ensembl has numbered releases of
           all their data: Release 31 genetic_code - Genetic code of
           organism. Overwrites determined GC from taxon object
           scientific_name - will be used to set the scientific name of the
           genome and link to a taxon generate_missing_genes - If the file
           has CDS or mRNA with no corresponding gene, generate a spoofed
           gene. Off by default) -> structure: parameter "fasta_file" of type
           "File" -> structure: parameter "path" of String, parameter
           "shock_id" of String, parameter "ftp_url" of String, parameter
           "gff_file" of type "File" -> structure: parameter "path" of
           String, parameter "shock_id" of String, parameter "ftp_url" of
           String, parameter "genome_name" of String, parameter
           "workspace_name" of String, parameter "source" of String,
           parameter "taxon_wsname" of String, parameter "taxon_id" of
           String, parameter "release" of String, parameter "genetic_code" of
           Long, parameter "scientific_name" of String, parameter "metadata"
           of type "usermeta" -> mapping from String to String, parameter
           "generate_missing_genes" of type "boolean" (A boolean - 0 for
           false, 1 for true. @range (0, 1))
        :returns: instance of unspecified object
        """
        # ctx is the context object
        # return variables are: genome
        #BEGIN fasta_gff_to_genome_json
        importer = FastaGFFToGenome(self.cfg)
        genome = importer.generate_genome_json(params)
        #END fasta_gff_to_genome_json

        # At some point might do deeper type checking...
        if not isinstance(genome, object):
            raise ValueError('Method fasta_gff_to_genome_json return value ' +
                             'genome is not type object as required.')
        # return the results
        return [genome]

    def fasta_gff_to_metagenome(self, ctx, params):
        """
        :param params: instance of type "FastaGFFToMetagenomeParams"
           (genome_name - becomes the name of the object workspace_name - the
           name of the workspace it gets saved to. source - Source of the
           file typically something like RefSeq or Ensembl taxon_ws_name -
           where the reference taxons are : ReferenceTaxons taxon_id - if
           defined, will try to link the Genome to the specified taxonomy id
           in lieu of performing the lookup during upload release - Release
           or version number of the data per example Ensembl has numbered
           releases of all their data: Release 31 genetic_code - Genetic code
           of organism. Overwrites determined GC from taxon object
           scientific_name - will be used to set the scientific name of the
           genome and link to a taxon generate_missing_genes - If the file
           has CDS or mRNA with no corresponding gene, generate a spoofed
           gene. Off by default) -> structure: parameter "fasta_file" of type
           "File" -> structure: parameter "path" of String, parameter
           "shock_id" of String, parameter "ftp_url" of String, parameter
           "gff_file" of type "File" -> structure: parameter "path" of
           String, parameter "shock_id" of String, parameter "ftp_url" of
           String, parameter "genome_name" of String, parameter
           "workspace_name" of String, parameter "source" of String,
           parameter "scientific_name" of String, parameter "metadata" of
           type "usermeta" -> mapping from String to String, parameter
           "generate_missing_genes" of type "boolean" (A boolean - 0 for
           false, 1 for true. @range (0, 1))
        :returns: instance of type "MetagenomeSaveResult" -> structure:
           parameter "metagenome_ref" of String
        """
        # ctx is the context object
        # return variables are: returnVal
        #BEGIN fasta_gff_to_metagenome

        for key in list(params.keys()):
            if params[key] is None:
                del params[key]

        for key, value in params.items():
            if isinstance(value, str):
                params[key] = value.strip()

        params['is_metagenome'] = True

        importer = FastaGFFToGenome(self.cfg)
        returnVal = importer.import_file(params)
        #END fasta_gff_to_metagenome

        # At some point might do deeper type checking...
        if not isinstance(returnVal, dict):
            raise ValueError('Method fasta_gff_to_metagenome return value ' +
                             'returnVal is not type dict as required.')
        # return the results
        return [returnVal]

    def save_one_genome(self, ctx, params):
        """
        :param params: instance of type "SaveOneGenomeParams" -> structure:
           parameter "workspace" of String, parameter "name" of String,
           parameter "data" of type "Genome" (Genome object holds much of the
           data relevant for a genome in KBase Genome publications should be
           papers about the genome Should the Genome object contain a list of
           contig_ids too? Source: allowed entries RefSeq, Ensembl,
           Phytozome, RAST, Prokka, User_upload #allowed entries RefSeq,
           Ensembl, Phytozome, RAST, Prokka, User_upload controlled
           vocabulary managed by API Domain is a controlled vocabulary
           Warnings : mostly controlled vocab but also allow for unstructured
           Genome_tiers : controlled vocabulary (based on ap input and API
           checked) Allowed values: #Representative, Reference, ExternalDB,
           User Examples Tiers: All phytozome - Representative and ExternalDB
           Phytozome flagship genomes - Reference, Representative and
           ExternalDB Ensembl - Representative and ExternalDB RefSeq
           Reference - Reference, Representative and ExternalDB RefSeq
           Representative - Representative and ExternalDB RefSeq Latest or
           All Assemblies folder - ExternalDB User Data - User tagged Example
           Sources: RefSeq, Ensembl, Phytozome, Microcosm, User, RAST,
           Prokka, (other annotators) @optional warnings contig_lengths
           contig_ids source_id taxonomy publications @optional
           ontology_events ontologies_present non_coding_features mrnas
           genome_type @optional genbank_handle_ref gff_handle_ref
           external_source_origination_date @optional release
           original_source_file_name notes quality_scores suspect
           assembly_ref @metadata ws gc_content as GC content @metadata ws
           taxonomy as Taxonomy @metadata ws md5 as MD5 @metadata ws dna_size
           as Size @metadata ws genetic_code as Genetic code @metadata ws
           domain as Domain @metadata ws source_id as Source ID @metadata ws
           source as Source @metadata ws scientific_name as Name @metadata ws
           genome_type as Genome Type @metadata ws length(features) as Number
           of Protein Encoding Genes @metadata ws length(cdss) as Number of
           CDS @metadata ws assembly_ref as Assembly Object @metadata ws
           num_contigs as Number contigs @metadata ws length(warnings) as
           Number of Genome Level Warnings @metadata ws suspect as Suspect
           Genome) -> structure: parameter "id" of type "Genome_id" (KBase
           genome ID @id kb), parameter "scientific_name" of String,
           parameter "domain" of String, parameter "warnings" of list of
           String, parameter "genome_tiers" of list of String, parameter
           "feature_counts" of mapping from String to Long, parameter
           "genetic_code" of Long, parameter "dna_size" of Long, parameter
           "num_contigs" of Long, parameter "molecule_type" of String,
           parameter "contig_lengths" of list of Long, parameter "contig_ids"
           of list of String, parameter "source" of String, parameter
           "source_id" of type "source_id" (Reference to a source_id @id
           external), parameter "md5" of String, parameter "taxonomy" of
           String, parameter "gc_content" of Double, parameter "publications"
           of list of type "publication" (Structure for a publication (float
           pubmedid string source (ex. Pubmed) string title string web
           address string  publication year string authors string journal))
           -> tuple of size 7: parameter "pubmedid" of Double, parameter
           "source" of String, parameter "title" of String, parameter "url"
           of String, parameter "year" of String, parameter "authors" of
           String, parameter "journal" of String, parameter "ontology_events"
           of list of type "Ontology_event" (@optional ontology_ref
           method_version eco description) -> structure: parameter "id" of
           String, parameter "ontology_ref" of type "Ontology_ref" (Reference
           to a ontology object @id ws KBaseOntology.OntologyDictionary),
           parameter "method" of String, parameter "method_version" of
           String, parameter "timestamp" of String, parameter "eco" of
           String, parameter "description" of String, parameter
           "ontologies_present" of mapping from String to mapping from String
           to String, parameter "features" of list of type "Feature"
           (Structure for a single CDS encoding ???gene??? of a genome ONLY
           PUT GENES THAT HAVE A CORRESPONDING CDS IN THIS ARRAY NOTE:
           Sequence is optional. Ideally we can keep it in here, but
           Recognize due to space constraints another solution may be needed.
           We may want to add additional fields for other CDM functions
           (e.g., atomic regulons, coexpressed fids, co_occurring fids,...)
           protein_translation_length and protein_translation are for longest
           coded protein (representative protein for splice variants) NOTE:
           New Aliases field definitely breaks compatibility. As Does
           Function. flags are flag fields in GenBank format. This will be a
           controlled vocabulary. Initially Acceptable values are pseudo,
           ribosomal_slippage, and trans_splicing Md5 is the md5 of
           dna_sequence. @optional functions ontology_terms note
           protein_translation mrnas flags warnings @optional inference_data
           dna_sequence aliases db_xrefs children functional_descriptions) ->
           structure: parameter "id" of type "Feature_id" (KBase Feature ID
           @id external), parameter "location" of list of tuple of size 4:
           type "Contig_id" (ContigSet contig ID @id external), Long, String,
           Long, parameter "functions" of list of String, parameter
           "functional_descriptions" of list of String, parameter
           "ontology_terms" of mapping from String to mapping from String to
           list of Long, parameter "note" of String, parameter "md5" of
           String, parameter "protein_translation" of String, parameter
           "protein_translation_length" of Long, parameter "cdss" of list of
           String, parameter "mrnas" of list of String, parameter "children"
           of list of String, parameter "flags" of list of String, parameter
           "warnings" of list of String, parameter "inference_data" of list
           of type "InferenceInfo" (category;#Maybe a controlled vocabulary
           type;#Maybe a controlled vocabulary) -> structure: parameter
           "category" of String, parameter "type" of String, parameter
           "evidence" of String, parameter "dna_sequence" of String,
           parameter "dna_sequence_length" of Long, parameter "aliases" of
           list of tuple of size 2: parameter "fieldname" of String,
           parameter "alias" of String, parameter "db_xrefs" of list of tuple
           of size 2: parameter "db_source" of String, parameter
           "db_identifier" of String, parameter "non_coding_features" of list
           of type "NonCodingFeature" (Structure for a single feature that is
           NOT one of the following: Protein encoding gene (gene that has a
           corresponding CDS) mRNA CDS Note pseudo-genes and Non protein
           encoding genes are put into this flags are flag fields in GenBank
           format. This will be a controlled vocabulary. Initially Acceptable
           values are pseudo, ribosomal_slippage, and trans_splicing Md5 is
           the md5 of dna_sequence. @optional functions ontology_terms note
           flags warnings functional_descriptions @optional inference_data
           dna_sequence aliases db_xrefs children parent_gene) -> structure:
           parameter "id" of type "Feature_id" (KBase Feature ID @id
           external), parameter "location" of list of tuple of size 4: type
           "Contig_id" (ContigSet contig ID @id external), Long, String,
           Long, parameter "type" of String, parameter "functions" of list of
           String, parameter "functional_descriptions" of list of String,
           parameter "ontology_terms" of mapping from String to mapping from
           String to list of Long, parameter "note" of String, parameter
           "md5" of String, parameter "parent_gene" of String, parameter
           "children" of list of String, parameter "flags" of list of String,
           parameter "warnings" of list of String, parameter "inference_data"
           of list of type "InferenceInfo" (category;#Maybe a controlled
           vocabulary type;#Maybe a controlled vocabulary) -> structure:
           parameter "category" of String, parameter "type" of String,
           parameter "evidence" of String, parameter "dna_sequence" of
           String, parameter "dna_sequence_length" of Long, parameter
           "aliases" of list of tuple of size 2: parameter "fieldname" of
           String, parameter "alias" of String, parameter "db_xrefs" of list
           of tuple of size 2: parameter "db_source" of String, parameter
           "db_identifier" of String, parameter "cdss" of list of type "CDS"
           (Structure for a single feature CDS flags are flag fields in
           GenBank format. This will be a controlled vocabulary. Initially
           Acceptable values are pseudo, ribosomal_slippage, and
           trans_splicing Md5 is the md5 of dna_sequence. @optional
           parent_gene parent_mrna functions ontology_terms note flags
           warnings @optional inference_data dna_sequence aliases db_xrefs
           functional_descriptions) -> structure: parameter "id" of type
           "cds_id" (KBase CDS ID @id external), parameter "location" of list
           of tuple of size 4: type "Contig_id" (ContigSet contig ID @id
           external), Long, String, Long, parameter "md5" of String,
           parameter "protein_md5" of String, parameter "parent_gene" of type
           "Feature_id" (KBase Feature ID @id external), parameter
           "parent_mrna" of type "mrna_id" (KBase mRNA ID @id external),
           parameter "note" of String, parameter "functions" of list of
           String, parameter "functional_descriptions" of list of String,
           parameter "ontology_terms" of mapping from String to mapping from
           String to list of Long, parameter "flags" of list of String,
           parameter "warnings" of list of String, parameter "inference_data"
           of list of type "InferenceInfo" (category;#Maybe a controlled
           vocabulary type;#Maybe a controlled vocabulary) -> structure:
           parameter "category" of String, parameter "type" of String,
           parameter "evidence" of String, parameter "protein_translation" of
           String, parameter "protein_translation_length" of Long, parameter
           "aliases" of list of tuple of size 2: parameter "fieldname" of
           String, parameter "alias" of String, parameter "db_xrefs" of list
           of tuple of size 2: parameter "db_source" of String, parameter
           "db_identifier" of String, parameter "dna_sequence" of String,
           parameter "dna_sequence_length" of Long, parameter "mrnas" of list
           of type "mRNA" (Structure for a single feature mRNA flags are flag
           fields in GenBank format. This will be a controlled vocabulary.
           Initially Acceptable values are pseudo, ribosomal_slippage, and
           trans_splicing Md5 is the md5 of dna_sequence. @optional
           parent_gene cds functions ontology_terms note flags warnings
           @optional inference_data dna_sequence aliases db_xrefs
           functional_descriptions) -> structure: parameter "id" of type
           "mrna_id" (KBase mRNA ID @id external), parameter "location" of
           list of tuple of size 4: type "Contig_id" (ContigSet contig ID @id
           external), Long, String, Long, parameter "md5" of String,
           parameter "parent_gene" of type "Feature_id" (KBase Feature ID @id
           external), parameter "cds" of type "cds_id" (KBase CDS ID @id
           external), parameter "dna_sequence" of String, parameter
           "dna_sequence_length" of Long, parameter "note" of String,
           parameter "functions" of list of String, parameter
           "functional_descriptions" of list of String, parameter
           "ontology_terms" of mapping from String to mapping from String to
           list of Long, parameter "flags" of list of String, parameter
           "warnings" of list of String, parameter "inference_data" of list
           of type "InferenceInfo" (category;#Maybe a controlled vocabulary
           type;#Maybe a controlled vocabulary) -> structure: parameter
           "category" of String, parameter "type" of String, parameter
           "evidence" of String, parameter "aliases" of list of tuple of size
           2: parameter "fieldname" of String, parameter "alias" of String,
           parameter "db_xrefs" of list of tuple of size 2: parameter
           "db_source" of String, parameter "db_identifier" of String,
           parameter "assembly_ref" of type "Assembly_ref" (Reference to an
           Assembly object in the workspace @id ws
           KBaseGenomeAnnotations.Assembly), parameter "taxon_ref" of type
           "Taxon_ref" (Reference to a taxon object @id ws
           KBaseGenomeAnnotations.Taxon), parameter "genbank_handle_ref" of
           type "genbank_handle_ref" (Reference to a handle to the Genbank
           file on shock @id handle), parameter "gff_handle_ref" of type
           "gff_handle_ref" (Reference to a handle to the GFF file on shock
           @id handle), parameter "external_source_origination_date" of
           String, parameter "release" of String, parameter
           "original_source_file_name" of String, parameter "notes" of
           String, parameter "quality_scores" of list of type
           "GenomeQualityScore" (Score_interpretation : fraction_complete -
           controlled vocabulary managed by API @optional method_report_ref
           method_version) -> structure: parameter "method" of String,
           parameter "method_report_ref" of type "Method_report_ref"
           (Reference to a report object @id ws KBaseReport.Report),
           parameter "method_version" of String, parameter "score" of String,
           parameter "score_interpretation" of String, parameter "timestamp"
           of String, parameter "suspect" of type "Bool", parameter
           "genome_type" of String, parameter "hidden" of type "boolean" (A
           boolean - 0 for false, 1 for true. @range (0, 1)), parameter
           "upgrade" of type "boolean" (A boolean - 0 for false, 1 for true.
           @range (0, 1))
        :returns: instance of type "SaveGenomeResult" -> structure: parameter
           "info" of type "object_info" (Information about an object,
           including user provided metadata. obj_id objid - the numerical id
           of the object. obj_name name - the name of the object. type_string
           type - the type of the object. timestamp save_date - the save date
           of the object. obj_ver ver - the version of the object. username
           saved_by - the user that saved or copied the object. ws_id wsid -
           the workspace containing the object. ws_name workspace - the
           workspace containing the object. string chsum - the md5 checksum
           of the object. int size - the size of the object in bytes.
           usermeta meta - arbitrary user-supplied metadata about the
           object.) -> tuple of size 11: parameter "objid" of type "obj_id"
           (The unique, permanent numerical ID of an object.), parameter
           "name" of type "obj_name" (A string used as a name for an object.
           Any string consisting of alphanumeric characters and the
           characters |._- that is not an integer is acceptable.), parameter
           "type" of type "type_string" (A type string. Specifies the type
           and its version in a single string in the format
           [module].[typename]-[major].[minor]: module - a string. The module
           name of the typespec containing the type. typename - a string. The
           name of the type as assigned by the typedef statement. major - an
           integer. The major version of the type. A change in the major
           version implies the type has changed in a non-backwards compatible
           way. minor - an integer. The minor version of the type. A change
           in the minor version implies that the type has changed in a way
           that is backwards compatible with previous type definitions. In
           many cases, the major and minor versions are optional, and if not
           provided the most recent version will be used. Example:
           MyModule.MyType-3.1), parameter "save_date" of type "timestamp" (A
           time in the format YYYY-MM-DDThh:mm:ssZ, where Z is either the
           character Z (representing the UTC timezone) or the difference in
           time to UTC in the format +/-HHMM, eg: 2012-12-17T23:24:06-0500
           (EST time) 2013-04-03T08:56:32+0000 (UTC time)
           2013-04-03T08:56:32Z (UTC time)), parameter "version" of Long,
           parameter "saved_by" of type "username" (Login name of a KBase
           user account.), parameter "wsid" of type "ws_id" (The unique,
           permanent numerical ID of a workspace.), parameter "workspace" of
           type "ws_name" (A string used as a name for a workspace. Any
           string consisting of alphanumeric characters and "_", ".", or "-"
           that is not an integer is acceptable. The name may optionally be
           prefixed with the workspace owner's user name and a colon, e.g.
           kbasetest:my_workspace.), parameter "chsum" of String, parameter
           "size" of Long, parameter "meta" of type "usermeta" (User provided
           metadata about an object. Arbitrary key-value pairs provided by
           the user.) -> mapping from String to String
        """
        # ctx is the context object
        # return variables are: returnVal
        #BEGIN save_one_genome

        genome_interface = GenomeInterface(self.cfg)
        returnVal = genome_interface.save_one_genome(params)
        #END save_one_genome

        # At some point might do deeper type checking...
        if not isinstance(returnVal, dict):
            raise ValueError('Method save_one_genome return value ' +
                             'returnVal is not type dict as required.')
        # return the results
        return [returnVal]
    def status(self, ctx):
        #BEGIN_STATUS
        returnVal = {'state': "OK", 'message': "", 'version': self.VERSION,
                     'git_url': self.GIT_URL, 'git_commit_hash': self.GIT_COMMIT_HASH}
        #END_STATUS
        return [returnVal]
