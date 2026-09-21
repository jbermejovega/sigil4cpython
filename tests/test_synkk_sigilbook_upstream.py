from sigil4py.synkk_sigilbook_upstream import *
def test_source_ahead_is_plan_not_git_effect():
    r=synkk(SynkkPin("jbermejovega/sigilbook","b170dc","PACA:V2"),SynkkPin("jbermejovega/sigil4cpython","64f87a","PACA:V1"))
    assert r.state is SyncState.SOURCE_AHEAD
    assert not r.git_effect_executed and not r.private_payload_transported
