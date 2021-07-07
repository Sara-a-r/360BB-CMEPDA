#!/usr/bin/env python3
""" First Assignemt
"""
import os                                       # Manipulate path of my PC
import argparse                                 # Make --help description
import logging                                  # Make Debug and Warning
import time                                     # Misure time of process
import string
# Don't forget to put in the same folder the file 'book_features.py'
import book_features                            # Add my features

logging.basicConfig(level=logging.INFO)         # Definisce il livello di log
# Potrebbe essere .DEBUG


_DESCRIPTION = 'Measure the releative frequencies of letters in a text file'

def extract(file_path, body):
    """ Extract the text from .txt file.
    """
    logging.info('Opening input file "%s"', file_path)  # Si usa la virgola perché
                                                        #non formatta sempre:
                                                        # se non stampa non formatta.
    with open(file_path) as input_file:         # Apro il file di testo con il libro
        data_raw = input_file.read()
        if body:                                # Estraggo i caratteri che mi servono.
            start_string = '*** START OF THIS PROJECT GUTENBERG EBOOK CHIMERA WORLD ***'
            end_string = '*** END OF THIS PROJECT GUTENBERG EBOOK CHIMERA WORLD ***'
            start = data_raw.find(start_string) + len(start_string)
            stop = data_raw.find(end_string)
            data_body = data_raw[start:stop]
    logging.info('Done. %d character(s) found.', len(data_raw))
    if body:
        logging.info('Extracted the body of %d character(s).', len(data_body))
        data_out = data_body
    else:
        data_out = data_raw
    return data_out

def process(file_path, ist, body, stats):
    """Main processing method.
    """
    start = time.time()                         # Start measuring time
    ##################
    #  Sanity check  #
    ##################
    assert file_path.endswith('.txt'), "Not a txt file"
    assert os.path.isfile(file_path), "Wrong path"

    ##########################################
    #  Open file and prepare the dictionary  #
    ##########################################
    data = extract(file_path, body)              # Extract from the file .txt the book
    # letters = 'abcdefghijklmnopqrstuvwxyz'      # Lettere da analizzare
    freq_dict = {}                              # Dizionario
    # for ch in letters:                          # Inizializzo a zero tutto
    #     freq_dict[ch] = 0
    letters = string.ascii_lowercase            # Ascii_lowercase contiene le lettere a-z
    freq_dict = {ch: 0 for ch in letters}       # Creo il dizionario con un loop su ch

    for char_dict in data.lower():                     # Lower mette tutto minuscolo
        if char_dict in letters:                       # Metto frequenze non normalizzate
            freq_dict[char_dict] += 1                  # nel dizionario.

    num_chars = float(sum(freq_dict.values()))  # Normalizzo solo su lettere conteggiate
    for char_dict in letters:                          # Applico normalizzazione al dizionario
        freq_dict[char_dict] /= num_chars

    #######################
    #  Print the results  #
    #######################
    book_features.print_freq(freq_dict)         # Print Result with ascii istogram
    if stats:
        book_features.print_stats(data)         # Print the stats of the book
    end = time.time()                           # Stop measuring time
    if ist:
        book_features.istogram(freq_dict)      # Print Instrogram from matplotlib
    logging.info('Elapsed Time: %f sec', end-start)


if __name__ == '__main__':                      # Per fare un modulo con più librerie (mie)
    parser = argparse.ArgumentParser(description=_DESCRIPTION)
    parser.add_argument('infile', help='path to the input file')
    parser.add_argument('-i', '--ist', help='Add matplot istogram', action='store_true')
    parser.add_argument('-b', '--body', help='Extract the body of the book', action='store_true')
    parser.add_argument('-s', '--stats', help='Print basic book stats', action='store_true')
    args = parser.parse_args()
    process(args.infile, args.ist, args.body, args.stats)
