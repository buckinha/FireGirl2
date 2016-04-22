# FireGirl2

FireGirl2 is a research simulator of forests, wildfire, timber harvest, and management. It is primarily designed in the context of ongoing research at Oregon State University regarding optimization of wildfire suppression policies; i.e. how to make better decisions about when to suppress wildfires and when to capitalize on their benefits by allowing them to burn.

The simulator is designed to be called from other Python code, as a Markov decision process, much like those used in libraries such as RLPy for research in machine learning.

This is an ONGOING PROJECT, and the simulator code IS NOT COMPLETE. It is not ready for application in machine learning, policy search, etc..., though the goal is to get there soon. 


What is simulated/modelled:

  -Tree Growth, primarily modelled as Ponderosa Pine, growing in NE Oregon.
  
  -Timber Values
  
  -Weather
  
  -Fire Spread, making use of the Canadian FWI system, and emperical studies of fire shape, size, and spread rates, and fuel models.
  
  -Timber Harvest: As a selection cut system typical of Ponderosa Pine on commercial land
  
  -Randomized landscape generation
  
  -Wildfire suppression policies: user defined, with access to all of the ongoing simulation state values, as desired.


Coming Soon:
  -User Manual
  -Research Background and emperical studies behind FireGirl2's model components
  -Model Validation Results
  


  
