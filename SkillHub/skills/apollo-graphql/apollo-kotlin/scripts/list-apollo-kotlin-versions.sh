#!/usr/bin/env bash
git ls-remote --tags git@github.com:apollographql/apollo-kotlin.git | cut -d / -f 3
