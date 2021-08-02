# Lost in Space B9 Robot Model Prop Controller

## Using the B9 Controller
1. Plug in a USB cable to the bottom circuit board. Plug the other end into your computer or to a USB wall charger. It will take the controller up to 24 hours to fully charge a depleted battery. Alternatively, disconnect the battery cell from the board using the JST connector, and charge it using a USB Li-Ion rapid charger in about 4 hours.
2. Turn on the switch to enable power to the B9 model.
3. Double-tap the model to trigger B9's speech.
4. Press the Palette button to cycle between color modes:
  - Default (faithful to the original TV show)
  - Cool
  - Warm
  - Rainbow Colors
5. B9 goes to sleep after about two minutes of inactivity. Double-tap him to wake him and trigger audio playback and lights again.
6. As his batter starts to run low, B9 will play an alert and announce that his energy cells are low.


## Features
- The Robot responds with random phrases when double-tapped
- The Robot has a default appearance mode and can be cycled through alternate color palettes
- The Robot self-monitors battery level and warns when getting low.

## Hardware
The following components are part of this design:
- Neopixel RGB LEDs ($varies). These are BRIGHT LEDs that support 24-bit color and they're addressable, like a pixel in a digital image, which means that you can connect them all with a single data wire and control them all at once. This makes them ideal for animated displays like the twelve 'processing' lights at the bottom of the B9's chest panel. The cost will vary slightly depending on how many we need, but you can pick up an entire real of 500 for $20, so call it less than $5.
- Super-bright 3W RGB LED ($1). Used to illuminate the voice grille when the robot is speaking
- Miniature speaker ($2). Used for audio playback from the model.
- Feather M4 Express ($25)- This is the power-sipping microcontroller that runs the custom firmware code for the model
- Prop-Maker Featherwing ($10)- Accelerometer, audio codec and amp circuit, LED drivers, servo control (see below)
- 2200 mAh Lithium-ion battery ($5)
