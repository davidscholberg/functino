@echo off

pyinstaller^
 --clean^
 --onefile^
 --windowed^
 --name functino^
 --add-data "src/functino/resources;functino/resources"^
 src\functino\gui\__init__.py
