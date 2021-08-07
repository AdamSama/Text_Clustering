import sys
import math
class PorterStemmer:

    def __init__(self):
        """The main part of the stemming algorithm starts here.
        b is a buffer holding a word to be stemmed. The letters are in b[k0],
        b[k0+1] ... ending at b[k]. In fact k0 = 0 in this demo program. k is
        readjusted downwards as the stemming progresses. Zero termination is
        not in fact used in the algorithm.

        Note that only lower case sequences are stemmed. Forcing to lower case
        should be done before stem(...) is called.
        """

        self.b = ""  # buffer for word to be stemmed
        self.k = 0
        self.k0 = 0
        self.j = 0   # j is a general offset into the string

    def cons(self, i):
        """cons(i) is TRUE <=> b[i] is a consonant."""
        if self.b[i] == 'a' or self.b[i] == 'e' or self.b[i] == 'i' or self.b[i] == 'o' or self.b[i] == 'u':
            return 0
        if self.b[i] == 'y':
            if i == self.k0:
                return 1
            else:
                return (not self.cons(i - 1))
        return 1

    def m(self):
        """m() measures the number of consonant sequences between k0 and j.
        if c is a consonant sequence and v a vowel sequence, and <..>
        indicates arbitrary presence,

           <c><v>       gives 0
           <c>vc<v>     gives 1
           <c>vcvc<v>   gives 2
           <c>vcvcvc<v> gives 3
           ....
        """
        n = 0
        i = self.k0
        while 1:
            if i > self.j:
                return n
            if not self.cons(i):
                break
            i = i + 1
        i = i + 1
        while 1:
            while 1:
                if i > self.j:
                    return n
                if self.cons(i):
                    break
                i = i + 1
            i = i + 1
            n = n + 1
            while 1:
                if i > self.j:
                    return n
                if not self.cons(i):
                    break
                i = i + 1
            i = i + 1

    def vowelinstem(self):
        """vowelinstem() is TRUE <=> k0,...j contains a vowel"""
        for i in range(self.k0, self.j + 1):
            if not self.cons(i):
                return 1
        return 0

    def doublec(self, j):
        """doublec(j) is TRUE <=> j,(j-1) contain a double consonant."""
        if j < (self.k0 + 1):
            return 0
        if (self.b[j] != self.b[j-1]):
            return 0
        return self.cons(j)

    def cvc(self, i):
        """cvc(i) is TRUE <=> i-2,i-1,i has the form consonant - vowel - consonant
        and also if the second c is not w,x or y. this is used when trying to
        restore an e at the end of a short  e.g.

           cav(e), lov(e), hop(e), crim(e), but
           snow, box, tray.
        """
        if i < (self.k0 + 2) or not self.cons(i) or self.cons(i-1) or not self.cons(i-2):
            return 0
        ch = self.b[i]
        if ch == 'w' or ch == 'x' or ch == 'y':
            return 0
        return 1

    def ends(self, s):
        """ends(s) is TRUE <=> k0,...k ends with the string s."""
        length = len(s)
        if s[length - 1] != self.b[self.k]: # tiny speed-up
            return 0
        if length > (self.k - self.k0 + 1):
            return 0
        if self.b[self.k-length+1:self.k+1] != s:
            return 0
        self.j = self.k - length
        return 1

    def setto(self, s):
        """setto(s) sets (j+1),...k to the characters in the string s, readjusting k."""
        length = len(s)
        self.b = self.b[:self.j+1] + s + self.b[self.j+length+1:]
        self.k = self.j + length

    def r(self, s):
        """r(s) is used further down."""
        if self.m() > 0:
            self.setto(s)

    def step1ab(self):
        """step1ab() gets rid of plurals and -ed or -ing. e.g.

           caresses  ->  caress
           ponies    ->  poni
           ties      ->  ti
           caress    ->  caress
           cats      ->  cat

           feed      ->  feed
           agreed    ->  agree
           disabled  ->  disable

           matting   ->  mat
           mating    ->  mate
           meeting   ->  meet
           milling   ->  mill
           messing   ->  mess

           meetings  ->  meet
        """
        if self.b[self.k] == 's':
            if self.ends("sses"):
                self.k = self.k - 2
            elif self.ends("ies"):
                self.setto("i")
            elif self.b[self.k - 1] != 's':
                self.k = self.k - 1
        if self.ends("eed"):
            if self.m() > 0:
                self.k = self.k - 1
        elif (self.ends("ed") or self.ends("ing")) and self.vowelinstem():
            self.k = self.j
            if self.ends("at"):   self.setto("ate")
            elif self.ends("bl"): self.setto("ble")
            elif self.ends("iz"): self.setto("ize")
            elif self.doublec(self.k):
                self.k = self.k - 1
                ch = self.b[self.k]
                if ch == 'l' or ch == 's' or ch == 'z':
                    self.k = self.k + 1
            elif (self.m() == 1 and self.cvc(self.k)):
                self.setto("e")

    def step1c(self):
        """step1c() turns terminal y to i when there is another vowel in the stem."""
        if (self.ends("y") and self.vowelinstem()):
            self.b = self.b[:self.k] + 'i' + self.b[self.k+1:]

    def step2(self):
        """step2() maps double suffices to single ones.
        so -ization ( = -ize plus -ation) maps to -ize etc. note that the
        string before the suffix must give m() > 0.
        """
        if self.b[self.k - 1] == 'a':
            if self.ends("ational"):   self.r("ate")
            elif self.ends("tional"):  self.r("tion")
        elif self.b[self.k - 1] == 'c':
            if self.ends("enci"):      self.r("ence")
            elif self.ends("anci"):    self.r("ance")
        elif self.b[self.k - 1] == 'e':
            if self.ends("izer"):      self.r("ize")
        elif self.b[self.k - 1] == 'l':
            if self.ends("bli"):       self.r("ble") # --DEPARTURE--
            # To match the published algorithm, replace this phrase with
            #   if self.ends("abli"):      self.r("able")
            elif self.ends("alli"):    self.r("al")
            elif self.ends("entli"):   self.r("ent")
            elif self.ends("eli"):     self.r("e")
            elif self.ends("ousli"):   self.r("ous")
        elif self.b[self.k - 1] == 'o':
            if self.ends("ization"):   self.r("ize")
            elif self.ends("ation"):   self.r("ate")
            elif self.ends("ator"):    self.r("ate")
        elif self.b[self.k - 1] == 's':
            if self.ends("alism"):     self.r("al")
            elif self.ends("iveness"): self.r("ive")
            elif self.ends("fulness"): self.r("ful")
            elif self.ends("ousness"): self.r("ous")
        elif self.b[self.k - 1] == 't':
            if self.ends("aliti"):     self.r("al")
            elif self.ends("iviti"):   self.r("ive")
            elif self.ends("biliti"):  self.r("ble")
        elif self.b[self.k - 1] == 'g': # --DEPARTURE--
            if self.ends("logi"):      self.r("log")
        # To match the published algorithm, delete this phrase

    def step3(self):
        """step3() dels with -ic-, -full, -ness etc. similar strategy to step2."""
        if self.b[self.k] == 'e':
            if self.ends("icate"):     self.r("ic")
            elif self.ends("ative"):   self.r("")
            elif self.ends("alize"):   self.r("al")
        elif self.b[self.k] == 'i':
            if self.ends("iciti"):     self.r("ic")
        elif self.b[self.k] == 'l':
            if self.ends("ical"):      self.r("ic")
            elif self.ends("ful"):     self.r("")
        elif self.b[self.k] == 's':
            if self.ends("ness"):      self.r("")

    def step4(self):
        """step4() takes off -ant, -ence etc., in context <c>vcvc<v>."""
        if self.b[self.k - 1] == 'a':
            if self.ends("al"): pass
            else: return
        elif self.b[self.k - 1] == 'c':
            if self.ends("ance"): pass
            elif self.ends("ence"): pass
            else: return
        elif self.b[self.k - 1] == 'e':
            if self.ends("er"): pass
            else: return
        elif self.b[self.k - 1] == 'i':
            if self.ends("ic"): pass
            else: return
        elif self.b[self.k - 1] == 'l':
            if self.ends("able"): pass
            elif self.ends("ible"): pass
            else: return
        elif self.b[self.k - 1] == 'n':
            if self.ends("ant"): pass
            elif self.ends("ement"): pass
            elif self.ends("ment"): pass
            elif self.ends("ent"): pass
            else: return
        elif self.b[self.k - 1] == 'o':
            if self.ends("ion") and (self.b[self.j] == 's' or self.b[self.j] == 't'): pass
            elif self.ends("ou"): pass
            # takes care of -ous
            else: return
        elif self.b[self.k - 1] == 's':
            if self.ends("ism"): pass
            else: return
        elif self.b[self.k - 1] == 't':
            if self.ends("ate"): pass
            elif self.ends("iti"): pass
            else: return
        elif self.b[self.k - 1] == 'u':
            if self.ends("ous"): pass
            else: return
        elif self.b[self.k - 1] == 'v':
            if self.ends("ive"): pass
            else: return
        elif self.b[self.k - 1] == 'z':
            if self.ends("ize"): pass
            else: return
        else:
            return
        if self.m() > 1:
            self.k = self.j

    def step5(self):
        """step5() removes a final -e if m() > 1, and changes -ll to -l if
        m() > 1.
        """
        self.j = self.k
        if self.b[self.k] == 'e':
            a = self.m()
            if a > 1 or (a == 1 and not self.cvc(self.k-1)):
                self.k = self.k - 1
        if self.b[self.k] == 'l' and self.doublec(self.k) and self.m() > 1:
            self.k = self.k -1

    def stem(self, p, i, j):
        """In stem(p,i,j), p is a char pointer, and the string to be stemmed
        is from p[i] to p[j] inclusive. Typically i is zero and j is the
        offset to the last character of a string, (p[j+1] == '\0'). The
        stemmer adjusts the characters p[i] ... p[j] and returns the new
        end-point of the string, k. Stemming never increases word length, so
        i <= k <= j. To turn the stemmer into a module, declare 'stem' as
        extern, and delete the remainder of this file.
        """
        # copy the parameters into statics
        self.b = p
        self.k = j
        self.k0 = i
        if self.k <= self.k0 + 1:
            return self.b # --DEPARTURE--

        # With this line, strings of length 1 or 2 don't go through the
        # stemming process, although no mention is made of this in the
        # published algorithm. Remove the line to match the published
        # algorithm.

        self.step1ab()
        self.step1c()
        self.step2()
        self.step3()
        self.step4()
        self.step5()
        return self.b[self.k0:self.k+1]

