from sigil4py.uap_public_paca_core import *
def test_public_projection_admits_without_private_payload():
    r=compile_public_uap("sigilbook:sha",[PublicProjection("PACA_CORE","KLI:PACA_CORE","sha256:public",("READ","TYPE"))])
    assert r.verdict is Verdict.ADMIT
    assert not r.private_payload_embedded
    assert not r.cpython_private_api_required
def test_quno_holds():
    r=compile_public_uap("",[PublicProjection("PACA_CORE","KLI:PACA_CORE","",("READ",))])
    assert r.verdict is Verdict.HOLD
