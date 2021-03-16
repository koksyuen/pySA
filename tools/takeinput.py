from termcolor import colored

def get_input(param_name):
    ''' Takes input from the user '''

    interact = colored('Please enter the value of the parameter', 'green') + ', ' + colored(param_name, 'red') + ':'
    param = input(interact)
    return param


def set_input(args):
    ''' Returns a dict input_values containing all input values '''

    input_values = argshandler(args)
    return input_values

def get_support_value(supports):
    ''' Returns the total support value '''

    support_value = 0
    for support in supports:
        if(support[0]=='pin'):
            support_value +=1
        elif(support[0]=='fixed'):
            support_value +=3
        elif(support[0]=='roller'):
            support_value +=7

    return support_value

def validate_input(input_values):
    ''' Validates input based on support input '''

    supports = input_values.get('supports')
    span = input_values.get('span')
    if(len(supports)>2):
        return False
    for support in supports:
        if(support[0]=='pin'):
            pass
        elif(support[0]=='fixed'):
            pass
        elif(support[0]=='roller'):
            pass
        else:
            return False

        if(float(support[2])>float(span)):
            return False
    support_value = get_support_value(supports)
    if(support_value in (2,3,8,14)):
        pass
    else:
        return False
    return True

def argshandler(args):
    x_input_values = {}
    y_input_values = {}
    for arg in args:
        if '-l=' in arg:
            x_input_values.update({'span':int(arg[3:])})
            y_input_values.update({'span':int(arg[3:])})
        elif '-sx=' in arg:
            x_input_values.update({'supports':listconvert(arg[4:])})
        elif '-px=' in arg:
            x_input_values.update({'point_loads':listconvert(arg[4:])})
        elif '-ux=' in arg:
            x_input_values.update({'UDLs':listconvert(arg[4:])})
        elif '-sy=' in arg:
            y_input_values.update({'supports':listconvert(arg[4:])})
        elif '-py=' in arg:
            y_input_values.update({'point_loads':listconvert(arg[4:])})
        elif '-uy=' in arg:
            y_input_values.update({'UDLs':listconvert(arg[4:])})
    return x_input_values, y_input_values

def listconvert(string):

    bracket_count = 0
    input_list = []
    list_element = []
    element = ''
    for piece in string:
        if piece == '[':
            bracket_count+=1
        elif piece == ']':
            bracket_count-=1
        elif bracket_count == 1 and not piece==',':
            element += piece
        elif bracket_count ==1 and piece ==',':
            list_element.append(element)
            element =''
        if bracket_count == 0 and not piece==',':
            list_element.append(element)
            input_list.append(list_element)
            element = ''
            list_element = []

    return input_list

def fileconvert(textfile):

    input_values = {}
    f = open(textfile, 'r')
    lines = f.readlines()
    for line in lines:
        if 'span=' in line:
            input_values.update({'span':line.strip('span=')[:-1]})
        elif 'point_loads=' in line:
            input_values.update({'point_loads':listconvert(line.strip('point_loads=')[:-1])})
        elif 'UDLs=' in line:
            input_values.update({'UDLs':listconvert(line.strip('UDLs=')[:-1])})
        elif 'supports=' in line:
            input_values.update({'supports':listconvert(line.strip('supports=')[:-1])})

    return input_values
