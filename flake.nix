{
  description = "mextractor: Python uv project";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";

    py-harbor = {
      url = "git+https://codeberg.org/caniko/py-harbor.git";
      inputs.nixpkgs.follows = "nixpkgs";
    };

    treefmt-nix.url = "github:numtide/treefmt-nix";
    git-hooks.url = "github:cachix/git-hooks.nix";
  };

  outputs = {
    self,
    nixpkgs,
    py-harbor,
    treefmt-nix,
    git-hooks,
    ...
  }:
    let
      py = py-harbor.lib;

      mkDevShells =
        system:
        let
          pkgs = py.mkPkgs { inherit system; };
          treefmtEval = treefmt-nix.lib.evalModule pkgs (import ./nix/treefmt.nix);
          pre-commit-check = git-hooks.lib.${system}.run {
            src = ./.;
            hooks = import ./nix/pre-commit.nix {
              inherit pkgs;
              treefmtWrapper = treefmtEval.config.build.wrapper;
            };
          };
        in
        {
          default = py.mkUvDevShell {
            inherit pkgs;
            uvExtra = "default";
            devGroup = "default";
            extraPackages = pre-commit-check.enabledPackages;
            shellHookSuffix = pre-commit-check.shellHook;
          };
        };

      mkPythonPackage =
        system:
        let
          pkgs = py.mkPkgs { inherit system; };
          python = pkgs.python313;
        in
        py.mkUvAppPackage {
          inherit pkgs python;
          name = "mextractor-cpu";
          envName = "mextractor-cpu-env";
          workspaceRoot = ./.;
          dependencies = {
            mextractor = [ "default" ];
          };
          scripts = [
            "mextractor"
          ];
        };

      mkPythonCheckEnv =
        system:
        let
          pkgs = py.mkPkgs { inherit system; };
          python = pkgs.python313;
        in
        py.mkUvCheckEnv {
          inherit pkgs python;
          name = "mextractor-cpu-env-check";
          workspaceRoot = ./.;
          dependencies = {
            mextractor = [
              "default"
              "default"
            ];
          };
        };

      mkChecks =
        system:
        let
          pkgs = py.mkPkgs { inherit system; };
          treefmtEval = treefmt-nix.lib.evalModule pkgs (import ./nix/treefmt.nix);
          checkEnv = mkPythonCheckEnv system;
          package = self.packages.${system}.mextractor-cpu;
        in
        {
          flake-eval = pkgs.runCommand "mextractor-flake-eval" { } ''
            test -x ${package}/bin/mextractor
            mkdir -p $out
            echo ok > $out/result
          '';
          formatting = treefmtEval.config.build.check self;
          offline-tests = pkgs.runCommand "mextractor-offline-tests" { } ''
            export HOME=$TMPDIR/home
            export XDG_CACHE_HOME=$TMPDIR/cache
            mkdir -p "$HOME" "$XDG_CACHE_HOME" "$out"
            cd ${./.}
            ${checkEnv}/bin/python -m pytest -p no:cacheprovider
            echo ok > $out/result
          '';
          typecheck = pkgs.runCommand "mextractor-typecheck" { } ''
            export HOME=$TMPDIR/home
            export XDG_CACHE_HOME=$TMPDIR/cache
            mkdir -p "$HOME" "$XDG_CACHE_HOME" "$out"
            cd ${./.}
            ${checkEnv}/bin/python -m mypy .
            echo ok > $out/result
          '';
          uv-format = pkgs.runCommand "mextractor-uv-format" { } ''
            export HOME=$TMPDIR/home
            export XDG_CACHE_HOME=$TMPDIR/cache
            export UV_NO_SYNC=1
            mkdir -p "$HOME" "$XDG_CACHE_HOME" "$out"
            cd ${./.}
            ${checkEnv}/bin/uv run --no-sync ruff format --check .
            echo ok > $out/result
          '';
        };

    in
    {
      devShells = py.forAllSystems mkDevShells;

      packages = py.forPackageSystems (
        system:
        let
          package = mkPythonPackage system;
        in
        {
          mextractor-cpu = package;
          default = package;
        }
      );

      apps = py.forPackageSystems (
        system:
        let
          package = self.packages.${system}.mextractor-cpu;
        in
        {
          mextractor-cpu = {
            type = "app";
            program = "${package}/bin/mextractor";
          };
          default = self.apps.${system}.mextractor-cpu;
        }
      );

      formatter = py.forAllSystems (
        system:
        let
          pkgs = py.mkPkgs { inherit system; };
          treefmtEval = treefmt-nix.lib.evalModule pkgs (import ./nix/treefmt.nix);
        in
        treefmtEval.config.build.wrapper
      );

      checks = py.forPackageSystems mkChecks;
    };
}
