from tools.solve import get_sfd, get_bmd, get_support_reactions
from tools.takeinput import set_input, validate_input
from tools.plot import plotter
from tools.report import solve_reactions, solve_sfd, solve_bmd
from termcolor import colored
import numpy as np
import matplotlib.pyplot as plotting
import math
import sys

def sfd_bmd(values, axis):
    if(validate_input(values)):
        loads = []
        moments = []
        positions = []
        span = values.get('span')
        position = 0
        reactions = get_support_reactions(values)
        if(len(reactions)==2):
            reaction1 = reactions[0]
            reaction2 = reactions[1]
        if(len(reactions)==1):
            reaction = reactions[0]
        while (position<=float(span)):
            load = 0
            moment = 0
            if(len(reactions)==2):
                if(position>=float(reaction1[2])):
                    load += float(reaction1[1])
                if(position<=float(reaction1[2])):
                    moment += float(reaction1[1])*(float(reaction1[2])-position)
                if(position>=float(reaction2[2])):
                    load += float(reaction2[1])
                if(position<=float(reaction2[2])):
                    moment += float(reaction2[1])*(float(reaction2[2])-position)
            elif(len(reactions)==1):
                if(position>=float(reaction[2])):
                    load = get_sfd(values, float(values.get('span')))
                if(position<=float(reaction[2])):
                    moment = float(reaction[1])
            loads.append(load-get_sfd(values, position))
            moments.append(moment-get_bmd(values, position))
            positions.append(position)
            position+=float(span)/100
        print(axis)
        solve_reactions(values)
        solve_sfd(values)
        plotter(loads, positions, 'Shear force', axis)
        solve_bmd(values)
        plotter(moments, positions, 'Bending Moment', axis)
    return positions, loads, moments

def plot_resultant(positions, xvalues, yvalues, diagram):
    resultant_values = []
    for x, y in zip(xvalues, yvalues):
      resultant = math.sqrt((x**2)+(y**2))
      resultant_values.append(resultant)

    fig = plotting.figure('Resultant ' + diagram + ' diagram')
    plotting.title('Resultant' + diagram +  ' diagram')
    plotting.xlabel('Position along length of the member (m) ->')

    if diagram == 'Shear force':
        plotting.ylabel('Resultant ' + diagram + '(N) ->')
    else:
        plotting.ylabel('Resultant ' + diagram + '(Nm) ->')

    plotting.plot(positions, resultant_values)
    plotting.grid()
    fig.savefig('/content/pySA/image/' + 'Resultant ' + diagram + ' diagram' + '.png')

def main():

    user_input = set_input(sys.argv)
    xaxis = sfd_bmd(user_input[0], 'xaxis')
    yaxis = sfd_bmd(user_input[1], 'yaxis')
    plot_resultant(xaxis[0], xaxis[1], yaxis[1], 'Shear force')
    plot_resultant(xaxis[0], xaxis[2], yaxis[2], 'Bending moment')
