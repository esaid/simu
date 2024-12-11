# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import sys
import math
import numpy as np
import matplotlib.pyplot as np
import pandas as pd
import openpyxl


def import_fileCPU(self, fileSource):
    with open(fileSource, 'r') as f:
        encoding = "cp1252"
    try:
        #
        self = pd.read_excel(fileSource, engine='openpyxl')
    except:
        print("Something went wrong when reading the file ", fileSource)
        sys.exit()
    return self


class conversion():
    def import_fileCPU(self, filedatasource):
        with open(filedatasource, 'r') as f:
            encoding = "cp1252"
        try:
            #
            # self = pd.read_csv(filedatasource)
            self = pd.read_excel(filedatasource)
        except:
            print("Something went wrong when reading the file ", filedatasource)
            sys.exit()
        return self

    def __init__(self, filedatasource):
        self.dataframe = import_fileCPU(self, filedatasource)
        self.dataframe.astype(str)


    def show(self):
        print('dataframe: ', self.dataframe)

    def binaire(self, opcodetest):
        """ donne la correspondance binaire de opcode
        :param opcodetest:
        :param simu:
        :return: un string mot binaire sur 5 bits
        >>> binaire('dup')
        '11000'
        >>> binaire('@p')
        '01000'
        """
        return self.dataframe.loc[self.dataframe['opcode'] == opcodetest, 'op binary (5bits)'].to_numpy()[0]

    def opcode(self, motbinaire):
        """ donne la correspondance  de opcode par rapport au codebinaire
        :param motbinaire:
        :param simu:
        :return: opcode du F18
        >>> opcode('11100')
        '.'
        >>> opcode('11111')
        'a!'
        """
        opcode = self.dataframe.loc[self.dataframe['op binary (5bits)'] == motbinaire, 'opcode'].to_numpy()[0]
        return opcode

    def codage(self, mot):
        """

        :param mot: [opcode0 opcode1 opcode2 opcode3]
        :return: 0x hexa sur 4 digits
        >>> codage(['@p', 'a!', '@p', '.'])
        0x4a12
        """
        # opcode0 opcode1 opcode2 opcode3
        # 5bits 5bits 5bits 5bits
        # 5bits 5bits 5bits 3bits    , supprimer les 2 derniers bits
        # mots18its XOR $15555
        mot20bits = ''
        for m in mot:
            mot20bits += self.binaire(m)
        mot18bits = int(mot20bits, base=2)
        mot18bits = (mot18bits >> 2) ^ 0x15555

        return mot18bits

    def decodagebinaire(self, mot):
        mot20bits = ''
        mot20bits = (mot ^ 0x15555) << 2

        mot20bits = "{0:b}".format(mot20bits)
        while len(mot20bits) < 20:
            mot20bits = '0' + mot20bits

        # print(len(mot20bits))

        return mot20bits

    def decodage(self, motbinaire):
        listemot = []

        for i in range(0, 19, 5):
            listemot.append((self.opcode((self.decodagebinaire(motbinaire)[i:i + 5]))))

        return listemot


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # initialisation fichier source Excel

    fileSource = "CPU.xlsx"
    # instanciation
    simu = conversion(fileSource)
    simu.show()

    opcodetest ='dup'
    print(opcodetest , ' ' , simu.binaire(opcodetest))
    mot = ['@p', 'a!', '@p', '.']
    print(mot, ' ', hex(simu.codage(mot)))

    print('0x4a12 ', simu.decodagebinaire(0x4a12))

    print('01000 ', simu.opcode('01000'))

    sys.exit()

