import importlib
import re

def test_consumer_prints_messages(monkeypatch, capsys):
    monkeypatch.setenv("BOOTSTRAP", "test:1234")
    monkeypatch.setenv("TOPIC", "unit-topic")
    monkeypatch.setenv("GROUP_ID", "unit-group")

    import src.consumer as cons
    importlib.reload(cons)

    class Msg:
        def __init__(self, i):
            self.topic = "unit-topic"
            self.partition = 0
            self.offset = i
            self.key = None
            self.value = {"hello": i}

    class FakeConsumer:
        def __init__(self, *a, **kw):
            self.closed = False
        def __iter__(self):
            for i in range(2):
                yield Msg(i)
            import src.consumer as _c
            _c.running = False
            return
        def close(self):
            self.closed = True

    monkeypatch.setattr(cons, "KafkaConsumer", FakeConsumer)

    cons.main()

    out = capsys.readouterr().out
    assert "Waiting for messages..." in out
    assert re.search(r"offset\s*=?\s*0\b", out)
    assert re.search(r"offset\s*=?\s*1\b", out)
