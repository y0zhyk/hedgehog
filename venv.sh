if [ ! -d ./venv ] ; then
   python3 -m venv ./venv
fi
sh venv/bin/activate
pip3 install flask
