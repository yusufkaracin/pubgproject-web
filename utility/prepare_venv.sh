#!/usr/bin/env bash

cd /tmp
curl -L https://raw.githubusercontent.com/pyenv/pyenv-installer/master/bin/pyenv-installer | bash
cat >> /home/vagrant/.bash_profile << 'EOF'

export PATH="$PATH:~/.pyenv/bin"
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"

EOF
source /home/vagrant/.bash_profile
pyenv install 3.6.3
pyenv global 3.6.3
pyenv virtualenv 3.6.3 env-3.6.3
pyenv activate env-3.6.3
pip install -r /home/vagrant/project/backend/requirements.txt
echo "pyenv activate env-3.6.3 && cd /home/vagrant/project" >> /home/vagrant/.bash_profile
