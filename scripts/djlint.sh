#!/bin/bash

# Custom rules

# C001: <script src=...> tags must include a nonce= attribute.
# djlint's built-in ignored-block logic suppresses custom pattern rules on
# <script> elements, so we check for this with grep instead.
check_script_nonces() {
  local errors=0
  local all_files=()

  for entry in "$@"; do
    if [ -d "$entry" ]; then
      while IFS= read -r f; do
        all_files+=("$f")
      done < <(find "$entry" -name '*.html' -type f | sort)
    else
      all_files+=("$entry")
    fi
  done

  for file in "${all_files[@]}"; do
    [ -z "$file" ] && continue
    local matches
    matches=$(perl -0777 -ne '
      while (/<script\b[^>]*>/gsi) {
        my $tag = $&;
        next unless $tag =~ /\bsrc=/i;
        next if $tag =~ /\bnonce\b/i;
        my $pos = pos($_) - length($tag);
        my $line = 1 + (() = substr($_, 0, $pos) =~ /\n/g);
        (my $snippet = $tag) =~ s/\s+/ /g;
        $snippet = substr($snippet, 0, 30);
        print "$line\t$snippet\n";
      }
    ' "$file")
    if [ -n "$matches" ]; then
      printf "%s\n%s\n" "$file" "$(printf '─%.0s' {1..79})"
      while IFS=$'\t' read -r lineno snippet; do
        printf "C001 %s:0 Script tags with src= must include a nonce= attribute %s\n" "$lineno" "$snippet"
      done <<< "$matches"
      printf "\n"
      errors=1
    fi
  done

  return $errors
}

# Exposed functions

lint_html() {
  local files=("${@:-templates/}")

  printf "Linting HTML files: \n${files[*]}\n"
  local djlint_exit=0
  local nonce_exit=0
  # shellcheck disable=SC2068
  djlint ${files[@]} --lint --profile=jinja || djlint_exit=$?
  printf "\nCustom checks:\n%s\n" "$(printf '─%.0s' {1..79})"
  # shellcheck disable=SC2068
  check_script_nonces ${files[@]} || nonce_exit=$?
  [ $djlint_exit -ne 0 ] || [ $nonce_exit -ne 0 ] && return 1
}

case "$1" in
  lint)
    shift
    lint_html "$@"
    ;;
  *)
    echo "Error: Unknown command '$1'"
    echo "Usage: $0 lint [files...]"
    exit 1
    ;;
esac
