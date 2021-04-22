# authot: sccub and ssamypoull
# Simulation of a galaxy to generate a value for the contact rate between civilizations

# import dependencies
import sys
import pygame
import time
from constants import *
from civ import Civ
from signal import Signal

# initialize simulation window
pygame.init()
pygame.display.set_caption("Galaxy Sim")
size = width, height = DIAM, DIAM
center = RAD, RAD
screen = pygame.display.set_mode(size)
black = 0, 0, 0

# declare a set for all civilizations
# and a set for all of their signals
init_civ_count = N_high
civilizations = [Civ(i) for i in range(int(init_civ_count))]
signals = [Signal(civ) for civ in civilizations]

# set up game clock and simulation speed
starttime = time.time()
century_length = 1.0 / SIM_SPEED
# variable to hold the century count
clock = 0

# number of centuries in between each new civ birth
civ_birthrate = 100

# begin game loop
while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

    # create 1 new civ every n centuries, where n
    # represents civ_birthrate. Create that
    # civ's signal as well.
    if clock % civ_birthrate == 0:
        newCiv = Civ(init_civ_count + clock + 1)
        newSig = Signal(newCiv)
        civilizations.append(newCiv)
        signals.append(newSig)

    # refresh screen background
    screen.fill(black)
    pygame.draw.circle(screen, (255, 255, 255), center, RAD)
    pygame.draw.circle(screen, (155, 155, 155), center, RAD, 5)
    # galactic center
    pygame.draw.circle(screen, (0, 0, 0), center, CENTER_RAD)

    # For all civs, redraw civ is still alive.
    # Remove civ if deceased
    for civ in civilizations.copy():
        civ.advanceAge()

        if civ.isAlive():
            civ.draw(screen)
        else:
            civilizations.remove(civ)

        for sig in signals:
            if civ.isContacted(sig):
                print("com!")

    # redraw all signals
    for sig in signals:
        sig.advanceAge()
        sig.draw(screen)

    # update newly refreshed screen
    pygame.display.flip()

    print("century " + str(clock) + ". there are " + str(len(civilizations)) + " civs.")

    # wait a century and advance clock by 1
    time.sleep(century_length - ((time.time() - starttime) % century_length))
    clock += 1