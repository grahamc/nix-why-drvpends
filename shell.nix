let
  pkgs = import <nixpkgs> {};
in
  pkgs.mkShell {
    buildInputs = [
        pkgs.python3
    ];
  }
