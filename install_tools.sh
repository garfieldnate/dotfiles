#!/usr/bin/env bash
# run after brew.sh

# countdown timer
pip3 install termdown
# leo dictionary lookup
pip3 install git+https://github.com/garfieldnate/leo-cli.git@ansii_formatting
# Japanese dictionary lookup
pip3 install myougiden
updatedb-myougiden -f
# other dictionary-related tools
pip3 install lxml
pip3 install git+https://github.com/garfieldnate/tango.git
echo "please synch ~/.tangocho with ~/pCloud\ Drive/.tangocho"

curl -s "https://get.sdkman.io" | bash
sdk install java
sdk install gradle

curl -o- https://raw.githubusercontent.com/creationix/nvm/v0.33.11/install.sh | bash
rm ~/.bashrc
echo 'export NVM_DIR="$HOME/.nvm"' >> ~/.bash_profile
echo '[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"  # This loads nvm' >> ~/.bash_profile
echo '[ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"  # This loads nvm bash_completion' >> ~/.bash_profile

source ~/.bash_profile
nvm install node # latest

curl -L https://install.perlbrew.pl | bash
perlbrew install perl-5.28.0
perlbrew switch 5.28.0
curl -L https://cpanmin.us | perl - App::cpanminus
cpanm App::cpanminus::reporter
cpanm-reporter --setup
# used by GET, PUT, etc. aliases
cpanm install Mozilla::CA

pip3 install buku
mkdir -p ~/.local/share/buku
ln -s ~/Dropbox/appdata/bookmarks.db ~/.local/share/buku/bookmarks.db
mkdir -p ~/.bash_completion.d
curl https://raw.githubusercontent.com/jarun/Buku/master/auto-completion/bash/buku-completion.bash > ~/.bash_completion.d/buku-completion.bash

echo "Please manually clone and install the mac_port branch of https://github.com/garfieldnate/oil"
