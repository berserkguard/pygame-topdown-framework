The Last Robot
==============

Game submission for the Fall 2014 twelve-hour Gamebuild-a-thon in Pygame. Created by Ryan Norby (berserkguard).


Story
-----
You are an old robot in a deserted world. Your body is slowly decaying, and there are automated turrets that still see you as a threat. As parts of your body become damaged, you incur status ailments that debilitate you. You must scavenge the barren earth, looking for scrap metal with which to repair yourself. How long can you last?


Controls
--------
WASD: Movement

Walk over scrap to pick them up. Different types of scrap repair different body parts. See the 'Scraps' section below for more information.
Avoid turrets. The shoot lasers that damage a random body part.
You lose when all of your body parts are at red damage. There is no way to win.


Scraps
------
 * Antenna: Repairs your antenna
 * Claw: Repairs one of your arms (prioritizes arm with more damage)
 * Cylinder: Repairs one of your legs (prioritizes leg with more damage)
 * Metal Crate: Repairs your head
 * Plate Metal: Repairs your body
 * Spring: Repairs one of your arms (prioritizes arm with more damage)


Status Ailments
-----------------
Each body part (antenna, head, arms, legs, body) can be in one of three conditions: Green (fully functional), Yellow (mostly functional), Red (barely functional).

The status ailments for yellow damage are as follows:
 * Antenna: Reduced visibility
 * Head: Inverted movement controls
 * Body: Repair amount reduced by 25%
 * Right Arm: Reduces pickup distance by 25%
 * Left Arm: Reduces pickup distance by 25%
 * Right Leg: Reduces movement speed by 25%
 * Left Leg: Reduces movement speed by 25%

The status ailments for red damage are as follows:
 * Antenna: Greatly reduced visibility
 * Head: Randomized movement controls (on a 20% chance)
 * Body: Repair amount reduced by 50%
 * Right Arm: Reduces pickup distance by 50%
 * Left Arm: Reduces pickup distance by 50%
 * Right Leg: Reduces movement speed by 50%
 * Left Leg: Reduces movement speed by 50%

Debilitation for right arm and left arm do not stack. The more damaged one will be the one whose status ailment is chosen. Likewise for right leg and left leg.
