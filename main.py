import sys
columns=[]
items=[]
test=[]
results={}
fp=tp=tn=0
class attribs:
    def __init__(self,col):
        self.counts={}
        self.col=col
    def insert(self,value,result):#counts={"x":{"e":1,"p":1}}
        if value !="?":
            if value not in self.counts:
                self.counts[value]={}
            if result not in self.counts[value]:
                self.counts[value][result]=0
            self.counts[value][result]+=1
    def probFor(self,value,result):
        resCount=results[result]
        if value not in self.counts or result not in self.counts[value]:
            return 1/(resCount+len(self.counts))
        return self.counts[value][result]/resCount

def getProb(result,attribs):
    val=results[result]/len(items)
    for i in range(len(attribs)):
        if attribs[i]!="?":
            val*=columns[i].probFor(attribs[i],result)/results[result]
    return val

def getResult(attribs):
    if getProb(list(results.keys())[0],attribs)>getProb(list(results.keys())[1],attribs):
        return list(results.keys())[0]
    return list(results.keys())[1]


class item:
    def __init__(self,line,learn=False):
        global fp,tp,tn
        self.result=line.split(",")[0]
        self.attribs=line.split(",")[1:]
        if learn:
            if self.result not in results:
                results[self.result]=0
            results[self.result]+=1
            if len(columns)==0:
                for i in range(1,len(self.attribs)+1):
                    columns.append(attribs(i))
            for i in range(0,len(columns)):
                columns[i].insert(self.attribs[i],self.result)
        else:
            res=getResult(self.attribs)
            if self.result=="e" and res=="p":
                fp+=1
            elif self.result=="p" and res=="p":
                tp+=1
            elif self.result=="e" and res=="e":
                tn+=1
def readTo(file,l,learn=False):
    with open(file) as file:
        for line in file:
            l.append(item(line.rstrip(),learn))

if __name__ == "__main__":
    readTo(sys.argv[1],items,True)
    readTo(sys.argv[2], test)
    print("Accuracy: {}".format(tp/len(test)))
    pr=tp / (tp+fp)
    print("Precision: {}".format(pr))
    rc=tp / (tp + fp)
    print("Recall: {}".format(rc))
    print("F-Measurement: {}".format(2*(pr*rc)/(pr+rc)))
#positive=poisonous
#accuracy=truepositive/totalitems
#precision=truepositive/(truepositive+falsepositive)
#recall=truepositive/truepositive+falsenegative
#f-measurement=2 * (precision * recall) / (precision + recall)