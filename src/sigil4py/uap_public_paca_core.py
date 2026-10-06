"""Public UAP projection from canonical SIGILBOOK into sigil4cpython.

This module validates a publication manifest. It never fetches private source,
transports private payload, or grants CPython/runtime authority.
"""
from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from hashlib import sha256
import json
SCHEMA_ID="SIGILBOOK_SIGIL4CPYTHON_UAP_PUBLIC_PACA_CORE_V1"
class Verdict(str,Enum): ADMIT="ADMIT"; HOLD="HOLD"; REJECT="REJECT"
@dataclass(frozen=True)
class PublicProjection:
    type_id:str
    interface_id:str
    public_digest:str
    capabilities:tuple[str,...]
    quno:tuple[str,...]=()
@dataclass(frozen=True)
class PublicUAPReceipt:
    schema_id:str
    source_commit:str
    projection_digest:str
    verdict:Verdict
    quno:tuple[str,...]
    private_payload_embedded:bool=False
    cpython_private_api_required:bool=False
    identity_transport:bool=False
    authority_transport:bool=False
def compile_public_uap(source_commit:str, projections:list[PublicProjection])->PublicUAPReceipt:
    hard=[]; q=[]
    if not source_commit:q.append("SIGILBOOK_SOURCE_COMMIT_PENDING")
    ids=[p.interface_id for p in projections]
    if len(ids)!=len(set(ids)):hard.append("DUPLICATE_PUBLIC_INTERFACE_ID")
    for p in projections:
        q.extend(p.quno)
        if not p.public_digest:q.append(f"PUBLIC_DIGEST_PENDING:{p.interface_id}")
    payload=[{"type":p.type_id,"interface":p.interface_id,"digest":p.public_digest,"capabilities":sorted(p.capabilities)} for p in projections]
    digest=sha256(json.dumps(payload,sort_keys=True,separators=(",",":")).encode()).hexdigest()
    v=Verdict.REJECT if hard else (Verdict.HOLD if q else Verdict.ADMIT)
    return PublicUAPReceipt(SCHEMA_ID,source_commit,digest,v,tuple(hard+q))
