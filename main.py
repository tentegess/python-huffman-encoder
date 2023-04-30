import sys
import pickle

class Node:
    '''
    Class representing a tree element
    :param symbol: the symbol found in the leaf
    :param freq: number of occurrences of a symbol
    :param left: descendant turning left
    :param right: descendant turning right
    '''
    def __init__(self, symbol, freq):
        '''
        Class constructor
        :param symbol: the symbol contained in the leaf
        :param freq: number of occurrences of the symbol
        '''
        self.symbol = symbol
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        '''
        Method for sorting subtrees
        :param other: object to be compared during sorting
        '''
        return self.freq < other.freq

def open_data(path, mode):
    '''
    function that reading the contents of a file
    :param path: path to file
    :param mode: mode of reading file
    :return: file content
    '''
    with open(path, mode) as file:
        data=file.read()
    return data 

def count_signs(data):
    '''
    function which calculates the number of occurrences of a given character in a string
    :param data: string of characters
    :return: dictionary containing the symbol as key and the number of occurrences as value
    '''
    signs=set(data)                                         #creation of a character set from a string
    dic={k : data.count(k) for k in signs}                  #creating a dictionary from a set of characters
    return dict(sorted(dic.items(), key=lambda x: x[1]))    #return a sorted dictionary
                                                            # by the number of occurrences of a character

def build_tree(sym_freq):
    '''
    function creating a huffman tree
    :param sym_freq: dictionary containing character frequency
    :return: root of the tree
    '''
    nodes=[Node(symbol,freq) for symbol, freq in sym_freq.items()]  #list of n independent trees
    nodes.sort()
    while len(nodes)>1:                        #repeating the operation until
                                               #there is 1 item left in the list
                                               
        left, right=nodes.pop(0),nodes.pop(0)  #drawing the pair of trees with
                                               #the smallest number of occurrences
                                               
        parent=Node(None,left.freq+right.freq) #creation of a subtree with the total number
                                               #of occurrences of descendant elements
                                               
        parent.left, parent.right=left,right   #adding descendant elements
                                               #to the created subtree
                                               
        nodes.append(parent)                   #adding a subtree to the list
        nodes.sort()                           #sorting the tree list
    
    return nodes[0]

codes_dict=dict()   #dictionary with codes for individual characters

def huffman_codes(node,code=''):
    '''
    function which calculates the codes of the individual symbols
    :param node: root of the tree
    :param code: fragment of code under construction
    '''
    if node.symbol is not None:    #if the descendant contains a symbol assign the code
            codes_dict[node.symbol] = code
            return
    huffman_codes(node.left, code + '0')  #0 for the code in the left node
    huffman_codes(node.right, code + '1') #1 for the code in the right node
     
def encode(data):
    '''
    string encoding function
    :param data: string
    :return: compressed string
    '''
    output=''
    for char in data:
        output+=codes_dict[char]
    return output

def save_to_file(output):
    '''
    function writing compressed data and code array to file
    :param output: compressed string 
    '''
    with open('compressed.bin', 'wb') as f: #saving the data as a binary file
                                            #by retrieving the following 8 characters from the data in a loop
                                            #and saving to file as a hexadecimal number
        f.write(bytes(int(output[i:i + 8], 2) for i in range(0, len(output), 8)))
        pickle.dump([f'{byte}:{value}' for byte, value in  codes_dict.items()],f)           
                                            #serialisation and insertion  
                                            #of a code table at the end of the file







if __name__ == '__main__':
    mode=input(
    '''
    select file type
    ____________________
    1. txt
    2. binary
    ''')
    match mode:
        case "1":
            data=open_data(sys.argv[1],"r")
        case "2":
            data=open_data(sys.argv[1],"rb")
        case _:
            print("wrong command")
            exit()
    
    sym_freq=count_signs(data)
    root=build_tree(sym_freq)
    print("an array of character occurrences:",sym_freq)
    huffman_codes(root)
    print("code board:",codes_dict)
    compressed_output=encode(data)
    print("encoding result:",compressed_output)
    save_to_file(compressed_output)
    
 
