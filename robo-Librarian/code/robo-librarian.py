#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""A script to rearrange the order of a long PDF document so that if
printed in Tabloid style, it reads like a book.

Here is how it works: 
E.g., for a document with 8 pages, this code rearranges the pages to
the following order:
4, 5, 6, 3, 2, 7, 8, 1

For a longer document, it splits the documents into the desired number of
booklets before rearranging it, and combining it all into a single PDF file.

The code enable via an argument to print in a right-to-left reading style if so thy wishest ;)

@authors: Original code : ChongChong He, on Nov 19, 2019. Tested with Python 3.6.7 on
                            macOS. Contact: chongchong@astro.umd.edu
                 Remake : JoBioux, 1st October, 2023. Tested with the 362 pages long open archive 
                            "坊っちゃん bocchan", by Natsume Souseki, bookletSize = 8 and bookletSize = 3, 
                            with python 3.11.5 on Windows 10 
                            contact : 

"""

import sys
import os
import math
import numpy as np
from PyPDF2 import PdfWriter as Writer, PdfReader as Reader
import argparse

def parse_arguments():
    parser = argparse.ArgumentParser(prog = "Robo-Librarian", description= "Give me a 4+ pages PDF document, and I'll edit "+
                                                                           "it to enable you to print it, split it into piles "+
                                                                           "of x sheets (x being 8 by default, but you can "+
                                                                           "set the number you like using '-n [int]'), fold "+
                                                                           "each of the booklet and make them stay together "+
                                                                           "(sewing them for example) and finally combining "+
                                                                           "all of your booklet into your very own edition of "+
                                                                           "your favorite text !"+
                                                                       "\n\nPrinter settings :"+
                                                                         "\n    Paper size: Tabloid (11*17 in) for academic papers, books, etc ;"+
                                                                         "\n    Layout: 2 pages per sheet. Set layout direction to normal 'Z' layout. Set two-sided to Short-Edge binding ;"+
                                                                         "\n    Scale to fit the page. An example setup for ARA&A:"+
                                                                         "\n                                162% on 11*17 Borderless", 
                                                                  epilog = "original code by ChongChong He, 19th November 2019 "+
                                                                           "as 'booklet.py', url : "+
                                                                           "https://github.com/chongchonghe/booklet-creator/blob/master/booklet.py"+
                                                                           "Remade and extended by JoBioux, 1st October 2023.")
    
    parser.add_argument(dest='pdffile',                              type = str,  help="The PDF file to convert")
    parser.add_argument('-s', '--start' ,           default = 1,     type = int,  help="The starting page number")
    parser.add_argument('-e', '--end',                               type = int,  help="The ending page number")
    parser.add_argument('-n', '--number',           default = 8,     type = int,  help="the number of sheets per booklet. Default = 8")
    parser.add_argument('-r', '--readingDirection', default = False, type = bool, help="'True' for a right to left reading (Japanese, Arabic, etc.). Default = False (Left to right)")
    return parser.parse_args()

def define(bookletSize) : #generates the order in which  
                          #pages should be on the sheets
    
    
    
    numberofSheets = bookletSize // 4
    
    base = np.arange(numberofSheets) + 1  # = 1, 2, ... 11
    base = 2 * base                       # = 2, 4, ... 22
    base = base[::-1]                     # = 22, 21, ... 2
    pages = []
    num = bookletSize + 1 # = 45
    for i in base:
        pages.append(i)
        pages.append(num - i)
        pages.append(num - i + 1)
        pages.append(num - (num - i + 1))
    return pages

def direction(readingDirection) : #returns "leftToRight" or "rightToLeft"
                                  #depending on the direction in which  
                                  #the document should be read 
    if readingDirection : 
        return "rightToLeft"
    else : 
        return "leftToRight"
  
def getSection(doc, start, end) : #gets a page from the base document
                                  #and adds it to "section" which is 
                                  #then returned
    section = Writer()
    print("New booklet beginning at page "+str(start+1))
    loopEnd = end-start+2
    for i in range(loopEnd) : 
        element = doc.pages[start]
        section.add_page(element)
        start += 1
    return section

def generateFinalSection(fname, nop, bookletSize) : #checks the number of pages
                                                    #and generates a fitting PDF
    
    lastSection = getSection(fname, nop-(nop%bookletSize), nop-2)
    finalNop = len(lastSection.pages)
    nop_booklet = finalNop // 4
    blankCounter = 0

    
    if finalNop % 4 > 0:
        nop_booklet += 1
        blankPagesNumber = finalNop%4
    
        while len(lastSection.pages)%4 > 0:
        
            lastSection.add_blank_page()
            blankCounter += 1
        
        print("Added "+str(blankCounter)+" blank page(s) at the end")

    return lastSection


def bookletify(doc, bookletNop, nop, readingDirection) : #takes a section of a PDF
                                                         #and changes the order of its 
                                                         #pages so that it can be printed
                                                         #as a booklet
    
    order = define(len(doc.pages))
    booklet = Writer()
    
    
    for i in range(len(doc.pages)) :
        idx = int(i)
        page = doc.pages[int(order[idx])-1]
        if readingDirection :
            page = page.rotate(180)
        booklet.add_page(page)
    return booklet



    
def splitDocument(baseDoc, nop, nopPerBooklet, fname, readingDirection) : #Creates new temporary PDFs to be 
                                                                          #reordered as booklets, and returns 
                                                                          #the temporary PDF names
    names = []

    
    if nop < 4 :
        print("ERROR : This program was made to automatically generate a "+ 
              "printable, booklet type version of a PDF file. Your "+
              "file was deemed too small to need this transformation")
        sys.exit()
    elif nop%nopPerBooklet > 0 :
        
        
        for i in range(int((nop-(nop%nopPerBooklet))/nopPerBooklet)) :
            
            
            tmp = os.path.join(os.path.dirname(fname)+"\\tmp\\",
                               os.path.basename(fname) + ".tmp"+str((i+1))+".pdf")
            
            section = getSection(baseDoc, i*nopPerBooklet, i*nopPerBooklet+nopPerBooklet-2)
            section = bookletify(section, nopPerBooklet, nop, readingDirection)
            
            with open(tmp, "wb") as new :
                section.write(new)
            
            names.append(tmp)
        
        tmp = os.path.join(os.path.dirname(fname)+"\\tmp\\",
                               os.path.basename(fname) + ".tmpFinal.pdf")
                               
        section = generateFinalSection(baseDoc, nop, nopPerBooklet)
        section = bookletify(section, len(section.pages), nop, readingDirection)
        
        with open(tmp, "wb") as new :
                section.write(new)
                           
        names.append(tmp)
    
    
    else :
        for i in range(int(nop/nopPerBooklet)) :
            tmp = os.path.join(os.path.dirname(fname)+"\\tmp\\",
                               os.path.basename(fname) + ".tmp"+str((i+1))+".pdf")
            
            section = getSection(fname, i*nopPerBooklet+1, i*nopPerBooklet+nopPerBooklet+1)
            
            section = bookletify(section, nopPerBooklet, nop, readingDirection)
            
            with open(tmp, "wb") as new :
                section.write(new)
            
            names.append(tmp)
    
    return names
        
    
def addToFinal(allTmps_nameFromArray, completeDoc) : #copies every pages from a single tmp PDF
                                                     #and adds it to a variable which gets returned
                                                     #as the "most up-to-date" final document
                                                     
    
    booklet = Reader(open(allTmps_nameFromArray, 'rb'))
    for i in range(len(booklet.pages)) :
        completeDoc.add_page(booklet.pages[i])
        
    
    return completeDoc
        
def saveFinal(fname, finalContainer, bookletSize, readingDirection) : #saves final document as 
                                                                      #"{base_name}.{desiredNumber;default=8}sheetsBooklets.pdf"
    final = os.path.join(os.path.dirname(fname),
                         os.path.basename(fname) + "."+str(bookletSize)+"sheetsBooklets."+direction(readingDirection)+".pdf")    
    with open(final, 'wb') as doc :
        finalContainer.write(doc)
        
    print("File saved as {}".format(final))
    


def run(fname, start = 1, end = None, bookletSize = 8, readingDirection = False) :
    
    
    baseDoc = Reader(open(fname, 'rb'))
    nop = len(baseDoc.pages)
    nopPerBooklet = bookletSize*4
    pages = define(nopPerBooklet)
    pdfsToUnify = splitDocument(baseDoc, nop, nopPerBooklet, fname, readingDirection)
    finalDocument = Writer()
    
    print("Unifying the documents into one...")
    for i in range(len(pdfsToUnify)-1) :
        
        finalDocument = addToFinal(pdfsToUnify[i], finalDocument)
        
    finalDocument = addToFinal(pdfsToUnify[len(pdfsToUnify)-1], finalDocument)
    
    saveFinal(fname, finalDocument, bookletSize, readingDirection)
    

if __name__ == "__main__":

    args = parse_arguments()
    
    run(args.pdffile, args.start, args.end, args.number, args.readingDirection)

    