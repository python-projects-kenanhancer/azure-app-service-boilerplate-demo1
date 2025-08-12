from infrastructure import LoggerStrategy, Settings, WebAppInterface, pipeline, shared_pipeline
from interfaces import ApplicationBootstrap


@pipeline(shared_pipeline)
def main(web_app: WebAppInterface, logger: LoggerStrategy, settings: Settings, bootstrap: ApplicationBootstrap):
    """Main application entry point with DI injection via pipeline."""

    # Build and initialize the application
    bootstrap.build()

    # Get configuration from settings (injected via DI)
    host = settings.host
    port = settings.port
    debug = settings.debug

    logger.info(f"🌐 Starting web server on {host}:{port} (debug={debug})")

    try:
        # Run the web application
        web_app.run(host=host, port=port, debug=debug)
    except KeyboardInterrupt:
        logger.info("🛑 Application stopped by user")
    except Exception as e:
        logger.error(f"❌ Application error: {str(e)}")
        raise


if __name__ == "__main__":
    main()
