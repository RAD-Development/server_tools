{
  description = "tools for our server";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
    poetry2nix = {
      url = "github:nix-community/poetry2nix";
      inputs = {
        flake-utils.follows = "flake-utils";
        nixpkgs.follows = "nixpkgs";
      };
    };
  };

  outputs =
    inputs@{
      self,
      nixpkgs,
      flake-utils,
      ...
    }:
    flake-utils.lib.eachDefaultSystem (
      system:
      let
        pkgs = nixpkgs.legacyPackages.${system};
        lib = pkgs.lib;
        poetry2nix = inputs.poetry2nix.lib.mkPoetry2Nix { inherit pkgs; };

        p2nix_defaults = {
          projectDir = ./.;
          python = pkgs.python312;
          overrides = poetry2nix.overrides.withDefaults (
            _: prev: lib.genAttrs [ "ruff" ] (package: prev.${package}.override { preferWheel = true; })
          );
        };
      in
      {
        packages.default = poetry2nix.mkPoetryApplication p2nix_defaults;

        devShells.default =
          (
            poetry2nix.mkPoetryEnv p2nix_defaults
            // {
              editablePackageSources = {
                server_tools = ./server_tools;
              };
            }
          ).env.overrideAttrs
            (old: {
              buildInputs = with pkgs; [
                poetry
                just
                python312Packages.pudb
              ];
            });

        apps.default = {
          type = "app";
          program = "${self.packages.server_tools}/bin/validate_jeeves";
        };
      }
    );
}
