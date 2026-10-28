#!/usr/bin/env bash
set -euo pipefail
mkdir -p third_party

clone_pin () {
  local url="$1" dir="$2" sha="$3"
  if [ ! -d "$dir/.git" ]; then
    git clone "$url" "$dir"
  fi
  git -C "$dir" fetch --all --tags
  git -C "$dir" checkout "$sha"
}

clone_pin https://github.com/jinlab-imvr/Deform3DGS.git third_party/Deform3DGS b06f0a501bd1c71aa70d9a48a8dd4810ccddb2b7
clone_pin https://github.com/neneyork/SurgicalGS.git third_party/SurgicalGS 62f6d5fa4031685edb01f2efa8a63b004db8110b
clone_pin https://github.com/ThatphumCpre/EndoPlanar.git third_party/EndoPlanar f5fd519319e901ad4c7f6b60e6c550c71fc5d7f6
clone_pin https://github.com/wMito/ColonSplat.git third_party/ColonSplat d317a4e7d1541290ab9478ba11658bbed2020afa
clone_pin https://github.com/hritam-98/physiosplat.git third_party/physiosplat 54c38915e64f1e9c300a638b15614043d44fff17
