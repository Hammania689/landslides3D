printf 'Will begin colmap reconstruction in "$PWD" as project directory.\n\n\n' "$LS"

DATASET_PATH=$PWD
DIRECTORY=$DATASET_PATH/images

if [ -d "$DIRECTORY" ]; then
  # Control will enter here if $DIRECTORY exists.
    colmap feature_extractor \
    --database_path $DATASET_PATH/database.db \
    --image_path $DATASET_PATH/images;

    colmap exhaustive_matcher \
    --database_path $DATASET_PATH/database.db

    mkdir $DATASET_PATH/sparse

    colmap mapper \
        --database_path $DATASET_PATH/database.db \
        --image_path $DATASET_PATH/images \
        --export_path $DATASET_PATH/sparse

    mkdir $DATASET_PATH/dense

    colmap image_undistorter \
        --image_path $DATASET_PATH/images \
        --input_path $DATASET_PATH/sparse/0 \
        --output_path $DATASET_PATH/dense \
        --output_type COLMAP \
        --max_image_size 2000

    colmap dense_stereo \
        --workspace_path $DATASET_PATH/dense \
        --workspace_format COLMAP \
        --DenseStereo.geom_consistency true

    colmap dense_fuser \
        --workspace_path $DATASET_PATH/dense \
        --workspace_format COLMAP \
        --input_type geometric \
        --output_path $DATASET_PATH/dense/fused.ply

    colmap dense_mesher \
        --input_path $DATASET_PATH/dense/fused.ply \
        --output_path $DATASET_PATH/dense/meshed.ply
    printf "Done :)\n" "$LS"
else 
    printf "This script should be ran from parent project directory\n"
    printf " "

    printf "Expected Directory Format :"
    printf "Parent Project Directory 
    |--- 'images' Directory (must be named 'images')\n"  
    
    printf " "
    printf "The folder containing images must be named 'images' for this script to work"

fi