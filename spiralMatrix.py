"""
Traverse matrix in spiral order.

Get the elements of a n*m matrix in spiral order.

O(n*m) time | O(1) space

author: Giuseppe 
"""

spiralMovesOrdered = [
    "right",
    "down",
    "left",
    "up"
]

def spiralTraverse(array, config):
    """
    Main function.
    
    :param array: list
    :param config: dict {outputType: str: flat | nested}
    """

    ret = []
    
    # we get the iterator once
    iterSpiralMove = getNextSpiralMove()

    # when indicating start and end, here we mean both INCLUSIVE
    rowStart = 0
    rowEnd = len(array)-1
    colStart = 0
    colEnd = len(array[0])-1

    # keep "shrinking" the matrix until the indexes
    # don't overlap
    while colStart <= colEnd  and rowStart <= rowEnd:

        # each move takes up all the remaining space
        # in that direction, in this fashion:
        # ----------->
        # ^          |
        # |          |
        # |          |
        # <--------- v

        
        # STEP 1: START

        # how the row and column indexes look like 
        # at the very beginning
        # 
        #   colStart   colEnd
        #     |          |
        #     v          v
        #     ----------->   <-- rowStart
        #     ^          |
        #     |          |
        #     |          |
        #     <--------- v   <-- rowEnd
        # 

        # MOVE RIGHT

        # ...after we move right, we move rowStart forward
        # 
        #   colStart   colEnd
        #     |          |
        #     v          v
        #     ----------->   <-- (moved in this row) (previous ignored rowStart index)
        #     ^          |   <-- rowStart
        #     |          |
        #     |          |
        #     <--------- v   <-- rowEnd
        # 

        # MOVE DOWN

        # ...after we move down, we move colEnd backward
        #            
        #            colEnd
        #              |
        #   colStart   | ------ (moved in this col) 
        #     |        | |    
        #     v        v v    
        #     ----------->     
        #     ^          |   <-- rowStart
        #     |          |
        #     |          |  
        #     <--------- v   <-- rowEnd 
        # 

        # MOVE LEFT

        # ...after we move left, we move rowEnd backward
        # 
        #            colEnd
        #   colStart   | 
        #     |        |         
        #     v        v     
        #     ----------->      
        #     ^          |   <-- rowStart
        #     |          |
        #     |          |   <-- rowEnd
        #     <--------- v   <-- (moved in this row)
        # 

        # MOVE UP

        # ...after we move up, we move colStart forward
        # 

        # (moved in this col) 
        #  |
        #  |          
        #  |   colStart 
        #  |     |      
        #  |---  |     -- colEnd  
        #     |  |     |         
        #     v  v     v     
        #     ----------->          
        #     ^          |   <-- rowStart
        #     |          |
        #     |          |   <-- rowEnd
        #     <--------- v
        # 

        # AFTER FIRST ROUND OF MOVES
        # the matrix will "get smaller", 
        # and we will do the same process with the
        # resulting submatrix - without creating a new submatrix in memory
        # - we just use the indexes!

        # NOTE:
        # in reality, because the submatrix is defined with indexes,
        # the program consider those indexes, of course.
        # however in this drawings, I've maintained the previous index 
        # and the new index only for teaching reasons, ONLY to show you the VISUAL difference,
        # but internally, the program doesn't know what the previous ignored index is, just the current one

        #     colStart 
        #       |      
        #       |    colEnd
        #       |     |         
        #       v     v     
        #     ----------->          
        #     ^          |   <-- rowStart
        #     |          |
        #     |          |   <-- rowEnd
        #     <--------- v   
        # 

        # RESULTING SUBMATRIX = START FROM STEP 1
        
        #     colStart 
        #       |      
        #       |    colEnd
        #       |     |         
        #       v     v     
        #       ------>  <-- rowStart        
        #       ^     v  
        #       <------  <-- rowEnd
        # 
        
        
        
        # MOVES
        # when we modify the rowStart and colStart indexes,
        # we are effectively saying "the numbers of that row or column have been 
        # visited, so move to the next/previous row or column
        # the next or previous depend on the meaning of + or - 1 
        # for example, when i move right and increase the rowStart by 1, 
        # it means "the elements in this row have been visited, move to the row
        # with index equal the current index + 1"

        # the ASSUMPTION is that with each move (right, down etc.)
        # we are visiting ALL the remaining numbers in that move.

        # the iterator
        currMove = next(iterSpiralMove)
        
        getNumbersInMoveAndAppendTo(array, currMove, {
            "colStart": colStart,
            "colEnd": colEnd,
            "rowStart": rowStart,
            "rowEnd": rowEnd 
        }, ret, config)
        
        # if current move is right, next move is down
        # ----------->
        if currMove == "right":
            # for example, if rowStar was previously 0, it means that
            # by moving right, we've visited all the numbers in the first row
            # so we increase rowStart
            rowStart += 1
            
        # if current move is down, next move is left
        #  |
        #  |
        #  |
        #  V
        elif currMove == "down":
            # for example, if colEnd was previously 0, it means that
            # by moving down, we've visisted all the numbers in colEnd,
            # so we decrease colEnd
            colEnd -= 1

        # if current is left, next move is up
        # <-------------
        elif currMove == "left":
            # for example, if rowEnd was previously len(matrix), it means that
            # by moving left, we've visisted all the numbers in the last row
            rowEnd -= 1

        # if current is up, move round is complete
        #  ^
        #  |
        #  |
        #  |
        elif currMove == "up":
            colStart += 1

    
    return ret
            

