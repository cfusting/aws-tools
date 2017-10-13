#!/usr/bin/env bash
connd() {
  export EC2NODE=$(python ~/bunny/aws-tools/launch.py -t $1 $2)
  alias node="ssh -i ~/aws/key-pairs/cfusting-key-pair-n-virginia.pem ubuntu@${EC2NODE}"
}

congp() {
  export EC2NODE=$(python ~/bunny/aws-tools/launch.py -t g3.4xlarge 1.20)
  alias node="ssh -i ~/aws/key-pairs/cfusting-key-pair-n-virginia.pem ubuntu@${EC2NODE}"
}

concp() {
  export EC2NODE=$(python ~/bunny/aws-tools/launch.py -t m4.16xlarge 3.30)
  alias node="ssh -i ~/aws/key-pairs/cfusting-key-pair-n-virginia.pem ubuntu@${EC2NODE}"
}

