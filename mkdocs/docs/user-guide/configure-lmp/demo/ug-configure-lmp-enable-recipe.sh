PS1="$ "

# To produce this demo as a cast, run:
# asciinema rec ./ug-configure-lmp-enable-recipe.cast -c ./ug-configure-lmp-enable-recipe.sh
#
# This demo requires user input when vim commands are called.

. ../../../../scripts/asciinema/demo-magic.sh -n

p "# Clone the meta-subscriber-overrides repo."

pe "git clone https://source.foundries.io/factories/cowboy/meta-subscriber-overrides.git"

p "# Enter the directory."

pe "cd meta-subscriber-overrides"

p "# Checkout to devel. Now the Target produced by this change will be tagged 'devel'"

pe "git checkout devel"

p "# Configure the recipe variables."

pe "vim conf/machine/include/lmp-factory-custom.inc"

p "# Add lmp-auto-hostname to the list of recipes in lmp-factory-image.bb."

pe "vim recipes-samples/images/lmp-factory-image.bb"

p "# Push the change to get built by Foundries."

pe "git add ."
pe "git commit -m \"enable lmp-auto-hostname\""
pe "git push"

rm -rf meta-subscriber-overrides
