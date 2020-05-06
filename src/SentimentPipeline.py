import Algorithmia


# API calls will begin at the apply() method, with the request body passed as 'input'
# For more details, see algorithmia.com/developers/algorithm-development/languages
def apply(input):
    output = {}
    client = Algorithmia.client()
    # check that the input type is of a valid type
    if isinstance(input, str):
        if client.dir(input).exists():
            # lets get all of the data API URIs for each file in the provided directory
            files = ["data://" + file.path for file in client.dir(input).files()]
        else:
            raise Exception(
                "input {} is not a valid data API input, or you don't have permission to access it".format(input))
    elif isinstance(input, list):
        # if the input a list of data URIs, lets skip directory scanning and process each URI normally
        files = input
    else:
        raise Exception("input type incorrect, found {}".format(str(type(input))))

    for url in files:
        # extract text from image using OCR
        body = client.algo("util/ExtractText/0.1.1").pipe(url).result
        body = body.rstrip("\n")

        # determine language of text
        lang = client.algo("nlp/LanguageIdentification/1.0.0").pipe({"sentence": body}).result

        # translate non-English text
        if lang != 'en':
            input = {"action": "translate", "text": body}
            body = client.algo("translation/GoogleTranslate/0.1.1").pipe(input).result["translation"]

        # Tokenize text for analysis by sentence
        token_body = client.algo("ApacheOpenNLP/SentenceDetection/0.1.0").pipe(body).result

        # determine sentiment of tokenized text
        keyword_sentiment = []
        for token in token_body:
            print(url + " -> " + token)
            sent = client.algo("nlp/SentimentAnalysis/1.0.5").pipe({"document": token}).result[0]["sentiment"]
            keyword_sentiment.append(sent)

        avg_sent = sum(keyword_sentiment) / len(keyword_sentiment)

        # record output
        output[url] = {"average sentiment": avg_sent}

    return output

#hello team!

if __name__ == "__main__":
    input = "data://AlgorithmiaSE/sentiment_pipe"
    print(apply(input))
