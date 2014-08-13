__author__ = 'juliewe'



class Sentence:

    def __init__(self):

        self.tokens=['*','man','loves','woman','!']

class HMM:

    def __init__(self):

        self.states=['S','N','V','E']
        self.transitions={}
        self.transitions['S']={'S':0,'N':0.5,'V':0.5,'E':0}
        self.transitions['N']={'S':0,'N':0.3,'V':0.4,'E':0.3}
        self.transitions['V']={'S':0,'N':0.8,'V':0.1,'E':0.1}
        self.transitions['E']={'S':0,'N':0,'V':0,'E':0}
        self.emissions={}
        self.emissions['N']={'man':0.5,'loves':0.1,'woman':0.4}
        self.emissions['V']={'man':0.2,'loves':0.7,'woman':0.1}
        self.emissions['S']={'*':1}
        self.emissions['E']={'!':1}
        self.viterbiprobs={}
        #self.backpointers={}

    def decode(self,sent):
        self.sentence=sent

        #initialise

        for i,token in enumerate(self.sentence.tokens):
            self.viterbiprobs[i]={}
            #self.backpointers[i]={}
            for j,state in enumerate(self.states):
                self.viterbiprobs[i][j]=(0,-1)
                #self.backpointers[i][j]=-1

        #forwards

        for i,token in enumerate(self.sentence.tokens):

            for j,state in enumerate(self.states):

                if i==0:
                    self.viterbiprobs[i][j]=(self.emissions[state].get(token,0),-1)
                else:
                    listprobs=[]
                    for k,prevstate in enumerate(self.states):
                        prob = self.viterbiprobs[i-1][k][0]*self.transitions[prevstate][state]*self.emissions[state].get(token,0)
                        listprobs.append((prob,k))
                    listprobs.sort(reverse=True)
                    self.viterbiprobs[i][j]=listprobs[0]



        #backwards

        currentstate=-1
        maxprob=0
        statesequence=[]
        index=len(self.sentence.tokens)-1
        for j,state in enumerate(self.states):
            if self.viterbiprobs[index][j][0]>maxprob:
                maxprob=self.viterbiprobs[index][j][0]
                currentstate=j


        while currentstate!=-1:
            statesequence.append(self.states[currentstate])
            currentstate=self.viterbiprobs[index][currentstate][1]
            index-=1

        statesequence.reverse()

        print statesequence
        print maxprob



    def beamdecode(self,sent,beam):
        self.sentence=sent

        #initialise

        for i,token in enumerate(self.sentence.tokens):
            self.viterbiprobs[i]={}
            #self.backpointers[i]={}
            for j,state in enumerate(self.states):
                self.viterbiprobs[i][j]=[(0,-1,-1)]
                #self.backpointers[i][j]=-1

        #forwards

        for i,token in enumerate(self.sentence.tokens):

            for j,state in enumerate(self.states):

                if i==0:
                    self.viterbiprobs[i][j]=[(self.emissions[state].get(token,0),-1,-1)]
                else:
                    listprobs=[]
                    for k,prevstate in enumerate(self.states):
                        for pos,tuple in enumerate(self.viterbiprobs[i-1][k]):
                            prob = self.viterbiprobs[i-1][k][pos][0]*self.transitions[prevstate][state]*self.emissions[state].get(token,0)
                            listprobs.append((prob,k,pos))
                    listprobs.sort(reverse=True)

                    self.viterbiprobs[i][j]=listprobs[0:beam]



        #backwards
        index=len(self.sentence.tokens)-1
        listprobs=[]
        for j,state in enumerate(self.states):
            for pos,tuple in enumerate(self.viterbiprobs[index][j]):
                listprobs.append((tuple,j,pos))
        listprobs.sort(reverse=True)


        for sequence in listprobs[0:beam]:

            statesequence=[]
            index=len(self.sentence.tokens)-1
            currentstate=sequence[1]
            currentpos=sequence[2]

            while currentstate!=-1:
                statesequence.append(self.states[currentstate])
                nextstate=self.viterbiprobs[index][currentstate][currentpos][1]
                nextpos=self.viterbiprobs[index][currentstate][currentpos][2]
                currentstate=nextstate
                currentpos=nextpos
                index-=1

            statesequence.reverse()

            print statesequence
            print sequence[0][0]


if __name__=='__main__':
    myHMM=HMM()
    mySentence=Sentence()
    myHMM.beamdecode(mySentence,3)



