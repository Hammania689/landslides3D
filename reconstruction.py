import argparse
import re 
import time 

from subprocess import *
from pathlib import Path

parser = argparse.ArgumentParser(['colmap reconstruction'], description="""


[Provide Better Description Here]


""")


parser.add_argument('--data_dir', default=Path.cwd(), help="""

Directory that holds both before and after images for reconstruction

Assumed Project Directory Structure 
\n|--- 'before_images/'
\n|--- 'after_images/'
""")
args = parser.parse_args()

image_path = Path(args.data_dir)

def colmap_subprocess(command, log_name='reconstruction.log'):
    file = Path(log_name)
    with open(file, 'a+') as log_file:
        call(command, shell=False, stdout=log_file)
    print(file.read_text())

batch_start = time.time()
total_time = 0

if Path.exists(image_path):
    print(f"Will begin colmap reconstruction in {image_path} as project directory.\n")
    
    print("Will reconstruct the following directories separately:")
    sub_dirs = [ x for x in image_path.iterdir() if x.is_dir()]
    [print(f"{x}") for x in image_path.iterdir() if x.is_dir()]
    print()
    
    for cur_sub in sub_dirs:
        db_path = str(Path(cur_sub, Path("database.db")))
        sub_dir = str(cur_sub)
        
        # Feature Extraction
        cmd = f"colmap feature_extractor --database_path {db_path} --image_path {cur_sub}"
        cmd = cmd.split()
        print(f"Feature Extraction : {cmd}")
        colmap_subprocess(cmd)
        
        
        # Feature Matching 
        cmd = f"colmap exhaustive_matcher --database_path {db_path}"
        cmd = cmd.split()
        print(f"Feature Matching : {cmd}")
        colmap_subprocess(cmd)
        

        # Sparse Reconstruction
        sparse_path = Path(cur_sub, Path("sparse"))
        if Path.exists(sparse_path) == False:
            Path.mkdir(sparse_path)        
        cmd = f"colmap mapper --database_path {db_path} --image_path {cur_sub} --export_path {sparse_path}"
        cmd = cmd.split()
        print(f"Sparse Reconstruction : {cmd}")
        colmap_subprocess(cmd)
        
        # Dense Reconstruction
        dense_path = Path(cur_sub, Path("dense"))
        if Path.exists(dense_path) == False:
            Path.mkdir(dense_path)
        cmd = f"colmap image_undistorter --image_path {cur_sub} --input_path {sparse_path} --output_path {dense_path} --output_type COLMAP --max_image_size 2000"
        cmd = cmd.split()
        print(f"Dense Reconstruction: {cmd}")
        colmap_subprocess(cmd)
        
        
        # Dense Stereo
        cmd = f"colmap dense_stereo --workspace_path {dense_path} --workspace_format COLMAP --DenseStereo.geom_consistency true"
        cmd = cmd.split()
        print(f"Dense stereo: {cmd}")
        colmap_subprocess(cmd)

        # Dense Fuser 
        fused_path = Path(dense_path, Path("fused.ply"))
        if Path.exists(fused_path) == False:
            Path.touch(fused_path)
        cmd = f"colmap dense_fuser --workspace_path {dense_path} --workspace_format COLMAP --input_type geometric --output_path {fused_path}"
        cmd = cmd.split()
        colmap_subprocess(cmd)
        print(f"Dense Fuser: {cmd}")

        # Dense Mesher 
        meshed_path = Path(dense_path, Path("meshed.ply"))
        if Path.exists(meshed_path) == False:
            Path.touch(meshed_path)
        cmd = f"colmap dense_mesher --input_path {fused_path} --output_path {meshed_path}"
        cmd = cmd.split()
        colmap_subprocess(cmd)
        print(f"Dense Mesher: {cmd}")
        
        
total_time = time.time() - batch_start
# Prompt that reconstuction is done
print("=" * 100)
print("Reconstruction is Complete :)")
print(f"Total time: {total_time//60:.0f}m {total_time % 60:.0f}s")
print()