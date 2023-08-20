#!/bin/bash

bench init --frappe-branch develop bench 

cd bench

bench get-app https://github.com/arunmathaisk/flashdesk

bench new-site flashdesk.site --admin-password apple --db-root-password apple

bench --site flashdesk.site add-to-hosts

bench --site flashdesk.site install-app flashdesk

bench use flashdesk.site

bench set-config -g developer_mode 1
