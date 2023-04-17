from dotenv import load_dotenv

from manager.main import main

if __name__ == "__main__":
    load_dotenv()
    raise SystemExit(main())
    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(main())
