set -euxo
cd example-ece264-hw04.dir

time {
make clean
make testall
} 1>/tmp/out

time {
luckbd clean
luckbd testall
} 1>/tmp/out
# false
echo [FIN]
