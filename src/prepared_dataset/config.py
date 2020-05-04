import os

FHIR_URL = os.environ.get("FHIR_URL", "http://ketos_preproc:5000")
FHIR_PREPROC_USER = os.environ.get("FHIR_PREPROC_USER", "gemini")
FHIR_PREPROC_PW = os.environ.get("FHIR_PREPROC_PW", None)
GEMINI_URL = os.environ.get("GEMINI_URL", "http://gemini:5000")
GEMINI_USER = os.environ.get("GEMINI_USER", "gemini")
GEMINI_PW = os.environ.get("GEMINI_PW", None)