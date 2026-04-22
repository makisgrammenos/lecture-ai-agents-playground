#!/usr/bin/env python3

import argparse
import sys

from openai import OpenAI
from model_config import API_KEY, BASE_URL, DEFAULTS, MODEL

try:
    from colorama import Fore, Style, init as colorama_init
    colorama_init()
    C_USER      = Fore.GREEN  + Style.BRIGHT
    C_ASSISTANT = Fore.CYAN   + Style.BRIGHT
    C_INFO      = Fore.WHITE  + Style.DIM
    C_RESET     = Style.RESET_ALL
except ImportError:
    C_USER = C_ASSISTANT = C_INFO = C_RESET = ""


def parse_args():
    p = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    p.add_argument("--temperature", "-t", type=float, default=DEFAULTS["temperature"])
    p.add_argument("--max-tokens",  "-m", type=int,   default=DEFAULTS["max_tokens"], dest="max_tokens")
    p.add_argument("--system",      "-s", type=str,   default=DEFAULTS["system"])
    return p.parse_args()


def print_banner(args):
    print()
    print(f"{C_INFO}{'─' * 54}{C_RESET}")
    print(f"{C_INFO}  Model       : {MODEL}{C_RESET}")
    print(f"{C_INFO}  Temperature : {args.temperature}{C_RESET}")
    print(f"{C_INFO}  Max tokens  : {args.max_tokens}{C_RESET}")
    print(f"{C_INFO}  System      : {args.system[:60]}{'…' if len(args.system) > 60 else ''}{C_RESET}")
    print(f"{C_INFO}{'─' * 54}{C_RESET}")
    print(f"{C_INFO}  /clear  /history  /settings  exit{C_RESET}")
    print(f"{C_INFO}{'─' * 54}{C_RESET}")
    print()


def stream_reply(client, history, args) -> str:
    stream = client.chat.completions.create(
        model       = MODEL,
        messages    = history,
        temperature = args.temperature,
        max_tokens  = args.max_tokens,
        stream      = True,
    )
    print(f"{C_ASSISTANT}Assistant:{C_RESET} ", end="", flush=True)
    chunks = []
    for chunk in stream:
        delta = chunk.choices[0].delta.content
        if delta:
            print(delta, end="", flush=True)
            chunks.append(delta)
    print("\n")
    return "".join(chunks)


def main():
    args   = parse_args()
    client = OpenAI(api_key=API_KEY, base_url=BASE_URL)
    history = [{"role": "system", "content": args.system}]

    print_banner(args)

    while True:
        try:
            user_input = input(f"{C_USER}You:{C_RESET} ").strip()
        except (KeyboardInterrupt, EOFError):
            print(f"\n{C_INFO}Goodbye.{C_RESET}")
            sys.exit(0)

        if not user_input:
            continue

        if user_input.lower() in ("exit", "quit"):
            print(f"{C_INFO}Goodbye.{C_RESET}")
            sys.exit(0)

        if user_input == "/clear":
            history = [{"role": "system", "content": args.system}]
            print(f"{C_INFO}History cleared.{C_RESET}\n")
            continue

        if user_input == "/history":
            print(f"{C_INFO}{'─' * 54}{C_RESET}")
            for msg in history:
                body = msg["content"][:300] + ("…" if len(msg["content"]) > 300 else "")
                print(f"{C_INFO}[{msg['role'].upper()}]{C_RESET} {body}")
            print(f"{C_INFO}{'─' * 54}{C_RESET}\n")
            continue

        if user_input == "/settings":
            print(f"{C_INFO}temperature={args.temperature}  max_tokens={args.max_tokens}{C_RESET}\n")
            continue

        history.append({"role": "user", "content": user_input})
        reply = stream_reply(client, history, args)
        history.append({"role": "assistant", "content": reply})


if __name__ == "__main__":
    main()
