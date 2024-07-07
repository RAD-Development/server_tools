{
  description = "A tool to find and remove reddit watermarks.";

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

  outputs = inputs @ {
    self,
    nixpkgs,
    flake-utils,
    ...
  }:
    flake-utils.lib.eachDefaultSystem (system: let
      pkgs = nixpkgs.legacyPackages.${system};
      lib = pkgs.lib;
      poetry2nix = inputs.poetry2nix.lib.mkPoetry2Nix {inherit pkgs;};

      p2nix_defaults = {
        projectDir = ./.;
        python = pkgs.python311;
        overrides = poetry2nix.overrides.withDefaults (
          _: prev:
            lib.genAttrs [
              "ruff"
            ]
            (package: prev.${package}.override {preferWheel = true;})
        );
      };
    in {
      packages = rec {
        server_tools = poetry2nix.mkPoetryApplication p2nix_defaults;
        default = server_tools;
      };

      devShells = rec {
        server_tools =
          (poetry2nix.mkPoetryEnv p2nix_defaults
            // {
              editablePackageSources = {
                server_tools = ./server_tools;
              };
            })
          .env
          .overrideAttrs (old: {
            buildInputs = with pkgs; [
              poetry
              just
              python311Packages.pudb
            ];
          });
        default = server_tools;
      };

      apps = rec {
        server_tools = {
          type = "app";
          program = "${self.packages.server_tools}/bin/validate_jeeves";
        };
        default = server_tools;
        hi = server_tools;
      };
    });
}
