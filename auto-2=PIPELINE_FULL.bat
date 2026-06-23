rd dist\ /q /s
rd build\ /q /s

python -m build --sdist -n
python -m build --wheel -n

twine upload dist/*
