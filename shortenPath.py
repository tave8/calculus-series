def shortenPath(path):
    # Write your code here.
        
    # case: path starts with /
    # case: path starts with ./

    # split path by /
    # tokens = path.split("/")
    # for token in tokens:
    #     # if there's nothing in the stack,
    #     # and the token is root path, then this is the root path
    #     # otherwise it's not root
    tokenStack = getTokens(path)
    # print("PATH: ", path)
    # print("------------------")

    for token in tokenStack:
        print("token: ", token)
    # print()
    # print()

    simplifyTokenStack(tokenStack)




def simplifyTokenStack(tokenStack):
    tokensReversed = []
    # print(tokenStack)
    # consume the stack, accumulating the
    # tokens inside of it
    reachedRoot = False
    while not reachedRoot and len(tokenStack) > 0:
        token = tokenStack[-1]
        
        # / and /. don't add meaning, just pop
        # off the stack
        if token["token"] in ["/", "/."]:
            tokenStack.pop()

        # it's not a directory token, so 
        # add it the simplified path
        elif not token["isDir"]:
            tokensReversed.append(token["token"])
            tokenStack.pop()

        # go up to previous directory
        elif token["token"] == "/..":
            tokenStack.pop()
            
            countMoveUpParent = 1

            # go back in the stack until there are elements
            # in the stack AND the moveup parent operations
            # are not completed
            while len(tokenStack) > 0 and countMoveUpParent != 0:
                # if the stack peek is yet another 
                # moveup parent token, accumulate
                # these moveup parent operations
                # in the counter
                if tokenStack[-1]["token"] == "/..":
                    countMoveUpParent += 1

                elif not tokenStack[-1]["isDir"]:
                    tokensReversed.append(tokenStack[-1]["token"])
                    countMoveUpParent -= 1
                
                elif tokenStack[-1]["isRoot"]:
                    reachedRoot = True
                    break
                # always remove the current
                # stack peek
                tokenStack.pop()
                

            # while 
            pass
            # reachedRoot = True
        elif token["isRoot"]:
            reachedRoot = True
        else:
            reachedRoot = True

        
        # print(tokenStack)
        
    print("".join(list(reversed(tokensReversed))))
    # return reversed(tokensReversed)



def getTokens(path):

    # if path starts with exactly /, it's an absolute path
    # otherwise it's a relative path

    # iterate through the path
    # if this char is /, find the next,
    # and get all the chars between this / and the next / (if it exists)
    # including the left-most / and excluding the right-most /
    tokens = []
    i = 0

    while i < len(path):
        char = path[i]
        # assume index i is jumping by one index
        jump = 1


        # we've found a slash, so now 
        # we must find the next slash, and get all the 
        # characters in between, including the first slash (this one)
        # and excluding the next one
        # example:
        #        /foo/bar/../baz
        #        ^   ^
        #        |   |
        #        | found next slash
        #    found slash
        if char == "/":
            # skip this character, because we've just said
            # it's a slash
            j = i+1
            # so include the slash 
            token = "/"
            # once we're sure we are in the path's index boundaries
            # keep on iterating until the first non-slash character is met
            # example:
            # 
            # loop 1:
            #        /foo/bar/../baz
            #        ^^
            #        ||--- j
            #        | 
            #        i

            # loop 2:
            #        /foo/bar/../baz
            #        ^ ^
            #        | |--- j
            #        | 
            #        i
        
            # loop 3:
            #        /foo/bar/../baz
            #        ^  ^
            #        |  |--- j
            #        | 
            #        i
                
            while j < len(path) and path[j] != "/":
                # append all non-slash characters 
                token += path[j]
                # increase j
                # note: when we found the last non-slash character, 
                # we still increase j. this means that the j in the next loop
                # will point to the next slash
                j += 1
            # print(token)
            # append the non-slash characters from the first slash (included)
            # to the next slash (excluded)
            isRoot = False
            if len(tokens) == 0:
                isRoot = True

            tokens.append(
                constructTokenInfo(isRoot=isRoot, token=token, isDir=isDirToken(token))
            )
            # jump index i to the next slash, which is pointed at by index j
            # example:
            #        /foo/bar/../baz
            #        ^   ^
            #        |   |--- j=4
            #        | 
            #        i=0

            #        |---|
            #        jump=4    
            jump = j-i
            
            # example:
            #  loop 1
            #        /foo/bar/../baz
            #            ^
            #            |--- i=j=4
            #  loop 2
            #        /foo/bar/../baz
            #                ^
            #                |--- i=j=8
            #  loop 3
            #        /foo/bar/../baz
            #                   ^
            #                   |--- i=j=11
            #  loop 4
            #        /foo/bar/../baz
            #                       ^
            #                       |--- i=j=15
            i += jump


        # at the very beginning, there might be no slash
        # the first slash might present itself when we've already
        # iterated past some characters
        # example
        #   ../foo/bar
        #   ../../bar
        #   ./foo/bar
        #   baz/foo/bar
        elif char != "/" and len(tokens) == 0:
            # print("token at path start: ", char)

            #   ../foo/bar
            #    ^
            #    |
            #    k   
            # tokens.append("./")
            k = i+1
            # add the char to the token
            token = f"{char}"

            #   ../foo/bar
            #     ^
            #     |
            #     k   
            while k < len(path) and path[k] != "/":
                # keep on appending this non-slash char 
                # to the token
                token += path[k]
                k += 1
            
            # when this while loop is done,
            # index k will point to the next first slash
            tokens.append(
                constructTokenInfo(isRoot=False, token=token, isDir=isDirToken(token))
            )
            # jump index i to the first slash
            i += k

    return tokens


def constructTokenInfo(isRoot, token, isDir):
    return {
        "isRoot": isRoot,
        "token": token,
        "isDir": isDir
    }


# for a token to be a "directory token",
# it must contain dots and slashes only
def isDirToken(token):
    for char in token:
        if char not in [".", "/"]:
            return False
    return True


# res = shortenPath("/foo/../test/../test/../foo//bar/./baz/")
res = shortenPath("../../a/../../b/../c//d/./e/") # ../../../c/d/e
# res = shortenPath("../foo/../test/../test/../foo//bar/./baz/")
# res = shortenPath("./foo/../test/../test/../foo//bar/./baz/")
# res = shortenPath("/foo/../test/../test/../foo//bar/./baz/")
# res = shortenPath("foo/../test/../test/../foo//bar/./baz/")
# res = shortenPath("foo/../test/../test/../foo//bar/./baz/")
# res = shortenPath("/../test/../test/../foo//bar/./baz/")

# res = shortenPath("/foo/bar/../baz")
# print(res)







