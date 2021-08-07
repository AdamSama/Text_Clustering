The input of the program has the following pattern:
///////////////////////////////////////////////////////////////////////
Bella Abzug 
An American lawyer, U.S. Representative, social activist and a
leader of the Women's Movement. Abzug joined other leading feminists
such as Gloria Steinem and Betty Friedan to found the National Women's
Political Caucus. 

Benjamin Britten
A composer, conductor and pianist. He was a central figure of..
...................
///////////////////////////////////////////////////////////////////////
This program cluster the each person based on their individual traits occured in the text.

In this lab, I use PorterStemmer algorithm to deal with the text, and in my algorithm, I will write all the regularized and stemmed words into a file called "temp.txt". You can ignore the file called "temp.txt".

If you want to use the stopwords (which will delete all the words that occur in the input file), PLEASE write all the words into a file called "stopwords.txt". And also, please include your input file in a .txt format.

Sample command:
    python lab4.py input.txt stopwords.txt
or
    python lab4.py input.txt