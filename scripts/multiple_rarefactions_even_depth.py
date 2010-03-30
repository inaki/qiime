#!/usr/bin/env python
# File created on 09 Feb 2010
from __future__ import division

__author__ = "Justin Kuczynski"
__copyright__ = "Copyright 2010, The QIIME project"
__credits__ = ["Justin Kuczynski"]
__license__ = "GPL"
__version__ = "0.92-dev"
__maintainer__ = "Justin Kuczynski"
__email__ = "justinak@gmail.com"
__status__ = "Pre-release"
 

from qiime.util import parse_command_line_parameters
from optparse import make_option
import os.path
from qiime.rarefaction import RarefactionMaker

script_info={}
script_info['brief_description']="""Perform multiple rarefactions on a single otu table, at one depth of sequences/sample"""
script_info['script_description']="""To perform bootstrap, jackknife, and rarefaction analyses, the otu table must be subsampled (rarefied).  This script rarefies, or subsamples, an OTU table.  This does not provide curves of diversity by number of sequences in a sample. Rather it creates a subsampled OTU table by random sampling (without replacement) of the input OTU table.  The pseudo-random number generator used for rarefaction by subsampling is NumPy's default - an implementation of the Mersenne twister PRNG."""
script_info['script_usage']=[]
script_info['script_usage'].append(("""Example:""","""subsample otu_table.txt at 400 seqs/sample (-d), 100 times (-n), write results to files (i.e. rarefaction_400_17.txt)""","""single_rarefaction.py -i otu_table.txt -o rarefaction_tables -d 400 -n 100"""))
script_info['output_description']="""The results of this script consist of n subsampled OTU tables, written to the directory specified by -o. The file has the same otu table format as the input otu_table.txt. note: if the output files would be empty, no files are written"""


script_info['required_options']=[
    make_option('-i', '--input_path',
        help='input otu table filepath'),

    make_option('-o', '--output_path',
        help="write output rarefied otu tables files to this dir (makes dir if it doesn't exist)"),

    make_option('-d', '--depth', type=int,
        help='sequences per sample to subsample'),
]


script_info['optional_options']=[

    make_option('-n', '--num-reps', dest='num_reps', default=1, type=int,
        help='num iterations at each seqs/sample level [default: %default]'),
     
    make_option('--lineages_included', dest='lineages_included', default=False,
        action="store_true",
          help="""output rarefied otu tables will include taxonomic (lineage) information for each otu, if present in input otu table [default: %default]"""),

    make_option('--small_included', dest='small_included', default=False,
        action="store_true",
        help="""samples containing fewer seqs than the rarefaction level are included in the output but not rarefied [default: %default]""")
]
script_info['version'] = __version__


def main():
    option_parser, opts, args = parse_command_line_parameters(**script_info)

    if not os.path.exists(opts.output_path):
        os.makedirs(opts.output_path)
    maker = RarefactionMaker(opts.input_path, opts.depth, opts.depth,
        1, opts.num_reps)
    maker.rarefy_to_files(opts.output_path, opts.small_included,
        include_lineages=opts.lineages_included)


if __name__ == "__main__":
    main()