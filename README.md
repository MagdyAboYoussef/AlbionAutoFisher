# AlbionAutoFisher

This is a simple Auto fishing project that I created to learn about openCV while I was playing Albion , It was intended for learning purpose and to be used in black zone to automate the process.
but it can be combined with other macros to fully automate the process for yellow/blue zones
it uses image reconition so it doesn't interact with the game client in any malicious way.

## How to use: 
need to install VB cable as it would read the sound of the client :https://vb-audio.com/Cable/
then set the output of albion client to be VB-cable

![image](https://github.com/MagdyAboYoussef/AlbionAutoFisher/assets/107952758/3adc52dd-4ac3-4d43-84c0-62496d23815e)

note: if you dont have sound from ingame client after applying this change, go to microphone devices and tick listen to this device on vb cable.

the script is then run through runner.py


![image](https://github.com/MagdyAboYoussef/AlbionAutoFisher/assets/107952758/69fe61cd-d220-42e7-aa55-d2f5ac509378)

if its the first launch select the images that will used(by default they are located in resources with the same name you can just move your pictures there and overwrite them) and if the detection isnt good make sure the images are clear such as the ones in the folder, they differ from resolution to resolution so to make it as clear as possible its better to take your own clear small pictures  or run in 1920x800 which I ususally ran and then select which scripts you want to run alongside 
### sound
automatically clicks when a biting sound occures (need to have only sound effects enabled to not confuse it and make the game sound around 50-60%) keep adjusting it until it fits for you
### player detection
it plays an annoying sound when someone comes off screen and it needs two images to detect one for bottom of screen to detect nametags behind the map 
and a hp/mana bar for people coming from other sides of the screen 


## Controls and usage 
this script is best used with RTS-like controls and it only has 2 buttons 

### MB4
you need to have invis potion equipped and by using mouse button 4 you can automatically use a fish bait (it assumes the keybinding for potion/bait is "1") and then swap to invis potion again(very useful to always have invis potion equipped when getting ganked)

### MB3
mouse button 3 would automatically calculate distance  and throw the bobber at your cursor location  (not very accurate and has issues with high ground)
and it will automatically keep throwing the bobber after each successful reel at the same location until you move





https://github.com/MagdyAboYoussef/AlbionAutoFisher/assets/107952758/8e212c19-1319-4bae-911f-fc01fc3fd3a5


