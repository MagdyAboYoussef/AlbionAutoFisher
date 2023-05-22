# AlbionAutoFisher

This is a simple Auto fishing project that I created to learn about openCV while I was playing Albion , It was intended for black zone to automate the process.
but it can be combined with other macros to fully automate the process for yellow/blue zones
it uses image reconition so it doesn't interact with the game client in any malicious way.

## How to use: 
need to install VB cable as it would read the sound of the client :https://vb-audio.com/Cable/
then set the output of albion client to be VB-cable

 ![image](https://github.com/MagdyAboYoussef/AlbionAutoFisher/assets/107952758/1a3e1f8f-f2d7-40fe-957a-a7a9a37c426d)


note: if you dont have sound from ingame client after applying this change, go to microphone devices and tick listen to this device on vb cable.

the script is then run through runner.py


![image](https://github.com/MagdyAboYoussef/AlbionAutoFisher/assets/107952758/3d7cccd3-3af2-49aa-851a-8c65f19b8b77)


if its the first launch select the images that will used(by default they are located in resources) and if the detection isnt good make sure the images are clear
and then select which scripts you want to run alongside 
### sound
automatically clicks when a biting sound occures (need to have only sound effects enabled to not confuse it and make the game sound around 50-60%) keep adjusting it until it fits for you
### player detection
it plays an annoying sound when someone comes off screen and it needs two images to detect one for bottom of screen to detect nametags behind the map 
and a hp/mana bar for people coming from other sides of the screen 


## Controls and usage 
### MB4
you need to have invis potion equipped and by using mouse button 4 you can automatically use a fish bait and then swap to invis potion again(very useful to always have invis potion equipped when getting ganked)

### MB3
mouse button 3 would automatically calculate distance  and throw the bobber at your cursor location  (not very accurate and has issues with high ground)
and it will automatically keep throwing the bobber after each successful reel at the same location until you move



https://github.com/MagdyAboYoussef/AlbionAutoFisher/assets/107952758/6d562002-7f18-4868-a88c-dce551534763

