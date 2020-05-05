# SentimentPipeline
This is a new version of [AlgorithmiaSE/SentimentPipe](https://algorithmia.com/algorithms/AlgorithmiaSE/SentimentPipe) that is backed by github and
 leverages github actions to facilitate CI/CD code management best practices.

Curious as to how we define the github CI integration? Click [here.](https://github.com/algorithmia-algorithms/SentimentPipeline/blob/master/.github/workflows/main.yml)

## Overview

This pipeline is used to identify negative news reports from customers. Originally this pipline only accepted .TXT documents, however it was modified to use an OCR model to also utilize PDF or image files.
![Composability](https://algorithmia.com/v1/data/AlgorithmiaSE/composability/WP5-2_Composability_v.2.0.png)

Algorithms in this pipeline
1. [Extract Text](https://algorithmia.com/algorithms/util/ExtractText)
2. [Language Identification](https://algorithmia.com/algorithms/nlp/LanguageIdentification)
3. [Translator](https://algorithmia.com/algorithms/translation/GoogleTranslate)
4. [Sentence Detection](https://algorithmia.com/algorithms/ApacheOpenNLP/SentenceDetection)
5. [Sentiment Analysis](https://algorithmia.com/algorithms/nlp/SentimentAnalysis)

### Applicable Scenarios and Problems

Specify a path you with to process files in a directory, the output for each file will be an average sentiment.

## Usage

### Input

There is only one input to pass, a string containing some URL to a algorithmia [data collection](https://algorithmia.com/data), or a group of files; either hosted on Algorithmia or publicly accessable on the internet.

| Parameter | Description |
| --------- | ----------- |
| URL     | This algorithm handles any URL, be it from the Data API or the URL to a file on the internet. |

### Output

The output is JSON containing the average sentiment for each file processed.

| Parameter | Description |
| --------- | ----------- |
| Data API File     | The file processed to extract an average sentiment. |
| Average Sentiment     | The average sentiment from the processed file. |

## Examples

### Example 1 - data collection
Example input:
```
"data://AlgorithmiaSE/sentiment_pipe"
```
Example Ouput:
```
{
  "data://AlgorithmiaSE/sentiment_pipe/like.pdf": {
    "average sentiment": 0.474
  },
  "data://AlgorithmiaSE/sentiment_pipe/like.txt": {
    "average sentiment": 0.474
  }
}
```

### Example 2 - list of data files
Example input:
```
["data://AlgorithmiaSE/sentiment_pipe/like.pdf", "data://AlgorithimiaSE/sentiment_pipe/like.txt"]
```
Example Ouput:
```
{
  "data://AlgorithmiaSE/sentiment_pipe/like.pdf": {
    "average sentiment": 0.474
  },
  "data://AlgorithmiaSE/sentiment_pipe/like.txt": {
    "average sentiment": 0.474
  }
}
```