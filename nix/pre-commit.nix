{
  pkgs,
  treefmtWrapper,
}: {
  treefmt = {
    enable = true;
    name = "treefmt";
    package = treefmtWrapper;
    entry = "${treefmtWrapper}/bin/treefmt --ci";
    pass_filenames = false;
  };

  nix-flake-check = {
    enable = true;
    name = "nix flake check";
    entry = "nix --extra-experimental-features 'nix-command flakes' flake check --cores 0 --max-jobs auto --no-update-lock-file";
    extraPackages = [pkgs.nix];
    pass_filenames = false;
    stages = ["manual"];
  };

  uv-mypy = {
    enable = true;
    name = "uv mypy";
    entry = "uv run mypy .";
    extraPackages = [pkgs.uv];
    pass_filenames = false;
  };
}
