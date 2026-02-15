TableData = [['apples', 'oranges', 'cherries', 'banana'],
['Alice', 'Bob', 'Carol', 'David'],
['dogs', 'cats', 'moose', 'goose']]

def printTable(pTableData):
    
    # Adjusting columns widths according to largest string in each list
    
    ColWidths = [0]*len(pTableData)
    outTableData = []
    
    for i in range(len(pTableData)):
        ColWidths[i] =  len(max(pTableData[i],key = len))
    
    for i in range(4):
        AdjustedCol = []
        
        for j in range(len(pTableData)):
            AdjustedCol.append(pTableData[j][i].rjust(ColWidths[j]," "))
    
        outTableData.insert(i,"\t".join(AdjustedCol))
        
    return outTableData
    
for row in printTable(TableData):
    print(row)
