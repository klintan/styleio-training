#Unsupervised Similarity Search

To generate a database with all the distances between all the pairs of images in the master folder you should do the following:

cd $TIEFVISION_HOME/src/torch/9-similarity-db
luajit similarity-db.lua
Once the database is generated, the images in master can be searched using that database using:

cd $TIEFVISION_HOME/src/torch/10-similarity-searcher-cnn-db
luajit search.lua -image <IMAGE_NAME_OF_AN_IMAGE_IN_$TIEFVISION_HOME/resources/dresses-db/master>