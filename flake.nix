{
  description = "Provides a tex2image LaTeX rendering service container";

  inputs = {
    docker-tools.url = "github:Danie-1/docker-tools-flake";
  };

  outputs = { ... }: {
    nixosModules.default = { config, lib, ... }: let
      cfg = config.services.tex2image;
    in {
      options.services.tex2image = with lib; with types; {
        enable = mkOption {
          type = bool;
          default = true;
          description = "Whether to run the tex2image container.";
        };
        image = mkOption {
          type = str;
          default = "ghcr.io/olympiad-bot/tex2image:v1.0.0";
          description = "Container image for tex2image.";
        };
        docker-network = mkOption {
          type = str;
          default = "tex2image";
          description = "Docker network to attach to.";
        };
      };

      config = lib.mkIf config.services.tex2image.enable {
        docker-tools.networks = [ cfg.docker-network ];
        virtualisation.oci-containers.containers."tex2image" = {
          serviceName = "tex2image";
          image = cfg.image;
          extraOptions = [
            "--network-alias=tex2image"
            "--network=${config.services.tex2image.docker-network}"
          ];
        };
      };
    };
  };
}
