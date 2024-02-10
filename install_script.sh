#!/bin/bash

bench init --frappe-branch version-15 bench

cd bench

bench new-site flashdesk.site --admin-password apple --db-root-password apple

bench use flashdesk.site

bench set-config -g developer_mode 1

bench --site flashdesk.site add-to-hosts

bench get-app https://github.com/arunmathaisk/flashdesk

bench --site flashdesk.site install-app flashdesk
