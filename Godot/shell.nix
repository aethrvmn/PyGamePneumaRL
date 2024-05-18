with import <nixpkgs> {};

pkgs.mkShell rec {

  dotnetPkg = (with dotnetCorePackages; combinePackages [
    sdk_9_0
  ]);
  
  NIX_LD_LIBRARY_PATH = lib.makeLibraryPath ([
    stdenv.cc.cc
  ] ++ deps);
  
  NIX_LD = "${pkgs.stdenv.cc.libc_bin}/bin/ld.so";

  nativeBuildInputs = [] ++ deps;
  
  shellHook = ''
    export LD_LIBRARY_PATH=$NIX_LD_LIBRARY_PATH
    DOTNET_ROOT="${dotnetPkg}"
  '';

  packages = [
    dotnet-sdk
    xorg.libX11
  ];

  deps = [
    zlib
    zlib.dev
    openssl
    dotnetPkg
  ];
}
