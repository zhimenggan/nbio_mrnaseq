#!/usr/bin/env python
__author__ = "Xiaoyu Liu"
__email__ = "liux@nbio.info"
__copyright__ = "Copyright (C) 2016 Xiaoyu Liu"
__status__ = "development"
__license__ = "Public Domain"
__version__ = "0.2b"

import pandas as pd
import sys, json
def qc_alignment(samples, output):
    '''
    parse the star align statistics
    :param samples, output:
    :return html QC table:
    '''

    qc_table = pd.DataFrame()
    qc_html  = pd.DataFrame()
    graphs = pd.Series(['QC_graphs/{}_geneboday_coverage.png',
                        'QC_graphs/{}_junction_satuation.png',
                        'QC_graphs/{}_splice_junction.png',
                        'QC_graphs/{}_inner_distance.png',
                        'QC_graphs/{}_read_dupRate.png'],
                index = ["Gene Body Coverage",
                         "Junction Saturation",
                         "Splicing Junction",
                         "ReadPair Inner Distance",
                         "Read Dupliction"])
    for sample in samples:
        sample_graphs = graphs.map(lambda x: x.format(sample))
        qc_table[sample]= sample_graphs
        sample_graph_links = sample_graphs.apply(lambda x: '<a href="{s}"><img src="{s}"]" alt="N.A." width="160" hight="40">'.format(s=x))
        qc_html[sample] = sample_graph_links


    qc_table.T.to_csv(output + ".txt", sep='\t')

    pd.set_option('display.max_colwidth', -1)  # prevent to_html truncating string
    with open ( output + ".html", 'w') as f_out:
        f_out.write( qc_html.T.to_html(classes="table table-bordered table-hover",  escape=False, ) )

if __name__ == "__main__":

    if len(sys.argv) != 3:
        print("USAGE: {} <run_config> <output_prefix>".format(sys.argv[0]))
        exit(-1)
    config = json.load(open(sys.argv[1]))
    samples = [ s for trt in sorted(config["treatments"].keys()) for s in config["treatments"][trt] ]
    qc_alignment(samples, sys.argv[2])