def getNumbersInMoveAndAppendTo(matrix, move, indexes, arrayToAppend, config):
    if (not "outputType" in config) or (config["outputType"] == "flat"):
        arrayToAppend.extend(
            getNumbersInMove(matrix, move, indexes)
        )

    elif config["outputType"] == "nested":
        arrayToAppend.append(
            getNumbersInMove(matrix, move, indexes)
        )
    
    elif config["outputType"] == "nestedInfo":
        numbers = getNumbersInMove(matrix, move, indexes)
        arrayToAppend.append({
            "indexes": indexes,
            "numbers": numbers,
            "move": move
        })

    else:
        raise Exception(f"outputType {config["outputType"]} not recognized")





def getNumbersInMove(matrix, move, indexes):
    
    colStart = indexes["colStart"]
    colEnd = indexes["colEnd"]
    rowStart = indexes["rowStart"]
    rowEnd = indexes["rowEnd"]

    # print(f"move: {move.upper()}") 
    # print(f"colStart: {colStart} | colEnd: {colEnd} | rowStart: {rowStart} | rowEnd: {rowEnd}")
    # print()

    # for each move, consider only the relevant indexes
    # that means, not all indexes are relevant for each move
    
    # to move right, the relevant input is:
    # rowTarget, colStart, colEnd, move forward
    if move == "right":
        res = getNumbersInRow(
            matrix, 
            # when we move right, we are interested in the rowStart row
            rowStart,
            colStart,
            colEnd+1,
            "forward"
        )
        # print(res)
        return res

    # to move down, the relevant input is:
    # colTarget, rowStart, rowEnd, move forward
    elif move == "down":
        res = getNumbersInCol(
            matrix, 
            # when we move down, we are interested in the colEnd col
            colEnd,
            rowStart,
            rowEnd+1,
            "forward"
        )
        # print(res)
        return res
    
    # to move left, the relevant input is:
    # rowTarget, colStart, colEnd, move backward
    elif move == "left":
        res = getNumbersInRow(
            matrix, 
            # when we move left, we are interested in the rowEnd row
            rowEnd,
            colStart,
            colEnd+1,
            "backward"
        )
        # print(res)
        return res

    # to move up, the relevant input is:
    # colTarget, rowStart, rowEnd, move backward
    elif move == "up":
        res = getNumbersInCol(
            matrix, 
            # when we move up, we are interested in the colStart col
            colStart,
            rowStart,
            rowEnd+1,
            "backward"
        )
        # print(res)
        return res

    else:
        raise Exception(f"move {move} not recognized")
    




def getNextSpiralMove():
    idx = 0
    while True:
        # examples:
        # 3 % 4 = 3
        # 4 % 4 = 0
        # 5 % 4 = 1
        idxModded = idx % (len(spiralMovesOrdered))
        yield spiralMovesOrdered[idxModded]
        idx += 1

    
# indexStart is included
# indexEnd is excluded
# example: 
#   iterateRow(matrix, 0, 0, len(array[0]), "forward")
#     moves in the entire array at matrix[0] forward
#   iterateRow(matrix, 0, 0, len(array[0]), "backward")
#     moves in the entire array at matrix[0] backward
def getNumbersInRow(matrix, indexRow, indexStart, indexEnd, direction):
    ret = []
    # get the row at the given index
    row = matrix[indexRow]
    # forward
    if direction == "forward":
        for i in range(indexStart, indexEnd):
            # the current number
            num = row[i]
            ret.append(num)
    # backward
    elif direction == "backward":
        # because indexEnd was excluded, we now need to include it
        #   because it's the index start
        # because indexStart was included, we now need to exclude it,
        #   because it's the index end
        for i in range(indexEnd-1, indexStart-1, -1):
            # the current number
            num = row[i]
            ret.append(num)
    
    return ret


def getNumbersInCol(matrix, indexCol, indexStart, indexEnd, direction):
    ret = []
    # forward
    if direction == "forward":
        # iterate through rows
        for indexRow in range(indexStart, indexEnd):
            # current number
            num = matrix[indexRow][indexCol]
            ret.append(num)
    # backward 
    elif direction == "backward":
        # iterate through rows
        for indexRow in range(indexEnd-1, indexStart-1, -1):
            # current number
            num = matrix[indexRow][indexCol]
            ret.append(num)
    
    return ret



def printResults(matrix):

    resFlat = spiralTraverse(matrix, {
        "outputType": "flat"
    })
    
    resNested = spiralTraverse(matrix, {
        "outputType": "nested"
    })

    resNestedInfo = spiralTraverse(matrix, {
        "outputType": "nestedInfo"
    })

    print()

    print("> Flat list")
    # print flat
    print(resFlat)
    print()

    print("> Nested list")
    # print nested
    for arr in resNested:
        print(arr)
    print()

    print("> List with info")
    # print nested info
    for info in resNestedInfo:
        print(info)
    print()


matrix1 = [
# col:   0   1   2   3   4     row:
        [1,  2,  3,  4,  5],   # 0 
        [6,  7,  8,  9,  10],  # 1 
        [11, 12, 13, 14, 15],  # 2
        [16, 17, 18, 19, 20],  # 3
        [21, 22, 23, 24, 25],  # 4
        [26, 27, 28, 29, 30]   # 5
]

matrix2 = [
    [1, 2, 3],
    [4, 5, 6],
]

printResults(matrix1)

