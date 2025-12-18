class WildthumperCore:
    name = "Wildthumper_6wd"

    def on_ready(self, ctx):
        # appelé quand le système est démarré
        print("online ✅")

        # optionnel: tu peux t’abonner à des events si tu veux
        ctx.bus.on("key.ctrl_q", self.on_quit)

    def on_quit(self, ctx):
        # appelé par masterstruct quand CTRL+Q est détecté
        ctx.kernel.shutdown()
