{pkgs ? import <nixpkgs>{}}:
with pkgs.pythonPackages;
buildPythonPackage {
  name = "setuptools_ez518";
  buildInputs = [setuptools setuptools_scm pytest];
  SOURCE_DATE_EPOCH="1234567890";

}