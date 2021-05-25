# Action Annotater
A tool for annotating meeting data, primarily intended for action-item detection

## Local development
- you need to install mongo-db manually, since it isn't part of the current requirements file, like so:  
  `conda install -c conda-forge mongodb`
- when working locally, without a docker container: in the data folder you need to create a db folder, for mongo to access
- To use the created db folder when starting the mongo-deamon, type:  
  `mongod --dbpath ./data/db`