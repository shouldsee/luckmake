set -euxo
cd example-ece264-hw04.dir

make clean
make testall

luckbd clean
luckbd testall
# false
echo [FIN]
