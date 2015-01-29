# NuPIC Cellular Automata Predictions

This is just an experiment, but I'm getting around 75% prediction accuracy for one column of Rule 30.

## Requirements

    pip install automatatron
    pip install colorama

## Swarm

First, create the swarm input file using `automatatron`'s Rule 30 and the swarm description file.

    python create_swarm_input.py

Then run the swarm. This will take some time. 

    python swarm.py

## Run

    python run.py

You'll get the cellular automata (middle 21 columns) output to the screen with NuPIC's prediction of column 10 highlighted. The percentage on the right is the rolling average of NuPIC's correctness over the last 500 rows.

```
###  ##  #.### ### ##   75%
   ### ###.#   #   #    75%
  ##   #  .## ### ###   75%
 ## # ### ##  #   #     75%
##  # #   # #### ####   75%
# ### ## ## #    #      75%
# #   #  #. ##  ###     76%
  ## ######## ###  ##   75%
###  #    .   #  ###    75%
#  ####   .  #####  #   75%
####   #  . ##    ###   75%
    # ### .## #  ##     75%
#  ## #  ###  #### #    75%
####  ####. ###    #    75%
#   ###   ###  #  ##    75%
 # ##  # ##  ######     75%
 # # ### #.###     ##   76%
## # #   #.#  #   ##    76%
   # ## ##.##### ## #   76%
  ## #  # .#     #  #   76%
 ##  ########   #####   76%
## ###    .  # ##       76%
#  #  #   . ## # #  #   76%
 #######  .##  # ####   76%
##      # ## ### #      76%
  #    ## #  #   ## #   76%
####  ##  ##### ##  #   76%
#   ### ###     # ###   76%
 # ##   # .#   ## #     76%
 # # # ###### ##  ##    76%
```

Green marks indicate a correct prediction. Red indicates incorrect. 