class Node:
    def __init__(self, name, content):
        self.name = name
        self.content = content
        self.edges = set()
        self.valuesum = 0.0
    def __str__(self) -> str:
        return self.name

class WordProcessing:
    def __init__(self, filename, stem, temp, stopfile):
        self.filename = filename
        self.stem = stem
        self.temp = temp
        self.dic = {}
        self.p = PorterStemmer()
        self.biolist = []
        self.clusters = []
        self.cou = 0
        self.names = []
        self.correspond = {}
        self.stopset = set()
        if stopfile:
            stop = open("stopwords.txt", 'r')
            while True:
                line = stop.readline()
                lis = line.split()
                if not line:
                    break
                for stopword in lis:
                    self.stopset.add(stopword.lower())
            stop.close()
            # print(self.stopset)
    def procword(self):
        infile = open(self.filename, 'r')
        tempfile = open(self.temp, 'w')
        readtemp = open(self.temp, 'r')
        # stem the whole text
        name = ''
        lastline = ''
        while True:
            line = infile.readline()
            word = ''
            if not line:
                break
            if lastline == '' or lastline == '\n':
                # print(line)
                lastline = line
                word += line
                tempfile.write(word)
                continue
            if line != '\n':
                lis = line.strip().split()
                for each in lis:
                    if len(each) < 3 or each.lower() in self.stopset:
                        continue
                    # if not each[len(each) -1].isalpha():
                    #     each = each[:len(each) - 1]
                    stemmed = self.p.stem(each.lower(), 0,len(each)-1)
                    word += stemmed + " "
                    self.dic[stemmed] = 0
                    self.correspond[stemmed] = each
            lastline = line
            word += "\n"
            tempfile.write(word)
        tempfile.seek(0)
        lastline = ''
        name = ''
        wordic = {}
        end = False
        # count the occurence of remainig word in the text
        while True:
            line = readtemp.readline()
            isname = False
            if line != '\n':
                lis = line.strip().split()
                if lastline == '' or lastline == '\n':
                    isname = True
                if isname:
                    name = line.strip()
                    if name != '':
                        self.cou += 1
                        for each in wordic:
                            self.dic[each] += 1
                    if end:
                        for each in wordic:
                            self.dic[each] += 1
                        break
                    wordic = {}
                else:
                    for each in lis:
                        wordic[each] = True
            lastline = line
            if not line:
                end = True
        lastline = ''
        tempfile.seek(0)
        bio = []
        readtemp = open(self.temp, 'r')
        while True:
            line = readtemp.readline()
            isname = False
            if not line:
                break
            if line != '\n':
                lis = line.strip().split()
                if lastline == '' or lastline == '\n':
                    isname = True
                if isname:
                    if name != '':
                        node = Node(name, bio)
                        self.biolist.append(node)
                    bio = []
                    name = line.strip()
                    isname = False
                else:
                    for each in lis:
                        # discard the word that appear over 1/2 of the text
                        if self.dic[each] / self.cou < 0.5:
                            bio.append(each)
            lastline = line
        readtemp.close()
    # assign each text a value based on the summation of the weight of each word
    def assignvalue(self):
        for node in self.biolist:
            weightsum = 0.0
            for each in node.content:
                freq = self.dic[each] / len(self.biolist)
                weightsum += -1 * math.log(freq)
            node.valuesum = weightsum
        
        for node in self.biolist:
            selfname = node.name
            for other in self.biolist:
                othername = other.name
                if selfname != othername and node.valuesum + other.valuesum >= N:
                    node.edges.add(other)
                    other.edges.add(node)

    def findconnected(self):
        visited = {}
        for node in self.biolist:
            visited[node.name] = False
        for each in self.biolist:
            if visited[each.name] == False:
                temp = []
                self.clusters.append(self.DFSutil(each, visited, temp))
        
    
    def DFSutil(self, node, visited, temp):
        visited[node.name] = True
        temp.append(node)
        for edge in node.edges:
            if visited[edge.name] == False:
                temp = self.DFSutil(edge, visited, temp)
        return temp

    def findname(self):
        # print(len(self.clusters))
        for cluster in self.clusters:
            wordset = set()
            
            count = {}
            for node in cluster:
                dic = {}
                for word in node.content:
                    wordset.add(word)
                    dic[word] = True
                    if word not in count:
                        count[word] = 0

                for each in dic:
                    count [each] += 1
            
            count = dict(sorted(count.items(), key=lambda item: item[1]))
            # print(count)
            count = [(k, v) for k, v in count.items()]
            
            self.names.append((count[len(count)-1][0], count[len(count)-2][0]))
        # print(self.names)

