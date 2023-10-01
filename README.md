# Robo-Librarian
A program based on ChongChong He's "booklet-creator", to expand the size of the book one could wish to print


Give me a 4+ pages PDF document, and I'll edit it to enable you to print it, split it into piles 
of x sheets (x being 8 by default, but you can set the number you like using '-n [int]'), fold 
each of the booklet and make them stay together (sewing them for example) and finally combining
all of your booklet into your very own edition of your favorite text !
                                                                      
          Printer settings :
                 Paper size: Tabloid (11*17 in) for academic papers, books, etc 
                 Layout: 2 pages per sheet. Set layout direction to normal 'Z' layout. Set two-sided to Short-Edge binding 
                 Scale to fit the page. An example setup for ARA&A:
                                        162% on 11*17 Borderless 

Basic usage : 

  Download the full "robo-Librarian/" folder.
  
  Copy your PDF to the "robo-Librarian" folder and use your terminal and go to "robo-Librarian/code". 
              Then, execute robo-librarian.py and give it the path to your PDF.
              
            For Windows :  
                cd C:\Users\MyUser\PathTo\robo-Librarian\code\
                python robo-librarian.py ..\myPDF.pdf
            
            For Unix : 
                 cd pathTo/robo-Librarian/code/
                 python robo-librarian.py ../myPDF.pdf

  Add " -r True" if you want the final printed version's pages to be turned left to right (Arabic, Japanese etc.).

  Please Type "python robo-librarian.py -h" for more informations.

  Please clear regularly your tmp folder to save space using : 
            
            python clear.py
  If you delete the "tmp" folder by accident just creat a new one, named strictly the same


  Numpy and PyPDF2 are required to run this program


    
original code by ChongChong He, 19th November 2019 as 'booklet.py', url : https://github.com/chongchonghe/booklet-creator/blob/master/booklet.py
  
  Remade and extended by JoBioux, 1st October 2023.

