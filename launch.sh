#!/usr/bin/env bash
# Assumes you have commands in .bash_aliases that require EC2NODE.

connd() {
  export EC2NODE=$(python ~/bunny/aws-tools/launch.py -t $1 $2)
  source $HOME/.bash_aliases
}

congp() {
  export EC2NODE=$(python ~/bunny/aws-tools/launch.py -t g3.4xlarge -p 1.20)
  source $HOME/.bash_aliases
}

concp() {
  export EC2NODE=$(python ~/bunny/aws-tools/launch.py -t c4.8xlarge -p .6)
  source $HOME/.bash_aliases
}

