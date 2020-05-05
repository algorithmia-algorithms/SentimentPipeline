from . import SentimentPipeline

def test_SentimentPipeline():
    assert SentimentPipeline.apply("Jane") == "hello Jane"
