# NuPIC Cellular Automata Predictions

This is just an experiment on first-order sequence prediction, but I'm getting 100% prediction accuracy for one column of Rule 30.

## Requirements

    pip install automatatron
    pip install colorama

## Run

    python run.py [-r X]

The `-r` option allows users to specify a cellular automata rule. The default rule is Rule 30.

If input data needs to be created, it will be created for a swarm. If model params don't exist, a swarm will automatically be run. If these steps have already happened, their results will be reused so no unecessary swarms are run.

You'll get the Rule 30 cellular automata (middle 21 columns) output to the screen with NuPIC's prediction of column 10 highlighted. The percentage on the right is the rolling average of NuPIC's correctness over the last 500 rows.

```
# #  # ## ###########   98%
# #### #  #             98%
# #    #####        #   98%
  ##  ##  . #      ##   98%
 ## ### # .###    ##    98%
 #  #   ####  #  ##     98%
###### ## . ###### ##   98%
       # #.##      #    98%
#     ## #.# #    ###   98%
 #   ##  #.# ##  ##     98%
### ## ###.# # ### #    99%
    #  #  .# # #   ##   99%
   ###### ## # ## ##    99%
  ##      #  # #  #     99%
 ## #    ##### ######   99%
##  ##  ##.    #        99%
# ### ### #   ###       99%
# #   #   ## ##  #  #   99%
# ## ### ##  # ######   99%
# #  #   #.### #        99%
  ##### ##.#   ##       100%
###     # .## ## #  #   100%
#  #   #####  #  ####   100%
 #### ##  . ######      100%
##    # # .##     #     100%
  #  ## #### #   ####   100%
 #####  # .  ## ##      100%
 #    ####. ##  # #     100%
 ##  ##   ### ### ###   100%
 ```

Green marks indicate a correct prediction. Red indicates incorrect. 
