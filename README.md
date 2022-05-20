# Frogger
A simple frogger game for practice purposes, made in Python using the graphics.py package.

Game field is populated with multiple 'lanes', stacked vertically.
Frog can move up or down lanes, or left and right in the same lane.
There are three types of lanes:
- Grass lanes allow no traffic.  There is a grass lane at the top and bottom of the screen.
- Road lanes allow car traffic.  Cars are relatively fast, and will kill your frog if you collide with one.
- River lanes allow log traffic.  Logs are slower than cars, but working the opposite way.  The frog can only traverse the river by hopping from log to log.  If the frog hops into a section of the river that does not have a log, then the frog will die.

If the frog makes it from the bottom grass lane to the top grass lane, then the player wins that round.

Cars and logs (herafter referred to as 'mobs') may move either from left to right or vice versa.  Mobs are spawned at either the far left or right of the screen, depending on the direction of traffic as set by the lane.  Mobs then proceed to cross the length of the lane, before despawning at the other side.
Settings control how many mobs can appear in a single lane at a time.  A lower number will help keep frame rate smooth.
Settings also control the min and max speed of both types of mobs (separately), as well as how many lanes of each type will appear in the game field.

Player is prevented from directly moving the frog past the bounds on the playfield.  However, when the frog is sitting upon a log on the river, the frog will travel with the log at the same speed and in the same direction.  This can force the frog beyond the playfield limits, at which point the frog dies.

The speed and direction of mobs is determined by the lane.  The lane chooses these parameters randomly when the playfield is generated.  In this manner, every game will be slightly different.
