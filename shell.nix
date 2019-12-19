let
  pkgs = import <nixpkgs> {};

  testrun = pkgs.writeScriptBin "why-drvpends" ''
    set -eux

    git ls-files '*.nix' | xargs nixpkgs-fmt

    git ls-files '*.py' | xargs mypy
    git ls-files '*.py' | xargs black

    ./why-drvpends.py "$@"
  '';
in
pkgs.mkShell {
  buildInputs = [
    testrun
    pkgs.nixpkgs-fmt
    pkgs.mypy
    (pkgs.python3.withPackages (pypkgs: with pypkgs; [ black ]))
    pkgs.flameGraph
  ];
}
