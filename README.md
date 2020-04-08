

sudo easy_install pip
pip install virtualenv
virtualenv -p python3 env

source env/bin/activate
pip install -r requirement.txt
python fetcher.py