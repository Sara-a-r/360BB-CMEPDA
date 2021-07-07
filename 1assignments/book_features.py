import matplotlib.pyplot as plt                 # for the istogram
import numpy as np
import math

def print_stats(book):
    """ Return n-of-characters, n-of-words, n-of-lines of the book.
    """
    n_caratteri=0                           # inizializzo il numero di caratteri a zero
    letters = 'abcdefghijklmnopqrstuvwxyz'  # Lettere da analizzare
    n_parole = len(book.split())            # Prende solo le parole nell'array split
    for char in book:                       # Conto i caratteri non vuoti
        if char in letters:
            n_caratteri += 1
    n_righe = len(book.splitlines())        # Prende solo le righe nell'array splitlines
    print(f'Number of characters: {n_caratteri}\n'\
           f'Number of words: {n_parole}\n'\
           f'Number of lines: {n_righe}')

def istogram(freq_dict):
    """ Print ascii istogram.
    """
    letters = []                            # Inizializzo vuoti, riempio nel
    vec = []                                #   loop scorrendo il dizionario
    # Riempie i miei vettori per il plot scorrendo il dizionario.
    for ch, freq in freq_dict.items():
        letters.append(ch)
        vec = np.append(vec,freq*100)

        # stampa l'istogramma su volontà dell'utente.
    plt.bar(letters, height=vec)
    plt.grid(axis='y', alpha=0.75)
    plt.xlabel('Value')
    plt.ylabel('Frequency')
    plt.title('Letters Frequencies')
    maxfreq = vec.max()
    plt.ylim(ymax=maxfreq+1)
    plt.show()

def print_freq(freq_dict):
    """ Print data and ascii istogram.
    """
    for ch, freq in freq_dict.items():
        if freq*100. < 10:                      # Se la percentuale è minore di 10 serve uno spazio in più
            #   lettera: perc                   esempio: 5% = #####, la funzione ceil arrotonda.
            print(f'{ch}: {freq:.3%} ', '#'*math.ceil( freq*100. - 0.5 ))
        else:
            print(f'{ch}: {freq:.3%}', '#'*math.ceil( freq*100. - 0.5 ))


