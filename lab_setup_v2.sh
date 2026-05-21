#!/bin/sh
echo "Starting the lab setup script!"
echo "********************"
echo "\nPulling latest git files"

cd /home/developer/lab-src
git pull

echo "********************"


echo "\nInstalling requirements"

cd /home/developer/lab-src
pip install --upgrade pip
pip install -r requirements.txt --no-warn-script-location

echo "********************"

echo "\nCreating lab directory"

mkdir /home/developer/mdp_lab

lab_files=/home/developer/lab-src/lab_files
for d in "$lab_files"/ch*; do
  [ -d "$d" ] || continue
  base=$(basename "$d")
  case "$base" in
    *_v2)
      cp -r "$d" "/home/developer/mdp_lab/${base%_v2}"
      continue
      ;;
  esac
  if [ -d "$lab_files/${base}_v2" ]; then
    continue
  fi
  cp -r "$d" /home/developer/mdp_lab/
done
cp -r /home/developer/lab-src/lab_files/b* /home/developer/mdp_lab

echo "********************"

echo "Lab setup script completed!"
