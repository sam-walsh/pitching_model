## Stuff Quality Metric

Project description:

Stuff quality models aim to predict the effectiveness of a pitcher's pitches based on the physical characteristics of the pitch rather than outcomes. When done correctly, this method can outperform traditional ERA estimators and projection systems in predicting future outcomes for pitchers. More info [here](https://library.fangraphs.com/pitching/stuff-location-and-pitching-primer/).

My approach to modeling pitch quality is a bit different from the versions of the metric found on Fangraphs; [Stuff+](https://www.fangraphs.com/leaders/major-league?pos=all&stats=pit&lg=all&qual=y&type=36&season=2023&month=0&season1=2023&ind=0) created by Eno Sarris (The Athletic) and Max Bay (Houston Astros), [PitchingBot](https://www.fangraphs.com/leaders/major-league?pos=all&stats=pit&lg=all&qual=y&type=25&season=2023&month=0&season1=2023&ind=0) created by Cameron Grove (Cleveland Guardians). 

#### Outline of approach:

1. Predicted run values:

 Use predicted context-neutral run values of balls in play with exit velocity, launch angle, and spray angle (binned and normalized for batter handedness) as the target for the model. Using context-neutral run values helps us evaluate the result of each specific pitch without baserunner and outs information leaking in from the previous ones. Using predicted run values helps to separate some of the noise from outcomes that are a result of defense, park dimensions, weather, etc. Eliminating noise in the target variable of the model really helps regularize predictions for pitches with outlier characteristics especially in small sample sizes.

2. Feature engineering / extra feature inclusions: 
 I've included some extra features in my model along with the traditionally used features.
 Traditional features:
 - velocity (`release_speed`)
 - vertical movement (`az`)
 - horizontal movement (`ax`)
 - vertical location (`plate_z`)
 - horizontal location (`plate_x`)

 Extra/engineered features: 
 - release point / vertical and horizontal approach angle (`haa` & `vaa`)
 - pitch axis deviation (`axis_deviation_adj`) - for estimating late break as a result of seam-shifted wake effect; data acquired from [baseball-savant](https://baseballsavant.mlb.com/leaderboard/spin-direction-pitches) (pre-averaged unfortunately)
 - vertical and horizontal movement difference from fastball (`vert_delta` & `horz_delta`) - used for non-fastballs 
 - velocity difference from fastball (`velo_delta`) - used for non-fastballs
 - spin axis difference from fastball (`spin_axis_delta`) - in theory this may help identify spin mirroring which makes pitches harder to differentiate for the batter

3. Location modeling (in progress)
 - experimenting with a Bayesian hierarchical model to simulate pitch location based on pitch type, batter handedness, and count
 - also experimenting with Kernel Density estimation for the same purpose

You can find the current leaders for my stuff quality metric for different pitch types in `stuff.ipynb`.