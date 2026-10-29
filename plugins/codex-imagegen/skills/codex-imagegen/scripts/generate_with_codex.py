#!/usr/bin/env python3
"""Pass selected Codex API configuration to the bundled imagegen CLI safely."""
import argparse
import json
import os
from pathlib import Path
import subprocess
import sys
import tomllib
from urllib.parse import urlsplit, urlunsplit


def resolve_config(home, environ, profile=None):
    config_path = home / "config.toml"
    config = tomllib.loads(config_path.read_text()) if config_path.exists() else {}
    selected_profile = profile or config.get("profile")
    if selected_profile:
        profiles = config.get("profiles", {})
        if selected_profile not in profiles:
            raise ValueError("Selected profile does not exist")
        config = {**config, **profiles[selected_profile]}
    provider_id = config.get("model_provider", "openai")
    providers = config.get("model_providers", {})
    if provider_id != "openai" and provider_id not in providers:
        raise ValueError("Selected provider does not exist")
    provider = providers.get(provider_id, {})
    base = provider.get("base_url")
    if not base:
        if provider_id != "openai":
            raise ValueError("Selected custom provider has no base_url")
        base = environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1")
    parsed = urlsplit(base)
    if parsed.scheme != "https" or not parsed.hostname or parsed.username or parsed.password:
        raise ValueError("An HTTPS API base URL without embedded credentials is required")
    if parsed.query or parsed.fragment:
        raise ValueError("API base URL must not contain query parameters or fragments")
    base = urlunsplit((parsed.scheme, parsed.netloc, parsed.path.rstrip("/") or "/v1", "", ""))
    env_key = provider.get("env_key")
    if env_key:
        key = environ.get(env_key)
        if not key:
            raise ValueError("Provider credential environment variable is not configured")
    else:
        key = provider.get("experimental_bearer_token") or provider.get("api_key")
        if not key and (provider_id == "openai" or provider.get("requires_openai_auth")):
            key = environ.get("OPENAI_API_KEY")
            if not key:
                auth_path = home / "auth.json"
                auth = json.loads(auth_path.read_text()) if auth_path.exists() else {}
                key = auth.get("OPENAI_API_KEY")
    if not isinstance(key, str) or not key.strip():
        raise ValueError("No API key found for the selected provider; OAuth tokens are not reused")
    return base, key


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--codex-home", type=Path, default=Path(os.environ.get("CODEX_HOME", str(Path.home() / ".codex"))))
    parser.add_argument("--profile")
    parser.add_argument("--cli", type=Path)
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--prompt-file", type=Path)
    parser.add_argument("--out", type=Path)
    parser.add_argument("--model", default="gpt-image-2")
    parser.add_argument("--size", default="1024x1024")
    parser.add_argument("--quality", choices=["low", "medium", "high", "auto"], default="high")
    args = parser.parse_args()
    try:
        base, key = resolve_config(args.codex_home, os.environ, args.profile)
        if args.check:
            print("Selected provider API credentials are configured. Image endpoint support is unverified.")
            return 0
        if not args.prompt_file or not args.out:
            parser.error("--prompt-file and --out are required for generation")
        if not args.prompt_file.is_file():
            raise ValueError("Prompt file does not exist")
        if args.out.exists():
            raise ValueError("Output already exists; choose a new versioned filename")
        cli = args.cli or args.codex_home / "skills/.system/imagegen/scripts/image_gen.py"
        if not cli.is_file():
            raise ValueError("Bundled imagegen CLI not found; supply its location with --cli")
        env = os.environ.copy()
        env.update(OPENAI_API_KEY=key, OPENAI_BASE_URL=base)
        args.out.parent.mkdir(parents=True, exist_ok=True)
        command = [sys.executable, str(cli), "generate", "--model", args.model,
                   "--prompt-file", str(args.prompt_file), "--size", args.size,
                   "--quality", args.quality, "--out", str(args.out)]
        return subprocess.run(command, env=env, check=False).returncode
    except (ValueError, OSError) as exc:
        # Do not print parsed config, credentials, or exception details from config files.
        if isinstance(exc, (json.JSONDecodeError, tomllib.TOMLDecodeError)):
            print("Invalid Codex configuration or authentication file", file=sys.stderr)
        elif isinstance(exc, OSError):
            print("Could not read configuration or launch imagegen CLI", file=sys.stderr)
        else:
            print(str(exc), file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
