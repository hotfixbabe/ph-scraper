# ph-scraper

A simple tool to extract public information from profiles and videos.

## About

This project provides a command-line interface (CLI) to fetch public data from a profile and list public videos.

The focus of this README is basic CLI documentation — how to run it and practical examples.

## CLI Usage

The CLI is exposed via the `ph_scraper` module. The main command currently available is `profile`.

Basic syntax:

```bash
ph-scraper profile <url> [--cache PATH] --get-pub-videos [-j|--print-json] [-u|--print-url]
```

### Key Options

* `profile` (command)

  * `url` (positional argument): URL of the profile to analyze.
  * `-c`, `--cache PATH`: path to save/load cache (optional).
  * `--get-pub-videos`: (required within the `profile` subcommand) retrieves the profile’s public videos.
  * `-j`, `--print-json`: prints the result in JSON format (list of video objects).
  * `-u`, `--print-url`: prints only the video URLs (default: `print_url` is true when no flags are provided).

Note: `--get-pub-videos` is one of the operation modes of the `profile` subcommand — currently, it is the only mode supported to list public videos.

### Default Behavior

If neither `-j/--print-json` nor `-u/--print-url` is provided, the CLI prints the video URLs by default (`--print-url` is set as default).

## Examples

1. List URLs of a profile’s public videos (default mode):

```bash
ph-scraper profile https://example.com/user --get-pub-videos
```

2. Print videos in JSON format:

```bash
ph-scraper profile https://example.com/user --get-pub-videos --print-json
```

3. Use local cache:

```bash
ph-scraper profile https://example.com/user --get-pub-videos --cache /tmp/ph_cache
```
