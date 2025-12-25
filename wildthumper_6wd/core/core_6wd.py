class WildthumperCore:
    name = "Wildthumper_6wd"

    def on_ready(self, ctx):
        # optionnel: tu peux t’abonner à des events si tu veux
        ctx.bus.on("key.ctrl_q", self.on_quit)
        self.log(ctx, "info" , "Wildthumper Core is ready.")

    def on_quit(self, ctx):
        # appelé par masterstruct quand CTRL+Q est détecté
        ctx.kernel.shutdown()

    def log(self, ctx, level: str, msg: str):
        logger = (
            getattr(ctx, "logger", None)
            or getattr(getattr(ctx, "kernel", None), "logger", None)
            or getattr(getattr(ctx, "system", None), "logger", None)
        )
        if logger:
            fn = getattr(logger, level, logger.info)
            fn(f"[{self.name}] {msg}")
