# Game.py
# Code to simulate the Shell Game and respective strategies

import numpy as np
from tqdm import tqdm
from matplotlib import pyplot as plt

NUMCUPS = 3
MINSWAPS = 2
MAXSWAPS = 16
NUMITERS = 500000

def printCurrPos(currPos: int):

    posString = ""
    for cup in range(1, NUMCUPS + 1):
        posString += "x" if cup == currPos else "_"
    print(posString)

def playGame(numSwaps: int = None, printFlag: bool = False):

    # Choose initial cup & number of swaps
    initPos = np.random.randint(1, NUMCUPS + 1)
    if not numSwaps:
        numSwaps = np.random.randint(MINSWAPS, MAXSWAPS + 1)

    # Swap cups correct number of times
    currPos = initPos
    for _ in range(numSwaps):
        
        if printFlag:
            printCurrPos(currPos)

        nextPos = currPos
        while nextPos == currPos:
            nextPos = np.random.randint(1, NUMCUPS + 1)
        
        currPos = nextPos
    
    if printFlag:
        printCurrPos(currPos)
    return initPos, numSwaps, currPos

def randomGuessStrat(numSwaps: int):

    numCorrect = 0
    for _ in tqdm(range(NUMITERS)):
        start, swaps, end = playGame(numSwaps, False)
        guess = np.random.randint(1, NUMCUPS + 1)
        if guess == end:
            numCorrect += 1
    
    accuracy = numCorrect / NUMITERS
    return accuracy

def smartGuessStrat(numSwaps: int):

    numCorrect = 0
    for _ in tqdm(range(NUMITERS)):
        start, swaps, end = playGame(numSwaps, False)

        guess = start
        if swaps % 2 == 1:
            while guess == start:
                guess = np.random.randint(1, NUMCUPS + 1)

        if guess == end:
            numCorrect += 1
    
    accuracy = numCorrect / NUMITERS
    return accuracy

def plotStrategies(savefile: str):

    numSwapRange = np.arange(MINSWAPS, MAXSWAPS + 1)
    randomGuessAccs, smartGuessAccs = list(), list()

    # Generate accuracies
    for numSwaps in numSwapRange:
        randomGuessAccs.append(randomGuessStrat(numSwaps))
        smartGuessAccs.append(smartGuessStrat(numSwaps))
    
    fig = plt.figure(figsize=(16, 9))
    plt.plot(numSwapRange, randomGuessAccs, 'o-', label="Random Guessing Strategy")
    plt.plot(numSwapRange, smartGuessAccs, 'o-', label="Smart Guessing Strategy")

    # Add xticks and yticks
    ax = plt.gca()
    ax.set_xticks(numSwapRange)
    ax.set_xticklabels([str(x) for x in numSwapRange])
    ax.set_yticks(np.arange(0.3, 0.55, 0.01))
    ax.set_yticklabels([f"{round(100 * x)}" for x in np.arange(0.3, 0.55, 0.01)])

    plt.legend(loc=7,fontsize='large', edgecolor='white')
    plt.title("Accuracies of Smart Strategy vs Random Guessing Strategy", fontsize='xx-large')
    plt.xlabel("Number of Swaps", fontsize='x-large')
    plt.ylabel("Guessing Accuracy Percentage", fontsize='x-large')

    fig.savefig(savefile)


def main():

    plotStrategies("plots/accuracyPlot_3cupslol.png")

    # accuracy = randomGuessStrat(2)
    # print(f"The accuracy of random guessing is {accuracy * 100}%")

    # accuracy = smartGuessStrat(2)
    # print(f"The accuracy of our strategy is {accuracy * 100}%")

if __name__ == '__main__':
    main()