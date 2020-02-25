execute_test() {
    python rest/manage.py test imageboard.tests.$1.$2   
}

source rest/env/scripts/activate

if [ $# == 1 ]; then
    for file in $(ls server/*/tests/$1); do
        if [[ $file =~ ^.*\.py$ ]]; then
            execute_test $1 ${file::-3}
        fi
    done
elif [ $# == 2 ]; then
    execute_test $1 $2
else
    echo "Provide directory of tests!"
fi