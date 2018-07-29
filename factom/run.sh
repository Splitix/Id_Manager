#!/usr/bin/env bash
factomd -count=5 -blktime=20 -network=LOCAL -startdelay=15 &
sleep 30
factom-walletd &
sleep 30
factom-cli importaddress Fs3E9gV6DXsYzf7Fqx1fVBQPQXV695eP3k5XbmHEZVRLkMdD9qCK
