{
  description = "Lifelog (Django + HTMX + SQLite) dev shell";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-24.05";
    flake-parts.url = "github:hercules-ci/flake-parts";
  };

  outputs = inputs@{ self, nixpkgs, flake-parts, ... }:
    flake-parts.lib.mkFlake { inherit inputs; } {
      systems = [ "x86_64-linux" "aarch64-linux" "x86_64-darwin" "aarch64-darwin" ];

      perSystem = { pkgs, ... }:
        let
          python = pkgs.python312;
          pythonEnv = python.withPackages (ps: with ps; [
            django
            uvicorn
          ]);
        in {
          devShells.default = pkgs.mkShell {
            packages = [
              pythonEnv
              pkgs.sqlite
              pkgs.git
              pkgs.just
              # pkgs.nodejs_20  # uncomment later if you add Tailwind tooling
            ];
            shellHook = ''
              export DJANGO_DEBUG=1
              export PYTHONUTF8=1
              echo "Dev shell ready. Run:"
              echo "  python manage.py makemigrations && python manage.py migrate"
              echo "  python manage.py bootstrap_eventtypes"
              echo "  python manage.py runserver"
              echo "  # or ASGI: uvicorn lifelog.asgi:application --reload --port 8000"
            '';
          };
        };
    };
}

