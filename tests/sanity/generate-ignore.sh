#!/usr/bin/env bash
cat ignore.extra
cd ../../

generate() {
    while read -r line; do
        find plugins \
            \( "$@" \) \
            -name "*.py" \
            ! -name "__init__.py" \
            -printf "%p ${line//[%\\]/&&}\n" \
        | sort
    done
}

generate -path "plugins/modules/*" <"tests/sanity/ignore-modules.template"
generate -path "plugins/lookup/*" <"tests/sanity/ignore-lookup.template"
generate -path "plugins/module_utils/*" <"tests/sanity/ignore-module_utils.template"
