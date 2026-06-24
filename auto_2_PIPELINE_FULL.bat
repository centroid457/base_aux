REM call it MANUALLY line by line in CMD.exe!!!

rd dist\ /q /s
rd build\ /q /s

python -m build --sdist -n
python -m build --wheel -n

twine upload dist/*
REM here you need to wait a little bit! about 20-40sec!
REM pypi service might update data

pip install -U base-aux
