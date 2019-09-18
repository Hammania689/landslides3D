# Landslide Erosion Analysis #

Our framework utilizes recent advances in open source
libraries and algorithms to provide landslide responders
with a single application that handles every step in the 3D
reconstruction and change detection process.

## General Overview ##

*[COLMAP](https://colmap.github.io/)* is used for 3D reconstruction.

*[Open3d](www.open3d.org)* is used for registration and segmentation.

*[Cloud Compare](https://www.danielgm.net/cc/)* is used for hausdorff distance heatmap calculation.

**For implementation details refer to the RISS journal [paper](https://gitlab.com/RISS_students_2018/landslide/blob/master/RISS-2018-PAPER-Abdul-Hameed.pdf) or [poster](https://gitlab.com/RISS_students_2018/landslide/blob/master/RissPoster_Final.pdf)**

**Please refer to [Open3D](www.open3d.org/docs/) examples or our included scripts [here](https://gitlab.com/RISS_students_2018/landslide/tree/master/Open3D_Scripts)**



## Future Work ##

1. **Search for more robust distance comparison algorithm. Hausdorff does not work well with outliers present** 


2. Improve UI and flow of framework pipeline.


3. Potentially use Open3D and OpenCV C++ api to incorporate more library features and achieve better performance.


Relevant data, papers and resources can be found in [Useful Resources](https://gitlab.com/RISS_students_2018/landslide/blob/master/Useful%20Resources.md).

Contacted Teams for Landslide data can be found in [Contacted Teams](https://gitlab.com/RISS_students_2018/landslide/blob/master/Contacted_Teams.md). Contains status, email, and download insturctions.

## COLMAP Bash Script ##
**Runs every step in the reconstruction process sequentially with one command**

**Run the Colmap Reconstruction Bash Script found [here](https://gitlab.com/RISS_students_2018/landslide/blob/master/colmap_reconstruct.sh)**
Must be ran from the Parent Project Directory <br>
`/home/Desktop/colmap_reconstruct.sh` 

**Directory MUST Follow Expected Format :** <br>
Parent Project Directory <br>
||=== 'images' Directory (**must be named 'images'**)


## Docker Instructions ##

**Must have nvidia-docker** 

Colmap Container :) <br>
`docker pull chapchaebytes/colmap`

**Change** `$HOME` **to your desired directory** <br>
`sudo nvidia-docker run -it --volume=$HOME:/home --name=colmap chapchaebytes/colmap bash`


**Change Ownership of Files** <br>
`sudo chown -R $USER [folder name]`

Use Colmap Terminal Commands. Documentation can be found [here](https://colmap.github.io/cli.html) 

### Relevant docker commands ###
`sudo nvidia-docker start {name/id of container}` <br>
`sudo nvidia-docker stop {name/id of container}`

Show all containers: <br>
`sudo nvidia-docker container ls`

Interact with the Running Container via Terminal: <br>
`sudo nvidia-docker attach {name/id of container}`

Permanetly Remove stopped containers: <br>
`sudo nvidia-docker container prune`