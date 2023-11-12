SAVE_DIR="/media/nwitt/Seagate Portable Drive/6258 Project/sidd/full/"
DOWNLOAD_DIR="./sidd-download/"

mkdir -p "$DOWNLOAD_DIR";
mkdir -p "$SAVE_DIR";
while read p; do
    echo "Downloading file - $p";
    wget -P "$DOWNLOAD_DIR" "$p";
    fpath="$DOWNLOAD_DIR"/$(echo $p | sed "s/.*\///");
    # echo "Unzipping file $fpath into $DOWNLOAD_DIR";
    # unzip -d "$DOWNLOAD_DIR" "$fpath";
    # echo "Removing file $fpath";
    # rm "$fpath";
    echo "Moving files from $DOWNLOAD_DIR to $SAVE_DIR";
    # mv $DOWNLOAD_DIR/* "$SAVE_DIR"
    mv "$fpath" "$SAVE_DIR"
done < sidd_download_links.txt
