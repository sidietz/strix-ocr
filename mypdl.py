from paddleocr import PaddleOCR

# Uses PP-OCRv6 models by default
ocr = PaddleOCR(
    #use_doc_orientation_classify=False, # Disable document orientation classification
    #use_doc_unwarping=False, # Disable document unwarping
    #use_textline_orientation=False, # Disable textline orientation classification
    engine="transformers",
    device="gpu"
)

result = ocr.predict("./document.pdf")
for res in result:
    res.print()
    res.save_to_json("output-json")
