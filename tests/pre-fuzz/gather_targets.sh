set -e

echo "Cloning targets"
# for TARGET_NAME in $TARGETS/*; do
#     if [ -d "${TARGET_NAME}" ]; then
#         # export TARGET=$TARGET
#         # $NAME= basename $TARGET_NAME
#         export TARGET=$OUT/targets/$TARGET_NAME
#         mkdir -p $TARGET
#         # cd $TARGET
#         sudo sh $TARGET_NAME/preinstall.sh
#         sh $TARGET_NAME/fetch.sh
#         # cd $old_dir
#     fi
# done

export TARGET_NAME=$MAGMA/targets/libpng
export TARGET=$OUT/targets/libpng
mkdir -p $TARGET
# cd $TARGET
sudo sh $TARGET_NAME/preinstall.sh
sh $TARGET_NAME/fetch.sh