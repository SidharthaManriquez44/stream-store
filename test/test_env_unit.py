import importlib
def test_env_overrides(monkeypatch):
    monkeypatch.setenv("BOOTSTRAP","envhost:9999"); monkeypatch.setenv("TOPIC","env-topic"); monkeypatch.setenv("GROUP_ID","env-group")
    import src.producer as producer; import importlib as _il; _il.reload(producer)
    import src.consumer as consumer; _il.reload(consumer)
    assert producer.BOOTSTRAP=="envhost:9999" and producer.TOPIC=="env-topic"
    assert consumer.BOOTSTRAP=="envhost:9999" and consumer.TOPIC=="env-topic" and consumer.GROUP_ID=="env-group"