if __name__ == '__main__':
    N = 0
    stopfile = False
    filename = ''
    for arg in sys.argv:
        if arg.isdecimal():
            N = int(arg)
        elif arg == 'stopwords.txt':
            stopfile = True
        elif arg[len(arg)-3: len(arg)] == "txt" and arg != 'stopwords.txt':
            filename = arg
    if N == 0:
        print('please give a value to N')
    else:
        stem = 'stemmed.txt'
        temp = 'temp.txt'
        wordp = WordProcessing(filename, stem, temp, stopfile)
        wordp.procword()
        wordp.assignvalue()
        wordp.findconnected()
        wordp.findname()
        total = 0
        for each in wordp.clusters:
            i = 0
            endstr = ''
            catogory1 = wordp.correspond[wordp.names[total][0]]
            if not catogory1[-1].isalpha():
                catogory1 = catogory1[:-1]
            catogory1 = catogory1[0].upper() + catogory1[1:]
            catogory2 = wordp.correspond[wordp.names[total][1]]
            if not catogory2[-1].isalpha():
                catogory2 = catogory2[:-1]
            catogory2 = catogory2[0].upper() + catogory2[1:]
            print(catogory1, "and", \
                catogory2 + ":")
            for node in each:
                original = ''
                lis = node.name.split()
                count = 0
                for word in lis:
                    original += word[0].upper() + word[1:]
                    count += 1
                    if count != len(lis):
                        original += ' '
                i += 1
                if i == len(each):
                    endstr = '\n'
                else:
                    endstr = ', '
                print(original, end = endstr)
            i = 0
            print()
            total += 1

    