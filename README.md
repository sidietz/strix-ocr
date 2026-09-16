# strix-ocr

## Introduction
strix-ocr is a collection of scripts about how to use PaddleOCR on AMD strix laptops.

## Disclaimer
The paddle.py script was created by AI (Google Gemini 3.8 Flash - medium) based on my hand-written mypdl.py. The AI mainly added the CLI interface. The prompt used was:
```
In this project you'll find mypdl.py. Create a new python script paddle.py which uses the core functionality but adds a reasonable cli (e.g. -i for input file) interface using argparse.
```

## Instructions
The following code snippets assume python envs are lying under ~/.avenv and python3.12 is installed.

### Preparations for GPU support

The rocm and torch versions are subject to change. The code snippeds are copied from [the official rocm.docs.amd.com](https://rocm.docs.amd.com/projects/ai-ecosystem/en/latest/frameworks/pytorch/install.html?fam=ryzen&gpu=amd-ryzen-ai-9-hx-475&os=linux&rocm-ver=10.0.0&pytorch-ver=2.13.0&i=pip&w=compute&gfx=gfx1150).

```bash
python3.12 -m venv ~/.avenv/paddleocr
source ~/.avenv/paddleocr/bin/activate
pip install --index-url https://stable.repo.amd.com/rocm/whl-next/ \
    "torch[device-gfx1150]==2.12.0+rocm10.0.0" \
    "torchvision[device-gfx1150]==0.27.0+rocm10.0.0" \
    "torchaudio==2.11.0+rocm10.0.0"
python -c "import torch; print(torch.cuda.is_available())"
```

The last script should return true, which means the necessary rocm dependencies for gpu support are installed properly.

### Installation

I am not sure if [all] is necessary.

```bash
pip install transformers paddleocr[all]
```

### Usage

```bash
python paddle.py -i document.pdf
```

The resulting .json files are in the folder output-json by default.

### CLI interface
```
python paddle.py --help
usage: paddle.py [-h] -i INPUT [INPUT ...] [-o OUTPUT_DIR] [--no-json] [--save-img] [-q]
                 [--device {gpu,cpu}] [--engine ENGINE]
                 [--ocr-version {PP-OCRv3,PP-OCRv4,PP-OCRv5,PP-OCRv6}] [--lang LANG]
                 [--text-det-model TEXT_DET_MODEL] [--text-rec-model TEXT_REC_MODEL]
                 [--doc-orientation-classify | --no-doc-orientation-classify]
                 [--doc-unwarping | --no-doc-unwarping]
                 [--textline-orientation | --no-textline-orientation]
                 [--score-thresh SCORE_THRESH] [--return-word-box | --no-return-word-box]

PaddleOCR document and image text recognition CLI.

options:
  -h, --help            show this help message and exit
  -i INPUT [INPUT ...], --input INPUT [INPUT ...]
                        Path to one or more input image or document files (e.g. PDF, PNG,
                        JPG). (default: None)
  -o OUTPUT_DIR, --output-dir OUTPUT_DIR
                        Directory to save output files. (default: output-json)
  --no-json             Disable saving OCR results to JSON. (default: False)
  --save-img            Save visualized OCR result image(s) to output directory. (default:
                        False)
  -q, --quiet           Suppress printing OCR results to console. (default: False)
  --device {gpu,cpu}    Device to use for inference. (default: gpu)
  --engine ENGINE       Inference engine backend. (default: transformers)
  --ocr-version {PP-OCRv3,PP-OCRv4,PP-OCRv5,PP-OCRv6}
                        OCR model version to use. (default: None)
  --lang LANG           Model language (e.g. 'en', 'ch'). (default: None)
  --text-det-model TEXT_DET_MODEL
                        Specific text detection model name (e.g. PP-OCRv5_server_det).
                        (default: None)
  --text-rec-model TEXT_REC_MODEL
                        Specific text recognition model name (e.g. PP-OCRv5_server_rec).
                        (default: None)
  --doc-orientation-classify, --no-doc-orientation-classify
                        Enable/disable document orientation classification. (default: None)
  --doc-unwarping, --no-doc-unwarping
                        Enable/disable document unwarping. (default: None)
  --textline-orientation, --no-textline-orientation
                        Enable/disable textline orientation classification. (default: None)
  --score-thresh SCORE_THRESH
                        Text recognition score threshold. (default: None)
  --return-word-box, --no-return-word-box
                        Whether to return word-level bounding boxes. (default: None)

```



