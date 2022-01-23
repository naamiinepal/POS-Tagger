# -*- coding: utf-8 -*-
"""
Created on Sun Jan 23 11:54:21 2022

@author: Sagun Shakya
"""

import os
import xml.etree.ElementTree as ET
from tqdm import tqdm
from pandas import DataFrame
import argparse
from utils import get_filenames
from time import time

def get_sent_tags(path):
    '''
    Gets the list of all the tokens and tags from a directory of Nepali National Corpus.

    Parameters
    ----------
    path : str
        Path to the XML files under NNC project.

    Raises
    ------
    FileNotFoundError
        if the directory doesn't exist.

    Returns
    -------
    Pandas DataFrame.
        DataFrame containing words (list) and corresponding tags (list).
        Columns -- ["words", "tags"] 

    '''
    
    if os.path.exists(path):
        filelist = get_filenames(path, verbose=False)
    else:
        raise FileNotFoundError
    
    ALLTAG= []
    ALLWORD = []

    for ii, file in tqdm(enumerate(filelist), desc = "Loop file"):
        
        if file.endswith('.xml'):
            filepath = os.path.join(path, file)
            #print(filepath)
        
            tree = ET.parse(filepath)
            root = tree.getroot()
            
            print(f"\nProcessing the file: {file}")
            
            for data in tqdm(root.findall('text'), desc = "Loop Text"):
                for value in data:
                    # #print(value.tag)
                    if (value.tag == 'group'):
                        # for group in value.findall('group'):
                        for body in value.findall('body'):
                            for div in body.findall('div'):
                                for subdiv in div:
                                    # #print(subdiv.tag)
                                    if (subdiv.tag == "head"):
                                        for sentence in subdiv.findall('s'):
                                            # #print(sentence.attrib)
        
                                            tags_i = []
                                            words_i = []
                                            for s in sentence:
                                                # #print(s.attrib)
                                                if (s.tag == "foreign"):
                                                    for words in s.findall('w'):
                                                        tags_i.append(words.attrib['ctag'])
                                                        words_i.append(words.text)
                                                        #print("%s/%s" % (words.text, words.attrib['ctag']), '', end=''),
        
        
                                                # #print("\n")
                                                if (s.tag == "w"):
                                                    tags_i.append(s.attrib['ctag'])
                                                    words_i.append(s.text)
                                                    #print("%s/%s" % (s.text, s.attrib['ctag']), '', end=''),
                                                    # countTags(tags,s.attrib['ctag'])
                                            
                                            if len(words_i) > 4:
                                                ALLTAG.append(tags_i)
                                                ALLWORD.append(words_i)
        
                                            #print('\n')
        
                                    if (subdiv.tag == "p"):
                                        for sentence in subdiv.findall('s'):
                                            #print(sentence.attrib)
        
                                            tags_j = []
                                            words_j = []
                                            for s in sentence:
                                                if (s.tag == "foreign"):
                                                    for words in s.findall('w'):
                                                        tags_j.append(words.attrib['ctag'])
                                                        words_j.append(words.text)
                                                        #print("%s/%s" % (words.text, words.attrib['ctag']), '', end=''),
                                                        # countTags(tags,words.attrib['ctag'])
                                                # #print("\n")
                                                if (s.tag == "w"):
                                                    tags_j.append(s.attrib['ctag'])
                                                    words_j.append(s.text)
                                                    #print("%s/%s" % (s.text, s.attrib['ctag']), '', end=''),
                                                    # countTags(tags,s.attrib['ctag'])
                                            if len(words_j) > 4:
                                                ALLTAG.append(tags_j)
                                                ALLWORD.append(words_j)
                                            
                                            #print('\n')
        
                    if (value.tag == 'body'):
                        # for body in value.findall('body'):
                        for div in value.findall('div'):
                            for subdiv in div:
                                # #print(subdiv.tag)
                                if (subdiv.tag == "head"):
                                    for sentence in subdiv.findall('s'):
                                        #print(sentence.attrib)
        
                                        words_i, tags_i = [], []
                                        for s in sentence:
                                            # #print(s.attrib)
                                            if (s.tag == "foreign"):
                                                for words in s.findall('w'):
                                                    tags_i.append(words.attrib['ctag'])
                                                    words_i.append(words.text)
        
                                                    #print("%s/%s" % (words.text, words.attrib['ctag']), '', end=''),
                                                    # countTags(tags,words.attrib['ctag'])
                                            # #print("\n")
                                            if (s.tag == "w"):
                                                tags_i.append(s.attrib['ctag'])
                                                words_i.append(s.text)
        
                                                #print("%s/%s" % (s.text, s.attrib['ctag']), '', end=''),
                                                # countTags(tags,s.attrib['ctag'])
                                        
                                        if len(words_i) > 4:
                                            ALLTAG.append(tags_i)
                                            ALLWORD.append(words_i)
                                            #print('\n')
        
                                if (subdiv.tag == "p"):
                                    for sentence in subdiv.findall('s'):
                                        #print(sentence.attrib)
        
                                        words_i, tags_i = [], []
                                        for s in sentence:
                                            if (s.tag == "foreign"):
                                                for words in s.findall('w'):
                                                    tags_i.append(words.attrib['ctag'])
                                                    words_i.append(words.text)
                                                    #print("%s/%s" % (words.text, words.attrib['ctag']), '', end=''),
                                                    # countTags(tags,words.attrib['ctag'])
                                            # #print("\n")
                                            if (s.tag == "w"):
                                                tags_i.append(s.attrib['ctag'])
                                                words_i.append(s.text)
                                                #print("%s/%s" % (s.text, s.attrib['ctag']), '', end=''),
                                                # countTags(tags,s.attrib['ctag'])
                                        
                                        if len(words_i) > 4:
                                            ALLTAG.append(tags_i)
                                            ALLWORD.append(words_i)                                
                                            #print('\n')
            
    return DataFrame({"words": ALLWORD,
                      "tags": ALLTAG})



if __name__ == '__main__':

    # Parse Arguments.
    parser = argparse.ArgumentParser(description="Parse the XML files of NNC project.")
    parser.add_argument("--files_path", "-i", help="Path to the directory containing the XML files." )
    parser.add_argument("--out_file_path", "-o", help="Path to the file to store the DataFrame. Must end with .gz" )
    args = parser.parse_args()

    # Note time.
    start = time()

    # Parse XML to a DF.
    result = get_sent_tags(path = args.files_path)

    # Save the DF to a compressed .gz file.
    out_filename = args.out_file_path
    result.to_csv(out_filename, index = None, compression = 'gzip')

    end = time()

    print(f"Completed!\nFile saved as: {out_filename}.")
    print(f"Time elapsed: {end - start : 5.2f} seconds.")
