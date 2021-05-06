PS1="$ "

# To produce this demo as a cast, run:
# asciinema rec ./ug-fioctl-enable-apps.cast -c ./ug-fioctl-enable-apps.sh

fioctl device config updates cowboy-device-1 --apps , > /dev/null 2>&1

. ../../../../scripts/asciinema/demo-magic.sh -n

p "# First, list Targets and ensure app(s) are available in the latest Target."

pe "fioctl targets list -f cowboy"

p "# Find a device to instruct by name."

pe "fioctl devices list -f cowboy"

p "# Enable only the desired app(s) on the device."

pe "fioctl devices config updates cowboy-device-1 --apps netdata,shellhttpd"

p "# Now only the app(s) supplied in the list will run on the device."
