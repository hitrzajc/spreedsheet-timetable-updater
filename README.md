### Updates washing timetable

basic run
```bash
python3 -m venv ./venv
source ./venv/bin/activate
pip install -r requirements.txt
python3 main.py
```

put the repo in `/opt` and services to `/etc/systemd/system/`
after that enable the timer. Change `User` and `Group` acordingly (it must not be root). This steps are not necessary.

program will break when python is updated to another version example from 3.10 to 3.11.
You can bypass it if you change the link to ordnary file in `venv/bin/python`


you have to create google cloud account and setup some keys. look it up.
