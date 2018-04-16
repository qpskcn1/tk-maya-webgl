The 'Lighting Setup' script should run the following steps:

1. Set the frame rate and playback settings to the frame rate specified in shotgun
2. Sync frame range to shotgun frame range
3. Use the loader to reference the highest version alembic for each asset specified under 'Assets' in shotgun. For each asset:
       1. Load the latest shader network publish and apply it to the alembic. 
4. Reference the highest version 'CAM_' camera publish.