#!/bin/bash

if [ "$1" == "start" ]; then
    modprobe cpuidle-haltpoll force
fi

## Question:  Does this also need another "if" checking to see if $1 is "stop" to unload the module?
