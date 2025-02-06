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

mkdir /home/developer/IPv6_lab

cp -r /home/developer/lab-src/lab_files/ch* /home/developer/IPv6_lab
cp -r /home/developer/lab-src/lab_files/b* /home/developer/IPv6_lab

echo "********************"

echo "Lab setup script completed!"
