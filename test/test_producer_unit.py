import importlib
def test_producer_sends_10(monkeypatch):
    monkeypatch.setenv("BOOTSTRAP", "test:1234"); monkeypatch.setenv("TOPIC", "unit-topic")
    import src.producer as producer; importlib.reload(producer)
    monkeypatch.setattr(producer.time, "sleep", lambda x: None)
    class _Meta: 
        def __init__(self, t, p, o): self.topic=t; self.partition=p; self.offset=o
    class _Future: 
        def __init__(self, t, i): self._m=_Meta(t,0,i)
        def get(self, timeout=None): return self._m
    class FakeProducer:
        def __init__(self,*a,**k): self.sent=[]
        def send(self, topic, value):
            assert isinstance(value, dict); i=len(self.sent); self.sent.append((topic,value)); return _Future(topic,i)
        def flush(self): pass
    holder={}; monkeypatch.setattr(producer, "KafkaProducer", lambda *a,**k: holder.setdefault('inst', FakeProducer()))
    producer.main(); inst=holder['inst']; assert len(inst.sent)==10; assert all(t=="unit-topic" for t,_ in inst.sent)
    for _, payload in inst.sent: assert {"id","ts","message"} <= set(payload.keys())
