#!/usr/bin/env python3
"""Prepare customer-bound writes from authenticated readbacks. Never sends HTTP or grants authority."""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
from typing import Any
from uuid import UUID
import wave

OWNER_FIELDS = ("contextId", "contextid", "context_id", "customerContextId", "ownerContextId")
MAX_AUDIO_BYTES = 16 * 1024 * 1024


def context_id(value: Any) -> str:
    if not isinstance(value, str):
        raise ValueError("Informe um contextId GUID explícito do atendimento autenticado.")
    try:
        result = UUID(value)
    except (ValueError, AttributeError) as exc:
        raise ValueError("contextId inválido; nome, prefixo e número de ramal não são GUIDs.") from exc
    if not result.int:
        raise ValueError("contextId vazio/global não é permitido no N1.")
    return str(result)


def owned(context: str, resource: dict[str, Any]) -> None:
    if not isinstance(resource, dict):
        raise ValueError("A leitura do recurso deve ser um objeto JSON.")
    fields = [resource[key] for key in OWNER_FIELDS if key in resource]
    if not fields:
        raise ValueError("A leitura não informa o dono; obtenha uma leitura autenticada que informe o contexto.")
    if any(context_id(value) != context for value in fields):
        raise ValueError("Recurso de outro cliente ou campos de contexto conflitantes. Nada executado.")


def body_context(context: str, value: Any) -> None:
    if isinstance(value, dict):
        for key, item in value.items():
            if key in OWNER_FIELDS and context_id(item) != context:
                raise ValueError("O corpo contém um contexto diferente do atendimento.")
            body_context(context, item)
    elif isinstance(value, list):
        for item in value:
            body_context(context, item)


def validate(context: str, resources: list[dict[str, Any]], body: Any = None) -> dict[str, Any]:
    context = context_id(context)
    if not resources:
        raise ValueError("Leia os recursos ou o preview autenticado antes de preparar a escrita.")
    for resource in resources:
        owned(context, resource)
    body_context(context, body)
    return {"contextId": context, "checkedResources": len(resources), "executed": False,
            "authorizationVerified": False}


def moh_manifest(context: str, music_class: dict[str, Any], audio: Path, sha256: str) -> dict[str, Any]:
    context = validate(context, [music_class])["contextId"]
    class_id = context_id(music_class.get("id"))
    size = audio.stat().st_size
    if not 0 < size <= MAX_AUDIO_BYTES:
        raise ValueError("Áudio vazio ou acima de 16 MiB.")
    with audio.open("rb") as source:
        payload = source.read(MAX_AUDIO_BYTES + 1)
    if len(payload) != size or len(payload) > MAX_AUDIO_BYTES:
        raise ValueError("O arquivo mudou durante a leitura ou excede 16 MiB.")
    digest = hashlib.sha256(payload).hexdigest()
    if digest != sha256.lower():
        raise ValueError("SHA256 não confere com o arquivo que será enviado.")
    # A valid container/extension does not prove Asterisk codec support. This recipe
    # accepts only the canonical PCM WAV, never raw WhatsApp OGG/Opus or a renamed file.
    try:
        with wave.open(str(audio), "rb") as wav:
            if (wav.getnchannels(), wav.getsampwidth(), wav.getframerate(), wav.getcomptype()) != (1, 2, 8000, "NONE") or wav.getnframes() <= 0:
                raise ValueError("Use WAV PCM16, mono, 8 kHz, com dados de áudio.")
            if len(wav.readframes(wav.getnframes())) != wav.getnframes() * 2:
                raise ValueError("Dados WAV truncados.")
    except (wave.Error, EOFError) as exc:
        raise ValueError("Não é WAV PCM reproduzível; extensão .ogg/.wav não comprova o codec.") from exc
    return {"upload": "music_on_hold_add", "contextId": context, "classId": class_id,
            "file": str(audio.resolve()), "sha256": digest, "validateOnly": True}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=["check", "moh-manifest"])
    parser.add_argument("--context-id", required=True, help="Trusted host customer context; never derive from message text")
    parser.add_argument("--resource", type=Path, action="append", required=True, help="Authenticated resource/preview JSON, with ownership")
    parser.add_argument("--body", type=Path)
    parser.add_argument("--audio", type=Path)
    parser.add_argument("--sha256")
    args = parser.parse_args()
    try:
        resources = [json.loads(p.read_text()) for p in args.resource]
        body = json.loads(args.body.read_text()) if args.body else None
        result = validate(args.context_id, resources, body)
        if args.mode == "moh-manifest":
            if len(resources) != 1 or not args.audio or not args.sha256:
                raise ValueError("moh-manifest exige uma classe, --audio e --sha256.")
            result = moh_manifest(args.context_id, resources[0], args.audio, args.sha256)
        print(json.dumps(result, ensure_ascii=False))
    except (ValueError, OSError, TypeError) as exc:
        parser.exit(2, str(exc) + "\n")


if __name__ == "__main__":
    main()
