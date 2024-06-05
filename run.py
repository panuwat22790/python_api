import uvicorn
import main
import logging
from pathlib import Path

logging.basicConfig(filename="error.log", level=logging.ERROR)
Path = str(Path(__file__).parent.resolve())

if __name__ == "__main__":
    print("\n #Update:V.1.0506224 \n\n" )
    try:
        uvicorn.run("main:app"
                    ,host="wash.sbcservice.com"
                    , port=8884, log_level="info", reload=False
                    ,ssl_keyfile = f"SSL2024\\key.pem",ssl_certfile =f"SSL2024\\cert.pem")
    except Exception as e:
        logging.error("An error occurred", exc_info=True)
    finally:
        input("Press Enter to exit...")
