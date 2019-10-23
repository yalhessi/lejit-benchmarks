export MOZ_DIR=$HOME/mozilla-central
export HERE="$(pwd)"
export TEST="six-speed"

cd $MOZ_DIR

for i in {1..100}
do
    echo "Run Number: " $i
    # find . | xargs touch

    # taskset 0x8 ./mach talos-test --suite js-benchmarks
    # cp /home/yousef/mozilla-central/testing/mozharness/build/local.json "$HERE/logs/$PREFIX$(date +"%F-%T").json"

    # find . -print0 | xargs touch

    PREFIX="range-analysis-enabled-$TEST-"
    taskset 0x8 ./mach jsshell-bench --arg='--ion-range-analysis=on' --perfherder . $TEST >> "$HERE/logs/$PREFIX$(date +"%F-%T").json"

    # find . -print0 | xargs touch

    PREFIX="range-analysis-disabled-$TEST-"
    taskset 0x8 ./mach jsshell-bench --arg='--ion-range-analysis=off' --perfherder . $TEST >> "$HERE/logs/$PREFIX$(date +"%F-%T").json"
done

cd $HERE
