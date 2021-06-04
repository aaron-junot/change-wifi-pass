# Change WiFi Password

This repository contains a small script used to change the wifi password. I set this up on a cron job so that the password on a certain network changes every day, such that my daughter has to do her chores before she receives the WiFi password.

## Usage

Basic Usage:
```bash
python change_pass.py
```

I set this up on a crontab with a little run.sh script that looks like this:
```bash
#!/bin/bash

cd ~/path/to/change-wifi-pass
source ./virtualenv/bin/activate
python change_pass.py
```

Then I set a cronjob that runs it at 8 every morning:
```bash
$ crontab -l
0 8 * * * ~/path/to/run.sh
```

## Credits
Wordlist taken from https://gist.github.com/marswh/0e06461ebf3a7cc48761629af2f8f445
