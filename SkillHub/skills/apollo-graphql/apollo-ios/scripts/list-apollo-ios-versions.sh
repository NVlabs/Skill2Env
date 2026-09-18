#!/usr/bin/env bash
git ls-remote --tags https://github.com/apollographql/apollo-ios.git | cut -d / -f 3
