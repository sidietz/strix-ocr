#!/usr/bin/env python3
"""CLI interface for PaddleOCR inference based on mypdl.py core functionality."""

import argparse
import os
import sys
from pathlib import Path
from paddleocr import PaddleOCR


def parse_args(args=None):
    parser = argparse.ArgumentParser(
        description="PaddleOCR document and image text recognition CLI.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    # Input and Output options
    parser.add_argument(
        "-i",
        "--input",
        nargs="+",
        required=True,
        help="Path to one or more input image or document files (e.g. PDF, PNG, JPG).",
    )
    parser.add_argument(
        "-o",
        "--output-dir",
        default="output-json",
        help="Directory to save output files.",
    )
    parser.add_argument(
        "--no-json",
        action="store_true",
        help="Disable saving OCR results to JSON.",
    )
    parser.add_argument(
        "--save-img",
        action="store_true",
        help="Save visualized OCR result image(s) to output directory.",
    )
    parser.add_argument(
        "-q",
        "--quiet",
        action="store_true",
        help="Suppress printing OCR results to console.",
    )

    # Model and hardware options
    parser.add_argument(
        "--device",
        default="gpu",
        choices=["gpu", "cpu"],
        help="Device to use for inference.",
    )
    parser.add_argument(
        "--engine",
        default="transformers",
        help="Inference engine backend.",
    )
    parser.add_argument(
        "--ocr-version",
        choices=["PP-OCRv3", "PP-OCRv4", "PP-OCRv5", "PP-OCRv6"],
        default=None,
        help="OCR model version to use.",
    )
    parser.add_argument(
        "--lang",
        default=None,
        help="Model language (e.g. 'en', 'ch').",
    )
    parser.add_argument(
        "--text-det-model",
        default=None,
        help="Specific text detection model name (e.g. PP-OCRv5_server_det).",
    )
    parser.add_argument(
        "--text-rec-model",
        default=None,
        help="Specific text recognition model name (e.g. PP-OCRv5_server_rec).",
    )

    # Document preprocessing options
    parser.add_argument(
        "--doc-orientation-classify",
        action=argparse.BooleanOptionalAction,
        default=None,
        help="Enable/disable document orientation classification.",
    )
    parser.add_argument(
        "--doc-unwarping",
        action=argparse.BooleanOptionalAction,
        default=None,
        help="Enable/disable document unwarping.",
    )
    parser.add_argument(
        "--textline-orientation",
        action=argparse.BooleanOptionalAction,
        default=None,
        help="Enable/disable textline orientation classification.",
    )

    # Recognition tuning options
    parser.add_argument(
        "--score-thresh",
        type=float,
        default=None,
        help="Text recognition score threshold.",
    )
    parser.add_argument(
        "--return-word-box",
        action=argparse.BooleanOptionalAction,
        default=None,
        help="Whether to return word-level bounding boxes.",
    )

    return parser.parse_args(args)


def init_ocr(args):
    ocr_kwargs = {
        "engine": args.engine,
        "device": args.device,
    }
    if args.lang:
        ocr_kwargs["lang"] = args.lang
    if args.ocr_version:
        ocr_kwargs["ocr_version"] = args.ocr_version
    if args.text_det_model:
        ocr_kwargs["text_detection_model_name"] = args.text_det_model
    if args.text_rec_model:
        ocr_kwargs["text_recognition_model_name"] = args.text_rec_model
    if args.doc_orientation_classify is not None:
        ocr_kwargs["use_doc_orientation_classify"] = args.doc_orientation_classify
    if args.doc_unwarping is not None:
        ocr_kwargs["use_doc_unwarping"] = args.doc_unwarping
    if args.textline_orientation is not None:
        ocr_kwargs["use_textline_orientation"] = args.textline_orientation
    if args.score_thresh is not None:
        ocr_kwargs["text_rec_score_thresh"] = args.score_thresh
    if args.return_word_box is not None:
        ocr_kwargs["return_word_box"] = args.return_word_box

    return PaddleOCR(**ocr_kwargs)


def process_file(ocr, input_file, args):
    predict_kwargs = {}
    if args.doc_orientation_classify is not None:
        predict_kwargs["use_doc_orientation_classify"] = args.doc_orientation_classify
    if args.doc_unwarping is not None:
        predict_kwargs["use_doc_unwarping"] = args.doc_unwarping
    if args.textline_orientation is not None:
        predict_kwargs["use_textline_orientation"] = args.textline_orientation
    if args.score_thresh is not None:
        predict_kwargs["text_rec_score_thresh"] = args.score_thresh
    if args.return_word_box is not None:
        predict_kwargs["return_word_box"] = args.return_word_box

    results = ocr.predict(input_file, **predict_kwargs)
    for res in results:
        if not args.quiet:
            res.print()
        if not args.no_json:
            res.save_to_json(args.output_dir)
        if args.save_img:
            res.save_to_img(args.output_dir)


def main(args=None):
    parsed_args = parse_args(args)

    # Validate input files
    for file_path in parsed_args.input:
        if not os.path.exists(file_path):
            print(f"Error: Input file '{file_path}' does not exist.", file=sys.stderr)
            sys.exit(1)

    # Create output directory if saving outputs
    if not parsed_args.no_json or parsed_args.save_img:
        os.makedirs(parsed_args.output_dir, exist_ok=True)

    ocr = init_ocr(parsed_args)

    for file_path in parsed_args.input:
        process_file(ocr, file_path, parsed_args)


if __name__ == "__main__":
    main()
