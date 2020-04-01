
#!/bin/zsh
PROJECT=$(pwd | awk -F '/' '{{print $NF}}')


init_venv(){
	virtualenv  $HOME/.venvs/$PROJECT -p $(which python)
	source $HOME/.venvs/$PROJECT/bin/activate
}

init_requirements(){
	pip install bpython six arrow isort pycodestyle pytest pipreqs
	if [ -f ./requirements.txt ]; then
		pip install -r ./requirements.txt
	else
		pipreqs ./ --force
	fi
}

init() {
	init_venv
	init_requirements
	echo "venv activate $PROJECT"
}

lint(){
	pycodestyle --show-source ./
}

isort(){
	isort -rc ./*.py --dir
}

test(){
	py.test --verbose --color=yes ./tests
}


clean() {
	find ./ -name "*.pyc" | xargs rm -f
    find ./ -name "*.pyc" | xargs rm -f
	rm -rf ./build
	rm -rf ./dist
	rm -rf *.egg-info
}

install(){
	clean
	tpl_dir=$(pwd -P)
	cd $tpl_dir
	python setup.py install
	clean
}


case $1 in
"init")
	init
	;;
"lint")
	lint
	;;
"test")
	test
	;;
"isort")
	isort
	;;
"clean")
	clean
	;;
"install")
	install
	;;
*)
	echo "Manager Usage: "
	printf "%-10s %-30s\n" init "generate virtualenv and install requirements"
	printf "%-10s %-30s\n" lint "check code style"
	printf "%-10s %-30s\n" test "run pytest"
	printf "%-10s %-30s\n" isort "sort imports smartly"
	printf "%-10s %-30s\n" clean "clean *.pyc & build * dist * egg"
	printf "%-10s %-30s\n" install "run install according to setup.py" 
	;;
esac
