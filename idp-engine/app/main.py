import logging
import os
import sys

from app.core.router import DocumentRouter

def configure_logging():
    """
    Configure global logging based on LOG_LEVEL environment variable.
    Defaults to INFO.
    """
    log_level = os.getenv("LOG_LEVEL", "INFO").upper()

    logging.basicConfig(
        level=getattr(logging, log_level, logging.INFO),
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )


def process_document(pdf_path: str):
    """
    Core processing function.
    Entry point used by CLI or NestJS integration.
    """
    router = DocumentRouter()
    result = router.process(pdf_path)
    return result


def main():
    configure_logging()

    if len(sys.argv) < 2:
        print("Usage: python -m app.main <pdf_path>")
        sys.exit(1)

    pdf_path = sys.argv[1]

    if not os.path.exists(pdf_path):
        print(f"File not found: {pdf_path}")
        sys.exit(1)

    try:
        result = process_document(pdf_path)

        # If result is a Pydantic model
        if hasattr(result, "model_dump_json"):
            print(result.model_dump_json(indent=2))
        else:
            print(result)

    except ValueError as e:
        logging.error(str(e))
        sys.exit(1)
    except Exception:
        logging.exception("Unhandled error during document processing")
        sys.exit(1)


if __name__ == "__main__":
    main()