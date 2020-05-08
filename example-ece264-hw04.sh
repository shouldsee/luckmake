set -euxo
cd example-ece264-hw04.dir

make clean
make testall

luck-build clean
luck-build testall
# false
echo [FIN]
